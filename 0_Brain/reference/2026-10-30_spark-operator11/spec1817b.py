import importlib.util, os
_s = importlib.util.spec_from_file_location('s1817', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec1817.py')); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
T = _m.T2
