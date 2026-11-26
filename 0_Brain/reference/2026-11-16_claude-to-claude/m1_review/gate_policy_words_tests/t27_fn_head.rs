fn depends_on_policy(manifest: &str) -> bool {
    const NAME: &str = "coagent-policy";
    let unquote = |k: &str| -> String {
        let k = k.trim();
        for q in ['"', '\''] {
            if k.len() >= 2 && k.starts_with(q) && k.ends_with(q) {
                return k[1..k.len() - 1].to_string();
            }
        }
        k.to_string()
    };
    // a table header's keys, split at dots outside quotes
    let keys = |h: &str| -> Vec<String> {
        let (mut out, mut cur, mut quote) = (Vec::new(), String::new(), None::<char>);
        let mut esc = false;
        for c in h.chars() {
            if esc {
                esc = false;
                cur.push(c);
                continue;
            }
            match (quote, c) {
                (Some('"'), '\\') => {
                    esc = true;
                    cur.push(c);
                }
                (None, '.') => out.push(unquote(&std::mem::take(&mut cur))),
                (None, '"' | '\'') => {
                    quote = Some(c);
                    cur.push(c);
                }
                (Some(q), _) if c == q => {
                    quote = None;
                    cur.push(c);
                }
                _ => cur.push(c),
            }
        }
        out.push(unquote(&cur));
        out
    };
    let dep_table = |k: &str| {
        matches!(
            k,
            "dependencies"
                | "dev-dependencies"
                | "build-dependencies"
                | "dev_dependencies"
                | "build_dependencies"
        )
    };
    let after_blanks_is = |rest: &str, c: char| rest.trim_start().starts_with(c);
    // the text before the first `stop` outside quotes (a basic string's `\"` does not end it), if there is one
    let until_outside_quotes = |t: &str, stop: char| -> Option<String> {
        let (mut quote, mut esc) = (None::<char>, false);
        for (i, c) in t.char_indices() {
            if esc {
                esc = false;
                continue;
            }
            match (quote, c) {
                (Some('"'), '\\') => esc = true,
                (Some(q), _) if c == q => quote = None,
                (None, '"' | '\'') => quote = Some(c),
                (None, _) if c == stop => return Some(t[..i].to_string()),
                _ => {}
            }
        }
        None
    };
    // a dependency key path: `<table>.coagent-policy…` or `target.<x>.<table>.coagent-policy…`
    let dep_path = |k: &[String]| {
        (k.len() >= 2 && dep_table(&k[0]) && k[1] == NAME)
            || (k.len() >= 4 && k[0] == "target" && dep_table(&k[2]) && k[3] == NAME)
    };
    let first_header = manifest
        .lines()
        .position(|l| l.trim_start().starts_with('['))
        .unwrap_or(usize::MAX);
    // POLICY-WORDS: does an inline table `{ k = …, k2 = … }` name `coagent-policy` as one of its own keys (its first
    // dotted part, quoted or not; keys of nested tables and text inside quotes do not count)?
    let inline_names_policy = |v: &str| -> bool {
        let Some(body) = v.trim_start().strip_prefix('{') else {
            return false;
        };
        let (mut depth, mut quote, mut esc) = (1usize, None::<char>, false);
        let (mut key, mut in_key) = (String::new(), true);
        for c in body.chars() {
            let keep = in_key && depth == 1;
            if esc {
                esc = false;
            } else {
                match (quote, c) {
                    (Some('"'), '\\') => esc = true,
                    (Some(q), _) if c == q => quote = None,
                    (Some(_), _) => {}
                    (None, '"' | '\'') => quote = Some(c),
                    (None, '{' | '[') => depth += 1,
                    (None, '}' | ']') => {
                        depth -= 1;
                        if depth == 0 {
                            break;
                        }
                    }
                    (None, '=') if keep => {
                        if keys(&key).first().is_some_and(|k| k == NAME) {
                            return true;
                        }
                        key.clear();
                        in_key = false;
                        continue;
                    }
                    (None, ',') if depth == 1 => {
                        key.clear();
                        in_key = true;
                        continue;
                    }
                    _ => {}
                }
            }
            if keep {
                key.push(c);
            }
        }
        false
    };
    // POLICY-WORDS (the POLICY-AT first check's n-7): a dependency table written as ONE inline table naming the crate
    // as a key, at the top level (`dependencies = { coagent-policy = { … } }`, `dev-dependencies = …`,
    // `build-dependencies = …`) or as a line under a `[target.<x>]` header
    let mut header: Option<Vec<String>> = None;
    let inline_table = manifest.lines().any(|l| {
        let t = l.trim_start();
        if t.starts_with('#') {
            return false;
        }
        if let Some(h) = t
            .strip_prefix('[')
            .and_then(|h| until_outside_quotes(h, ']'))
        {
            header = Some(if t.starts_with("[[") {
                vec![String::new()]
            } else {
                keys(&h)
            });
            return false;
        }
        let top_or_target = match &header {
            None => true,
            Some(k) => k.len() == 2 && k[0] == "target",
        };
        if !top_or_target {
            return false;
        }
        let Some(k) = until_outside_quotes(t, '=') else {
            return false;
        };
        let ks = keys(&k);
        ks.len() == 1 && dep_table(&ks[0]) && inline_names_policy(&t[k.len() + 1..])
    });
    if inline_table {
        return true;
    }
    manifest.lines().enumerate().any(|(line_no, l)| {
        let t = l.trim_start();
        // the old disjunct, unchanged
        if t.starts_with(NAME) {
            return true;
        }
        if t.starts_with('#') {
            return false;
        }
        // a table header (its closing `]` found outside quotes)
        if let Some(h) = t
            .strip_prefix('[')
            .and_then(|h| until_outside_quotes(h, ']'))
        {
            let h = h.as_str();
            if !t.starts_with("[[") {
                let k = keys(h);
                let n = k.len();
                if n >= 2
                    && k[n - 1] == NAME
                    && dep_table(&k[n - 2])
                    && (n == 2 || (n == 4 && k[0] == "target"))
                {
                    return true;
                }
            }
        }
        // a top-level dotted key, before any header
        if line_no < first_header {
            if let Some(k) = until_outside_quotes(t, '=') {
                if dep_path(&keys(&k)) {
                    return true;
                }
            }
        }
        // a quoted key
        for q in ["\"coagent-policy\"", "'coagent-policy'"] {
            if let Some(rest) = t.strip_prefix(q) {
                if after_blanks_is(rest, '=') || after_blanks_is(rest, '.') {
                    return true;
                }
            }
        }
        // package = "coagent-policy"
        let mut from = 0;
        while let Some(i) = t[from..].find("package") {
            let at = from + i;
            let before_ok = t[..at]
                .chars()
                .last()
                .is_none_or(|c| !(c.is_ascii_alphanumeric() || c == '_' || c == '-'));
            let mut rest = t[at + "package".len()..].trim_start();
            // a quoted key `"package"` / `'package'`: skip its closing quote
            if let Some(q @ ('"' | '\'')) = t[..at].chars().last() {
                if let Some(r) = t[at + "package".len()..].strip_prefix(q) {
                    rest = r.trim_start();
                }
            }
            if before_ok {
                if let Some(v) = rest.strip_prefix('=') {
                    let v = v.trim_start();
                    if v.starts_with("\"coagent-policy\"")
                        || v.starts_with("'coagent-policy'")
                        || v.starts_with("\"\"\"coagent-policy\"\"\"")
                        || v.starts_with("'''coagent-policy'''")
                    {
                        return true;
                    }
                }
            }
            from = at + "package".len();
        }
        false
    })
}
