//! QA gate round 2: attacks on `FragTracker` (G3 fix). Differential against tungstenite itself.
//! Included from meter.rs with `#[cfg(test)] #[path = "gate_r2_meter.rs"] mod gate_r2;`.

use super::*;
use std::io::{self, Cursor, Read, Write};
use tokio_tungstenite::tungstenite::protocol::frame::FrameHeader;
use tokio_tungstenite::tungstenite::protocol::{Role, WebSocket, WebSocketConfig};
use tokio_tungstenite::tungstenite::{Error as WsError, Message};

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

/// A masked client frame with an explicit length encoding (0 = minimal, 1 = force 16-bit, 2 = force 64-bit).
fn frame(fin: bool, opcode: u8, n: usize, enc: u8, rng: &mut Rng) -> Vec<u8> {
    let mut v = vec![if fin { 0x80 } else { 0 } | opcode];
    let form = match (enc, n) {
        (0, 0..=125) => 0,
        (0, 126..=65535) | (1, 0..=65535) => 1,
        _ => 2,
    };
    match form {
        0 => v.push(0x80 | n as u8),
        1 => {
            v.push(0x80 | 126);
            v.extend_from_slice(&(n as u16).to_be_bytes());
        }
        _ => {
            v.push(0x80 | 127);
            v.extend_from_slice(&(n as u64).to_be_bytes());
        }
    }
    let key = (rng.next() as u32).to_be_bytes();
    v.extend_from_slice(&key);
    // payload 'a' (valid UTF-8 for text), masked
    for i in 0..n {
        v.push(b'a' ^ key[i % 4]);
    }
    v
}

