// Gate r2 probe: does an ordinary (non-test) binary see the test-only seam?
type Seal = fn(
    &mut coagent_crypto::channel::Channel,
    coagent_proto::record::RecordKind,
    &[u8],
) -> Result<Vec<u8>, coagent_crypto::CryptoError>;
fn main() {
    let f: Seal = coagent_crypto::channel::Channel::seal_record;
    println!("seal_record reachable from a plain binary: {:p}", f as *const ());
}
