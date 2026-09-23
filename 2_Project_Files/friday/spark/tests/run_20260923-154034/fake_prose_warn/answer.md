Here you go:
```diff
--- a/calc.py
+++ b/calc.py
@@ -7,3 +7,3 @@
 
 def mul(a, b):
-    return a + b
+    return a * b
--- a/test_calc.py
+++ b/test_calc.py
@@ -8,3 +8,6 @@
         self.assertEqual(calc.add(2, 3), 5)
+
+    def test_mul(self):
+        self.assertEqual(calc.mul(3, 4), 12)
 
 
```
