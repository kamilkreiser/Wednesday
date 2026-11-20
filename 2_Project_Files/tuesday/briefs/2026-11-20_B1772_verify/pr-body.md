## What the repository now holds

- An empty .NET 10 solution: a core library with one marker type, one server host that maps no route, and one test project with one test. Package versions are exact, come from one registry, and are held by lock files; on a pipeline runner a restore that does not match the lock files fails.
- One workflow, `ci`, with four jobs: `linux`, `windows`, `secret-scan`, `rules`. It runs on a push to `main`, on a push to a lane branch, on a pull request and by hand. It reads no stored credential, its only permission is to read the code, and every action is pinned to a commit.
- A container file for the Linux packaging and a short note for the Windows packaging.
- Two check scripts in Python (standard library only) with 48 planted-control tests, and an empty deny-list file.

## What each check stops

- `linux` and `windows`: a solution that does not restore from the lock files, build without warnings, pass its tests or publish for that platform. Each then runs the release guard over the published folder. `linux` also builds the container image and pushes it nowhere.
- The release guard: HP's beta library in the published folder, by file name or by content, also inside a ZIP; a certificate whose fingerprint is on the deny-list, or a file carrying the development CA's file name; and any file or ZIP it cannot read, which is a failure and never a skip.
- `secret-scan`: a secret in the history or in the working tree. The job first plants a token outside the checkout and fails unless the scanner finds it. The scanner binary is fetched from its release and checked against a sha256 before it runs.
- `rules`: an ignore file, a baseline, a config file or a narrowing option for the secret scan; a reference to the beta library in what ships; a workflow that names a stored credential, runs with wider rights or uses an action that is not pinned to a commit; a binary or key file by extension. It runs the 48 planted controls first.

## What is NOT built, and what stays open of WP0.3

- The bundle tool in the pipeline, and a test bundle. No job exists for it.
- The fingerprint of the real development CA. The deny-list holds no fingerprint; the guard prints a warning and passes; only the file-name half of that rule works today. A release build must refuse an empty list; that mode is not built.
- Code scanning: no analysis exists for this repository yet.
- The secret scanner skips some file names by its own built-in list (for example `package-lock.json`, `yarn.lock`, `go.sum`, image and font files, anything under `node_modules/`). No such file is in the repository. A rule that refuses those names is not built.
- The release guard reads ZIP files only, and looks for the beta library's name only in files that start like a Windows program file. Other archive formats and a single-file publish are not covered.
- The rule checks read lines, not YAML.
- No check is required by a repository setting. The checks run from the same commit they check.
- The container image has never been started. There is no Windows installer.

So WP0.3 is NOT closed by this change.

## Nothing is deployed, nothing was sent

No workflow deploys, publishes or uploads anything. Nothing was released. Nothing was sent to anyone outside the organisation. No cloud resource was created or touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
