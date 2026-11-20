## What the repository now holds

- An empty .NET 10 solution: a core library with one marker type, one server host that maps no route, and one test project with one test. Package versions are exact, come from one registry, and are held by lock files; on a pipeline runner a restore that does not match the lock files fails. The two runtimes the product is packaged for are declared once, in `Directory.Build.props`, and every project takes them from there.
- One workflow, `ci`, with four jobs: `linux`, `windows`, `secret-scan`, `rules`. It runs on a push to `main`, on a push to a lane branch, on a pull request and by hand. It reads no stored credential, its only permission is to read the code, and every action is pinned to a commit.
- A container file for the Linux packaging and a short note for the Windows packaging.
- Two check scripts in Python (standard library only) with 53 planted-control tests in three test files, and an empty deny-list file.

## What each check stops

- `linux` and `windows`: a solution that does not restore from the lock files, build without warnings, pass its tests or publish for that platform. Each then runs the release guard over the published folder. `linux` also builds the container image and pushes it nowhere.
- The release guard: HP's beta library in the published folder, by file name or by content, also inside a ZIP; a certificate whose fingerprint is on the deny-list, or a file carrying the development CA's file name; and any file or ZIP it cannot read, which is a failure and never a skip. A deny-list that cannot be opened is a failure, never an empty list.
- `secret-scan`: a secret in the history or in the working tree, and then a second scan: every file the repository stores, in any commit of any branch the job fetched, is copied under a neutral name behind one plain first line and scanned again. The scanner on its own skips many files by name (lock files, images, fonts, anything under `node_modules/`) and files that start like a PDF, a program or an archive; under the neutral name it reads them. The job first plants six files, five of which the scanner does not read under their own names, and fails unless the second scan finds all six. The scanner binary is fetched from its release and checked against a sha256 before it runs.
- `rules`: an ignore file, a baseline, a config file or a narrowing option for the secret scan; a reference to the beta library in what ships; a workflow that names a stored credential, runs with wider rights or uses an action that is not pinned to a commit; a binary or key file by extension. It runs the 53 planted controls first and fails unless at least 53 ran; a test fails unless that floor equals the number of controls.
- A test holds the text of the `secret-scan` job and of the `rules` job to a fingerprint, so a change inside either job also needs a change in a second file, where a reviewer sees it.

## What the second scan does not see

- Text saved as UTF-16, compressed content, a secret split over two lines.
- A secret in a commit message, in a tag message or in a file name: only files are exported.
- A secret that lies across a read cut of a large file that has no blank line (the scanner reads 125 kB at a time).
- A file made on purpose with one of three byte marks at a fixed place (the scanner takes it for another kind of file and skips it).
- A rule of the scanner that is keyed on a file name does not fire under the neutral name; it still fires in the scan by name.
- No file in the repository holds a secret today: every stored object, messages and file names included, was scanned in review.

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
