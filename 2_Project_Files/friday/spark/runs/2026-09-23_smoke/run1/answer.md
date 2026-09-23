--- a/2_Project_Files/tests/absence_claim_check_arms.sh
+++ b/2_Project_Files/tests/absence_claim_check_arms.sh
@@ -2,3 +2,3 @@
 # Arms for tools/absence_claim_check.sh. Each prints PASS/FAIL; exit 1 if any fail.
-C=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/absence_claim_check.sh; F=0
+C="$(dirname "$0")/../tools/absence_claim_check.sh"; F=0
 arm(){ # name, text, expect_flag(yes/no)