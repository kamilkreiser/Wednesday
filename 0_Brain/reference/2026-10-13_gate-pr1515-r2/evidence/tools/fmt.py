import sys,json
for l in sys.stdin:
  try: r=json.loads(l)
  except: print(l.rstrip()); continue
  print(f"{r['shape']:52} tsc={r['tsc']} {','.join(r['codes']):16} dev={r['dev']} {r['dev_tags']}  head={r['head']} {r['head_tags']}")
