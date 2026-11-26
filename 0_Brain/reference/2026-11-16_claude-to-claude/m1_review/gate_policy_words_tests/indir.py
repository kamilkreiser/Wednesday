# QA-POLICY-WORDS: usage python3 -B indir.py <dir> <prog> [args...]: chdir in-process (no shell cd), then exec
import os, sys
os.chdir(sys.argv[1]); os.execvp(sys.argv[2], sys.argv[2:])