/// In-memory server-side socket: reads from `inp`, swallows writes; WouldBlock when drained.
struct Mem {
    inp: Cursor<Vec<u8>>,
}
impl Read for Mem {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = self.inp.read(buf)?;
        if n == 0 && !buf.is_empty() {
            return Err(io::ErrorKind::WouldBlock.into());
        }
        Ok(n)
    }
}
impl Write for Mem {
    fn write(&mut self, b: &[u8]) -> io::Result<usize> {
        Ok(b.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

fn feed_chunked(t: &mut FragTracker, bytes: &[u8], rng: &mut Rng) {
    let mut rest = bytes;
    while !rest.is_empty() {
        let n = 1 + rng.below(23) as usize;
        let (a, b) = rest.split_at(n.min(rest.len()));
        t.feed(a);
        rest = b;
        if let FragState::Head { have, .. } = t.st {
            assert!(have <= 14, "head buffer bounded");
        }
    }
}

/// Generates a VALID client stream (control frames only between frames, fragments well formed),
/// possibly ending inside a fragmented message. Then checks the tracker's "message open" belief
/// against tungstenite's real state: tungstenite consumes the stream, then is offered a final empty
/// continuation, which completes a message iff one was open (else it is a protocol error).
#[test]
fn r2_g3_tracker_agrees_with_tungstenite_on_random_valid_streams() {
    let mut rng = Rng(0x9e37_79b9_7f4a_7c15);
    let sizes = [0usize, 1, 5, 125, 126, 127, 300, 65535, 65536, 70_000];
    let mut agreed_open = 0;
    let mut agreed_closed = 0;
    for case in 0..3000 {
        let mut s = Vec::new();
        let msgs = 1 + rng.below(4);
        let mut open_at_end = false;
        'm: for mi in 0..msgs {
            let frags = 1 + rng.below(4);
            let op = if rng.below(2) == 0 { 1 } else { 2 };
            for fi in 0..frags {
                // control frames (ping 9 / pong 10), 0..=125 bytes, anywhere between frames
                for _ in 0..rng.below(3) {
                    let c = if rng.below(2) == 0 { 9 } else { 10 };
                    let n = rng.below(126) as usize;
                    s.extend(frame(true, c, n, 0, &mut rng));
                }
                let fin = fi + 1 == frags;
                let opcode = if fi == 0 { op } else { 0 };
                let n = sizes[rng.below(sizes.len() as u64) as usize];
                let enc = if rng.below(4) == 0 { rng.below(3) as u8 } else { 0 };
                s.extend(frame(fin, opcode, n, enc, &mut rng));
                // sometimes stop in the middle of a fragmented message (last message only)
                if mi + 1 == msgs && !fin && rng.below(3) == 0 {
                    open_at_end = true;
                    // trailing pings after the open fragment: the G3 attack shape
                    for _ in 0..rng.below(3) {
                        s.extend(frame(true, 9, 0, 0, &mut rng));
                    }
                    break 'm;
                }
            }
        }
        let mut t = FragTracker::new();
        feed_chunked(&mut t, &s, &mut rng);
        // tungstenite
        let probe = frame(true, 0, 0, 0, &mut rng);
        let mut all = s.clone();
        all.extend_from_slice(&probe);
        let cfg = WebSocketConfig::default()
            .max_message_size(Some(1 << 24))
            .max_frame_size(Some(1 << 24));
        let mut ws = WebSocket::from_raw_socket(Mem { inp: Cursor::new(all) }, Role::Server, Some(cfg));
        let mut data_msgs = 0;
        let mut ended = None;
        loop {
            match ws.read() {
                Ok(Message::Text(_)) | Ok(Message::Binary(_)) => data_msgs += 1,
                Ok(_) => {}
                Err(WsError::Io(e)) if e.kind() == io::ErrorKind::WouldBlock => break,
                Err(e) => {
                    ended = Some(format!("{e}"));
                    break;
                }
            }
        }
        // if a message was open, the probe completed it (data_msgs == msgs) and no error;
        // if none was open, the probe is "continue frame but nothing to continue" (protocol error).
        let ws_open = ended.is_none() && data_msgs as u64 == msgs;
        assert_eq!(
            t.in_frag, ws_open,
            "case {case}: tracker in_frag={} but tungstenite open={ws_open} (err={ended:?}, msgs={msgs}, got={data_msgs}, generator open_at_end={open_at_end})",
            t.in_frag
        );
        assert_eq!(open_at_end, ws_open, "case {case}: generator vs tungstenite");
        if ws_open {
            agreed_open += 1;
        } else {
            agreed_closed += 1;
        }
    }
    assert!(agreed_open > 300 && agreed_closed > 300, "{agreed_open} / {agreed_closed}");
}

/// Header-level differential: for random 2..14-byte headers (any opcode, RSV bits, mask bit,
/// 7/16/64-bit lengths incl. top bit set), the tracker's notion of header length and payload
/// length matches tungstenite's `FrameHeader::parse` whenever tungstenite accepts the header.
#[test]
fn r2_g3_header_parse_matches_tungstenite() {
    let mut rng = Rng(0x0123_4567_89ab_cdef);
    for _ in 0..200_000 {
        let mut h = [0u8; 14];
        for b in &mut h {
            *b = rng.next() as u8;
        }
        // bias the length field toward the extended forms
        match rng.below(3) {
            0 => h[1] = (h[1] & 0x80) | 126,
            1 => h[1] = (h[1] & 0x80) | 127,
            _ => {}
        }
        let hl = head_len(h[1]);
        let mut cur = Cursor::new(&h[..hl]);
        let Ok(Some((th, tlen))) = FrameHeader::parse(&mut cur) else {
            continue;
        };
        assert_eq!(cur.position() as usize, hl, "header length");
        // feed the header to the tracker and check its parsed state
        let mut t = FragTracker::new();
        t.feed(&h[..hl]);
        match t.st {
            FragState::Payload { left, opcode, fin } => {
                assert_eq!(left, tlen);
                assert_eq!(opcode, u8::from(th.opcode));
                assert_eq!(fin, th.is_final);
            }
            FragState::Head { have, .. } => {
                assert_eq!(have, 0);
                assert_eq!(tlen, 0, "a zero-length frame is done at the header");
            }
        }
    }
}

/// Garbage after the upgrade: random bytes, random chunking, every byte boundary. No panic, no
/// arithmetic overflow (debug build), bounded state.
#[test]
fn r2_g3_garbage_never_panics_and_state_is_bounded() {
    let mut rng = Rng(0xdead_beef_cafe_f00d);
    for _ in 0..2000 {
        let n = rng.below(4096) as usize;
        let mut g = vec![0u8; n];
        for b in &mut g {
            *b = rng.next() as u8;
        }
        // sometimes a 64-bit length with the top bit set / u64::MAX
        if n > 10 && rng.below(4) == 0 {
            g[1] = 0xff;
            for b in &mut g[2..10] {
                *b = 0xff;
            }
        }
        let mut t = FragTracker::new();
        feed_chunked(&mut t, &g, &mut rng);
        let mut t2 = FragTracker::new();
        for b in &g {
            t2.feed(std::slice::from_ref(b)); // every byte boundary
        }
        assert_eq!(t.in_frag, t2.in_frag);
    }
    // a u64::MAX payload length simply stays in Payload; feeding more is O(n), no overflow
    let mut t = FragTracker::new();
    t.feed(&[0x02, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 1, 2, 3, 4]);
    t.feed(&vec![0u8; 1 << 16]);
    assert!(matches!(t.st, FragState::Payload { .. }));
}
