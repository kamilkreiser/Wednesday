//! QA: does a stop inside a release survive without its pending anchor? (mutation M7 check)
use super::common::*;
use super::copy_tree;
use crate::fsio::fault::{self, Op, Rule};
use crate::{Causer, Input};

#[test]
fn qa_m7_stop_inside_release() {
    for k in 0..6usize {
        let mut w = World::new(160, 4, 4);
        let base = scratch("qa-m7");
        let root = base.join("host");
        let mut h = create_host(&w, 1, &root, cfg(&w));
        let mut p3 = mem_member(&w, 3);
        for n in 0..3u64 {
            host_record(&mut h, &w.ids[1], Causer::LocalHuman, n + 1);
            let s = p3.record(&w.ids[3], bare("p"), t(n + 1)).unwrap();
            let e = p3.outgoing(s).into_iter().find(|(to, _)| *to == w.key(1)).unwrap().1;
            h.apply(&w.ids[1], Input::Receive(e), t(n + 1)).unwrap();
        }
        let r = w.remove(3);
        h.apply(&w.ids[1], Input::Roster(r), t(10)).unwrap();
        let mut n_unlink = 0usize;
        fault::arm(Rule::StopWhen(Box::new(move |c| {
            if c.op == Op::Unlink && c.dir == "store" {
                if n_unlink == k { return true; }
                n_unlink += 1;
            }
            false
        })));
        let res = h.apply(&w.ids[1], Input::Release(w.key(3)), t(20));
        let rep = fault::disarm();
        drop(h);
        let s = base.join("snap");
        copy_tree(&root, &s);
        let o = open_host(&w, 1, &s, cfg(&w), 30).map(|(_, r)| format!("{:?}", r.opened)).unwrap_or_else(|e| format!("REFUSED {e:?}"));
        println!("QA m7 stop at store unlink #{k}: stopped {} release {:?} -> {o}", rep.stopped, res.as_ref().map(|_| "ok").map_err(|e| format!("{e:?}").chars().take(60).collect::<String>()));
        scratch_done(&base);
    }
}
