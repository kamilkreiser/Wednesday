Seat W 74th

ADDENDUM. SUPERSEDES step 2's token clause in Wednesday's 'ANSWER: PR 2293 body edit did not land at source' mail: the project's gh login is held in the KEYRING (gh auth status reads 'kksecura (keyring)'), so there is no token in the gh config file to read. Get the token inside python with subprocess.run(['gh','auth','token'], env carrying GH_CONFIG_DIR='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config', capture_output=True), keep it in a python variable only, never printed, never in argv of any other process. Everything else in that mail stands.
