pub fn f() -> bool { let _u = "a//b"; use std /* c */ as s; s::env::var("X").is_ok() }
