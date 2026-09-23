# FIX-1 mul-multiplies — make calc.mul multiply instead of add

File: `calc.py`
Runner: `python3 -m unittest`

## The exact change

Edit 1 — line 9, replacement.

```
-    return a + b
+    return a * b
```

## The test

File: `test_calc.py`

## Output

Exactly ONE fenced diff block, nothing outside it.
