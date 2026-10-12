ANSWER to the Vision_Sales_Portal seat (pane %7). Your refusal to bypass was exactly right. This is the Datasec org CodeQL policy (Kam's ruling 2026-09-29): a commit reaches main only after CodeQL has scanned THAT commit on a pull request. Never bypass, never dismiss.

RULED: (b). Kam is asked on his board (card) to run `gh auth login` in your pane, which writes only to your project's 4_Credentials/.gh-config. When gh works (`gh auth status` with your GH_CONFIG_DIR, quote the account), do this:
1. Open the PR feat/qq-cad-currency-2026-10-12 -> main (head 1270b71).
2. Wait for CodeQL (every Analyze run, both thresholds) and tests.yml.
3. Read the PR's open alerts, and merge through GitHub with a merge commit (your --no-ff convention).
4. Read main back by ls-remote and quote the CI run ids.
5. MERGED mail, then wrap.
SUPERSEDES the "HOW" paragraph of the 04:57Z GO; everything else in that GO stands (merge only, no publish, e1a865c excluded).
Meanwhile: leave the unpushed local 8b29136 as it is. Do not reset anything; the PR route makes it moot. If Kam has not done the login when you would otherwise idle, write your handover and wrap. A successor does the PR on his login.
-- Tuesday
