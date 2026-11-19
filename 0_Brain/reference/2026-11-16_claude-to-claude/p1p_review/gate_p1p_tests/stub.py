import os, socket, sys, time, threading
# stub.py <sock> <mode>: modes: garbage, noline, close, slow11, huge, wrongdec, allow_nohalt, okfalse_unknown, partial
path, mode = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
os.chmod(os.path.dirname(os.path.dirname(path)), 0o700)
try: os.unlink(path)
except FileNotFoundError: pass
s = socket.socket(socket.AF_UNIX); s.bind(path); s.listen(8)
held = []
def serve(c):
    f = c.makefile('rb'); f.readline()
    if mode == 'garbage': c.sendall(b'this is not json\n')
    elif mode == 'noline': held.append(c); return
    elif mode == 'close': c.close(); return
    elif mode == 'slow11': time.sleep(11); c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"allow","reason":"r","halt":false}}\n')
    elif mode == 'huge': c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"allow","reason":"' + b'a'*(4*1024*1024) + b'","halt":false}}\n')
    elif mode == 'wrongdec': c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"ALLOW","reason":"r","halt":false}}\n')
    elif mode == 'allow_nohalt': c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"allow","reason":"r"}}\n')
    elif mode == 'okfalse_unknown': c.sendall(b'{"v":1,"id":1,"ok":false,"error":{"code":"made_up","message":"m"},"result":{"decision":"allow","reason":"r","halt":false}}\n')
    elif mode == 'ok_string': c.sendall(b'{"v":1,"id":1,"ok":"true","result":{"decision":"allow","reason":"r","halt":false}}\n')
    elif mode == 'partial': c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"allow"'); c.close(); return
    elif mode == 'wrongid': c.sendall(b'{"v":1,"id":999,"ok":true,"result":{"decision":"allow","reason":"r","halt":false}}\n')
    elif mode == 'reason_num': c.sendall(b'{"v":1,"id":1,"ok":true,"result":{"decision":"allow","reason":5,"halt":false}}\n')
    try: c.close()
    except Exception: pass
while True:
    c, _ = s.accept(); threading.Thread(target=serve, args=(c,), daemon=True).start()
