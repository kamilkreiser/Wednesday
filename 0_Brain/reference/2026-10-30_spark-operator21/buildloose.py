# usage: python3 -I buildloose.py spec.py  (builds a real LOOSE candidate: product not given, hunk headers dictated)
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import loosegen21 as lg, mk21
m = lg.load(sys.argv[1]); S = dict(m.S)
S['rung_raw'] = '**' + S['rung'] + '**'
S['loose'] = S['loose'] + lg.dictation(m.S)
mk21.build(S)
