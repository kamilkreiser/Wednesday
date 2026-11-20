## What the repository now holds

- An empty .NET 10 solution: a core library with one marker type, one server host that maps no route, and one test project with one test. Package versions are exact, come from one registry, and are held by lock files; on a pipeline runner a restore that does not match the lock files fails. The two runtimes the product is packaged for are declared once, in `Directory.Build.props`, and every project takes them from there.
- One workflow, `ci`, with four jobs: `linux`, `windows`, `secret-scan`, `rules`. It runs on a push to `main`, on a push to a lane branch, on a pull request and by hand. It reads no stored credential, its only permission is to read the code, and every action is pinned to a commit.
- A container file for the Linux packaging and a short note for the Windows packaging.
- Two check scripts in Python (standard library only) with 53 planted-control tests in three test files, and a deny-list file that holds comment lines only.

## What each check stops

- `linux` and `windows`: a solution that does not restore from the lock files, build without warnings, pass its tests or publish for that platform. Each then runs the release guard over the published folder. `linux` also builds the container image and pushes it nowhere.
- The release guard: HP's beta library in the published folder, by file name or by content, also inside a ZIP; a certificate whose fingerprint is on the deny-list, or a file carrying the development CA's file name; and any file or ZIP it cannot read, which is a failure and never a skip. A deny-list that cannot be opened is a failure, never an empty list.
- `secret-scan`: a secret in the history or in the working tree, and then a second scan of every object the checkout holds, for every branch and tag of the origin: every file of every commit, every commit with its header lines and its message, every annotated tag with its message, and every folder listing with the file and folder names in it. Each object is copied twice under a neutral name, once behind one plain first line and once behind a plain block of 43008 bytes, so the scanner reads the two copies in different pieces. The scanner on its own skips many files by name (lock files, images, fonts, anything under `node_modules/`) and files that start like a PDF, a program or an archive, and no pass of it reads a commit message, a tag message or a file name; under the neutral names it reads all of these. The job first builds a planted repository that holds a token in 11 places (six files, five of which the scanner does not read under their own names; a file name; a folder name; a commit message; a tag message; and across the scanner's read cut in a large file with no blank line) and fails unless the second scan finds the token exactly 25 times. It also fails when the checkout holds an ignore file of the scanner. The scanner binary is fetched from its release and checked against a sha256 before it runs.
- `rules`: an ignore file, a baseline, a config file or a narrowing option for the secret scan; a reference to the beta library in what ships; a workflow that names a stored credential, runs with wider rights or uses an action that is not pinned to a commit; a binary or key file by extension. It runs the 53 planted controls first and fails unless at least 53 ran; a test fails unless that floor equals the number of controls.
- A test holds the text of the `secret-scan` job and of the `rules` job to a fingerprint, so a change inside either job also needs a change in a second file, where a reviewer sees it.

## What the second scan does not see

- Text saved as UTF-16 or UTF-32; compressed content; a secret split over two lines.
- The names of branches and tags: they are not stored objects.
- An object that only another kind of ref on the origin reaches, a git note for example: the job reads what the branches and the tags reach.
- A secret across a read cut in a large file that has blank lines but none within 25 kB of that cut. In a file with no blank line at all the two copies cover each other.
- A rule of the scanner that is keyed on a file name fires in the scan by name only.

Two things follow from reading everything. Every run reads every branch of the origin, so a token on one branch, or a commit message the scanner flags, turns `secret-scan` red for every branch until that commit is gone from the origin. And there is no ignore mechanism, by rule: the answer to a real finding is to revoke the credential and remove the commit, never to add an ignore file.

No stored object holds a secret at the reviewed head: all 71 objects of the repository (37 files, 4 commits, 30 folder listings) pass the second scan.

## What is NOT built, and what stays open of WP0.3

- The bundle tool in the pipeline, and a test bundle. No job exists for it.
- The fingerprint of the real development CA. The deny-list holds no fingerprint; the guard prints a warning and passes; only the file-name half of that rule works today. A release build must refuse an empty list; that mode is not built.
- Code scanning: no analysis exists for this repository yet.
- The release guard reads ZIP files only, and looks for the beta library's name only in files that start like a Windows program file. Other archive formats and a single-file publish are not covered.
- The rule checks read lines, not YAML.
- No check is required by a repository setting, and the checks run from the same commit they check. The fingerprint covers two jobs, not the whole workflow: a change outside them, or a commit that changes a job and its fingerprint together, is caught only by review.
- The container image has never been started. There is no Windows installer.

So WP0.3 is NOT closed by this change.

## Nothing is deployed, nothing was sent

No workflow deploys, publishes or uploads anything. Nothing was released. Nothing was sent to anyone outside the organisation. No cloud resource was created or touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
