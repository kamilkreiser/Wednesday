# QA3: exhaustive arithmetic check of the one-comparison argument (brief s.2 item 1), per seat (pb, pr).
# Parts as in src/budget.rs and StoreLimits: seat, own=(pb-.pr, pr), free=own//2, allowance=(own-own//2)//7, pool=7*seat.
SEATS=8; SEAT_BYTES=5_097_490; SEAT_RECORDS=28_604
db,dr=SEAT_BYTES,SEAT_RECORDS; own_max=db-dr
def parts(pb,pr):
    o=(max(pb-pr,0),pr); f=(o[0]//2,o[1]//2); a=((o[0]-f[0])//7,(o[1]-f[1])//7)
    return [(pb,pr),o,f,a,(7*pb,7*pr)]
D=parts(db,dr)
def le(p): return all(x[0]<=y[0] and x[1]<=y[1] for x,y in zip(p,D))
def cap(B,R):
    b=min(B,SEATS*db); r=min(R,SEATS*dr); pb,pr=b//8,r//8
    if max(pb-pr,0)>own_max: b=(own_max+pr)*8
    return b,r
bad=0; tight=0; nec=0
for pr in range(0,dr+1):
    # largest pb the clause allows for this pr, and the cap applied to default bytes
    b,r=cap(SEATS*db, 8*pr); pb=b//8
    if not le(parts(pb,pr)): bad+=1
    # the boundary pb is the maximal: one more byte per seat breaks some part (necessity), unless capped by db
    if pb<db:
        if le(parts(pb+1,pr)): nec+=1
    # every pb up to the boundary is fine is implied by monotonicity; check a few
    for q in (0,1,pb//2,pb-1):
        if q>=0 and not le(parts(q,pr)): bad+=1
    if pb-pr==own_max: tight+=1
print(f"records per seat 0..{dr}: violations {bad}; boundary not maximal (one more byte still within) {nec}; offers lowered to exactly own_max {tight}")
# random big offers incl. near 2**64
import random; random.seed(7)
vals=[0,1,7,8,9,2**64-1,2**64-8,2**63]+[random.randrange(0,2**64) for _ in range(200000)]
bad2=0
for i in range(0,len(vals)-1):
    b,r=cap(vals[i],vals[-1-i]); 
    if not le(parts(b//8,r//8)): bad2+=1
print("random u64 offers:",len(vals)-1,"violations",bad2)
print("pin offer (40779920, 171624) ->",cap(40779920,171624))
