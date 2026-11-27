# QA wrapper: runs the UNMODIFIED engine with os.replace instrumented. argv: mode engine_path [engine args...]
import os, sys, time, runpy
sys.dont_write_bytecode=True
mode=sys.argv[1]; engine=sys.argv[2]; sys.argv=[engine]+sys.argv[3:]
real=os.replace; n=[0]
def patched(a,b):
    n[0]+=1
    if mode=="crash-before-2nd" and n[0]==2:
        os._exit(137)          # the process dies between the archive rename and the state rename
    if mode.startswith("barrier:") and n[0]==1:
        gate=mode.split(":",1)[1]
        open(gate+".waiting","w").close()
        while not os.path.exists(gate): time.sleep(0.01)
    return real(a,b)
os.replace=patched
runpy.run_path(engine, run_name="__main__")
