| q | site | value | base | head | same |
|---|---|---|---|---|---|
| Q4 | BruteForce.get | V01 ordinary Error | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | BruteForce.get | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V04 null | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V05 undefined | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V06 string | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | BruteForce.get | V07 number | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V09 {message: Symbol} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V10 {message: BigInt} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V11 {message: revoked Proxy} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V12 {message: obj whose toString throws} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.get | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V14 thrown Symbol | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | BruteForce.get | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | BruteForce.get | V17 plain {message} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | BruteForce.set | V01 ordinary Error | out=returned undefined; sentinelLines=1 | out=returned undefined; sentinelLines=1 | = |
| Q4 | BruteForce.set | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V04 null | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V05 undefined | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V06 string | out=returned undefined; sentinelLines=1 | out=returned undefined; sentinelLines=1 | = |
| Q4 | BruteForce.set | V07 number | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V09 {message: Symbol} | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V10 {message: BigInt} | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V11 {message: revoked Proxy} | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V12 {message: obj whose toString throws} | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | BruteForce.set | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V14 thrown Symbol | out=returned undefined; sentinelLines=1 | out=returned undefined; sentinelLines=1 | = |
| Q4 | BruteForce.set | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=returned undefined; sentinelLines=0 | DIFF |
| Q4 | BruteForce.set | V17 plain {message} | out=returned undefined; sentinelLines=0 | out=returned undefined; sentinelLines=0 | = |
| Q4 | CSRF.generate | V01 ordinary Error | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | CSRF.generate | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V04 null | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V05 undefined | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V06 string | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | CSRF.generate | V07 number | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V09 {message: Symbol} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V10 {message: BigInt} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V11 {message: revoked Proxy} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V12 {message: obj whose toString throws} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.generate | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V14 thrown Symbol | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | CSRF.generate | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | CSRF.generate | V17 plain {message} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | CSRF.validate | V01 ordinary Error | out=returned false; sentinelLines=1 | out=returned false; sentinelLines=1 | = |
| Q4 | CSRF.validate | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V04 null | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V05 undefined | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V06 string | out=returned false; sentinelLines=1 | out=returned false; sentinelLines=1 | = |
| Q4 | CSRF.validate | V07 number | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V09 {message: Symbol} | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V10 {message: BigInt} | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V11 {message: revoked Proxy} | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V12 {message: obj whose toString throws} | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | CSRF.validate | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V14 thrown Symbol | out=returned false; sentinelLines=1 | out=returned false; sentinelLines=1 | = |
| Q4 | CSRF.validate | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=returned false; sentinelLines=0 | DIFF |
| Q4 | CSRF.validate | V17 plain {message} | out=returned false; sentinelLines=0 | out=returned false; sentinelLines=0 | = |
| Q4 | RateLimit.get | V01 ordinary Error | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | RateLimit.get | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V04 null | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V05 undefined | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V06 string | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | RateLimit.get | V07 number | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V09 {message: Symbol} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V10 {message: BigInt} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V11 {message: revoked Proxy} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V12 {message: obj whose toString throws} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.get | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V14 thrown Symbol | out=returned null; sentinelLines=1 | out=returned null; sentinelLines=1 | = |
| Q4 | RateLimit.get | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=returned null; sentinelLines=0 | DIFF |
| Q4 | RateLimit.get | V17 plain {message} | out=returned null; sentinelLines=0 | out=returned null; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V01 ordinary Error | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | = |
| Q4 | RateLimit.increment | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V04 null | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V05 undefined | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V06 string | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | = |
| Q4 | RateLimit.increment | V07 number | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V09 {message: Symbol} | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V10 {message: BigInt} | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V11 {message: revoked Proxy} | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V12 {message: obj whose toString throws} | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | RateLimit.increment | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V14 thrown Symbol | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=1 | = |
| Q4 | RateLimit.increment | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | RateLimit.increment | V17 plain {message} | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | out=returned {"count":1,"resetAt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V01 ordinary Error | out=returned 0; sentinelLines=1 | out=returned 0; sentinelLines=1 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V02 Error, message getter throws | out=returned 0; sentinelLines=1 | out=returned 0; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.getAttempts (get fails) | V03 revoked Proxy | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V04 null | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V05 undefined | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V06 string | out=returned 0; sentinelLines=1 | out=returned 0; sentinelLines=1 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V07 number | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V08 Object.create(null) | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V09 {message: Symbol} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V10 {message: BigInt} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V11 {message: revoked Proxy} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V12 {message: obj whose toString throws} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V13 Proxy whose get trap throws | out=returned 0; sentinelLines=1 | out=returned 0; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.getAttempts (get fails) | V14 thrown Symbol | out=returned 0; sentinelLines=1 | out=returned 0; sentinelLines=1 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V15 Error, name getter throws (message readable) | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V16 {message readable, toString throws} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.getAttempts (get fails) | V17 plain {message} | out=returned 0; sentinelLines=0 | out=returned 0; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V01 ordinary Error | out=returned {"blocked":false}; sentinelLines=1 | out=returned {"blocked":false}; sentinelLines=1 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V02 Error, message getter throws | out=returned {"blocked":false}; sentinelLines=1 | out=returned {"blocked":false}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V03 revoked Proxy | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V04 null | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V05 undefined | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V06 string | out=returned {"blocked":false}; sentinelLines=1 | out=returned {"blocked":false}; sentinelLines=1 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V07 number | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V08 Object.create(null) | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V09 {message: Symbol} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V10 {message: BigInt} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V11 {message: revoked Proxy} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V12 {message: obj whose toString throws} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V13 Proxy whose get trap throws | out=returned {"blocked":false}; sentinelLines=1 | out=returned {"blocked":false}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V14 thrown Symbol | out=returned {"blocked":false}; sentinelLines=1 | out=returned {"blocked":false}; sentinelLines=1 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V15 Error, name getter throws (message readable) | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V16 {message readable, toString throws} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.isBlocked (get fails; stored record says BLOCKED) | V17 plain {message} | out=returned {"blocked":false}; sentinelLines=0 | out=returned {"blocked":false}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V01 ordinary Error | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V02 Error, message getter throws | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (get fails) | V03 revoked Proxy | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V04 null | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V05 undefined | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V06 string | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V07 number | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V08 Object.create(null) | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V09 {message: Symbol} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V10 {message: BigInt} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V11 {message: revoked Proxy} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V12 {message: obj whose toString throws} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V13 Proxy whose get trap throws | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (get fails) | V14 thrown Symbol | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V15 Error, name getter throws (message readable) | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V16 {message readable, toString throws} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (get fails) | V17 plain {message} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V01 ordinary Error | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V02 Error, message getter throws | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V03 revoked Proxy | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V04 null | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V05 undefined | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V06 string | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V07 number | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V08 Object.create(null) | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V09 {message: Symbol} | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V10 {message: BigInt} | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V11 {message: revoked Proxy} | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V12 {message: obj whose toString throws} | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V13 Proxy whose get trap throws | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=1 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V14 thrown Symbol | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=1 | = |
| Q4 | caller BruteForce.recordFailure (set fails) | V15 Error, name getter throws (message readable) | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V16 {message readable, toString throws} | out=returned {"attempts":1,"lastAttempt":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | DIFF |
| Q4 | caller BruteForce.recordFailure (set fails) | V17 plain {message} | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | out=returned {"attempts":100,"lastAttempt":"<t>","blockedUntil":"<t>"}; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V01 ordinary Error | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | caller CSRF.refresh (set fails) | V02 Error, message getter throws | out=threw Error (new: S-getter); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V03 revoked Proxy | out=threw TypeError (new); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V04 null | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V05 undefined | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V06 string | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | caller CSRF.refresh (set fails) | V07 number | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V08 Object.create(null) | out=threw TypeError (new); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V09 {message: Symbol} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V10 {message: BigInt} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V11 {message: revoked Proxy} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V12 {message: obj whose toString throws} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q4 | caller CSRF.refresh (set fails) | V13 Proxy whose get trap throws | out=threw Error (new: S-trap); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V14 thrown Symbol | out=threw SAME value rethrown; sentinelLines=1 | out=threw SAME value rethrown; sentinelLines=1 | = |
| Q4 | caller CSRF.refresh (set fails) | V15 Error, name getter throws (message readable) | out=threw Error (new: name boom); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V16 {message readable, toString throws} | out=threw Error (new: ts boom); sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | DIFF |
| Q4 | caller CSRF.refresh (set fails) | V17 plain {message} | out=threw SAME value rethrown; sentinelLines=0 | out=threw SAME value rethrown; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V01 ordinary Error | out=resolved; nextCalls=2; sentinelLines=1 | out=resolved; nextCalls=2; sentinelLines=1 | = |
| Q5a | cacheMiddleware via downstream next() throws | V02 Error, message getter throws | out=rejected Error (new: S-getter); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V03 revoked Proxy | out=rejected TypeError (new); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V04 null | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V05 undefined | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V06 string | out=resolved; nextCalls=2; sentinelLines=1 | out=resolved; nextCalls=2; sentinelLines=1 | = |
| Q5a | cacheMiddleware via downstream next() throws | V07 number | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V08 Object.create(null) | out=rejected TypeError (new); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V09 {message: Symbol} | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V10 {message: BigInt} | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V11 {message: revoked Proxy} | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V12 {message: obj whose toString throws} | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via downstream next() throws | V13 Proxy whose get trap throws | out=rejected Error (new: S-trap); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V14 thrown Symbol | out=resolved; nextCalls=2; sentinelLines=1 | out=resolved; nextCalls=2; sentinelLines=1 | = |
| Q5a | cacheMiddleware via downstream next() throws | V15 Error, name getter throws (message readable) | out=rejected Error (new: name boom); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V16 {message readable, toString throws} | out=rejected Error (new: ts boom); nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via downstream next() throws | V17 plain {message} | out=resolved; nextCalls=2; sentinelLines=0 | out=resolved; nextCalls=2; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V01 ordinary Error | out=resolved; nextCalls=1; sentinelLines=1 | out=resolved; nextCalls=1; sentinelLines=1 | = |
| Q5a | cacheMiddleware via redis.get fails | V02 Error, message getter throws | out=rejected Error (new: S-getter); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V03 revoked Proxy | out=rejected TypeError (new); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V04 null | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V05 undefined | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V06 string | out=resolved; nextCalls=1; sentinelLines=1 | out=resolved; nextCalls=1; sentinelLines=1 | = |
| Q5a | cacheMiddleware via redis.get fails | V07 number | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V08 Object.create(null) | out=rejected TypeError (new); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V09 {message: Symbol} | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V10 {message: BigInt} | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V11 {message: revoked Proxy} | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V12 {message: obj whose toString throws} | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5a | cacheMiddleware via redis.get fails | V13 Proxy whose get trap throws | out=rejected Error (new: S-trap); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V14 thrown Symbol | out=resolved; nextCalls=1; sentinelLines=1 | out=resolved; nextCalls=1; sentinelLines=1 | = |
| Q5a | cacheMiddleware via redis.get fails | V15 Error, name getter throws (message readable) | out=rejected Error (new: name boom); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V16 {message readable, toString throws} | out=rejected Error (new: ts boom); nextCalls=0; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | DIFF |
| Q5a | cacheMiddleware via redis.get fails | V17 plain {message} | out=resolved; nextCalls=1; sentinelLines=0 | out=resolved; nextCalls=1; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V01 ordinary Error | out=resolved isRedis=false; sentinelLines=1 | out=resolved isRedis=false; sentinelLines=1 | = |
| Q5b | caller getSecurityStores | V02 Error, message getter throws | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V03 revoked Proxy | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V04 null | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V05 undefined | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V06 string | out=resolved isRedis=false; sentinelLines=1 | out=resolved isRedis=false; sentinelLines=1 | = |
| Q5b | caller getSecurityStores | V07 number | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V08 Object.create(null) | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V09 {message: Symbol} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V10 {message: BigInt} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V11 {message: revoked Proxy} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V12 {message: obj whose toString throws} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V13 Proxy whose get trap throws | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V14 thrown Symbol | out=resolved isRedis=false; sentinelLines=1 | out=resolved isRedis=false; sentinelLines=1 | = |
| Q5b | caller getSecurityStores | V15 Error, name getter throws (message readable) | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V16 {message readable, toString throws} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | caller getSecurityStores | V17 plain {message} | out=resolved isRedis=false; sentinelLines=0 | out=resolved isRedis=false; sentinelLines=0 | = |
| Q5b | redisClient.connect | V01 ordinary Error | out=rejected SAME value rethrown; sentinelLines=1 | out=rejected SAME value rethrown; sentinelLines=1 | = |
| Q5b | redisClient.connect | V02 Error, message getter throws | out=rejected Error (new: S-getter); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V03 revoked Proxy | out=rejected TypeError (new); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V04 null | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V05 undefined | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V06 string | out=rejected SAME value rethrown; sentinelLines=1 | out=rejected SAME value rethrown; sentinelLines=1 | = |
| Q5b | redisClient.connect | V07 number | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V08 Object.create(null) | out=rejected TypeError (new); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V09 {message: Symbol} | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V10 {message: BigInt} | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V11 {message: revoked Proxy} | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V12 {message: obj whose toString throws} | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5b | redisClient.connect | V13 Proxy whose get trap throws | out=rejected Error (new: S-trap); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V14 thrown Symbol | out=rejected SAME value rethrown; sentinelLines=1 | out=rejected SAME value rethrown; sentinelLines=1 | = |
| Q5b | redisClient.connect | V15 Error, name getter throws (message readable) | out=rejected Error (new: name boom); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V16 {message readable, toString throws} | out=rejected Error (new: ts boom); sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | DIFF |
| Q5b | redisClient.connect | V17 plain {message} | out=rejected SAME value rethrown; sentinelLines=0 | out=rejected SAME value rethrown; sentinelLines=0 | = |
| Q5c | pool caller acquire | V01 ordinary Error | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool caller acquire | V02 Error, message getter throws | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V03 revoked Proxy | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V04 null | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V05 undefined | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V06 string | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool caller acquire | V07 number | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V08 Object.create(null) | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V09 {message: Symbol} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V10 {message: BigInt} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V11 {message: revoked Proxy} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V12 {message: obj whose toString throws} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller acquire | V13 Proxy whose get trap throws | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V14 thrown Symbol | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool caller acquire | V15 Error, name getter throws (message readable) | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V16 {message readable, toString throws} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller acquire | V17 plain {message} | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Acquire timeout - pool exhausted); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V01 ordinary Error | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller initialize | V02 Error, message getter throws | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=1 | out=rejected Error (new: S-getter); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V03 revoked Proxy | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected TypeError (new); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V04 null | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V05 undefined | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V06 string | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller initialize | V07 number | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V08 Object.create(null) | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected TypeError (new); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V09 {message: Symbol} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V10 {message: BigInt} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V11 {message: revoked Proxy} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V12 {message: obj whose toString throws} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller initialize | V13 Proxy whose get trap throws | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=1 | out=rejected Error (new: S-trap); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V14 thrown Symbol | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller initialize | V15 Error, name getter throws (message readable) | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: name boom); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V16 {message readable, toString throws} | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: ts boom); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller initialize | V17 plain {message} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V01 ordinary Error | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller performMaintenance (create) | V02 Error, message getter throws | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=1 | out=rejected Error (new: S-getter); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V03 revoked Proxy | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected TypeError (new); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V04 null | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V05 undefined | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V06 string | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller performMaintenance (create) | V07 number | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V08 Object.create(null) | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected TypeError (new); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V09 {message: Symbol} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V10 {message: BigInt} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V11 {message: revoked Proxy} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V12 {message: obj whose toString throws} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool caller performMaintenance (create) | V13 Proxy whose get trap throws | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=1 | out=rejected Error (new: S-trap); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V14 thrown Symbol | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=4 | = |
| Q5c | pool caller performMaintenance (create) | V15 Error, name getter throws (message readable) | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: name boom); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V16 {message readable, toString throws} | out=resolved; factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: ts boom); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool caller performMaintenance (create) | V17 plain {message} | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V01 ordinary Error | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool createConnection direct | V02 Error, message getter throws | out=rejected Error (new: S-getter); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V03 revoked Proxy | out=rejected TypeError (new); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V04 null | out=rejected Error (new: Failed to create connection); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Failed to create connection); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V05 undefined | out=rejected Error (new: Failed to create connection); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected Error (new: Failed to create connection); factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V06 string | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool createConnection direct | V07 number | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V08 Object.create(null) | out=rejected TypeError (new); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V09 {message: Symbol} | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V10 {message: BigInt} | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V11 {message: revoked Proxy} | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V12 {message: obj whose toString throws} | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool createConnection direct | V13 Proxy whose get trap throws | out=rejected Error (new: S-trap); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V14 thrown Symbol | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=3 | = |
| Q5c | pool createConnection direct | V15 Error, name getter throws (message readable) | out=rejected Error (new: name boom); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V16 {message readable, toString throws} | out=rejected Error (new: ts boom); factoryCalls=1; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool createConnection direct | V17 plain {message} | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=rejected SAME value rethrown; factoryCalls=3; removedEvents=0; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V01 ordinary Error | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V02 Error, message getter throws | out=rejected Error (new: S-getter); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V03 revoked Proxy | out=rejected TypeError (new); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V04 null | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V05 undefined | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V06 string | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V07 number | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V08 Object.create(null) | out=rejected TypeError (new); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V09 {message: Symbol} | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V10 {message: BigInt} | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V11 {message: revoked Proxy} | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V12 {message: obj whose toString throws} | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V13 Proxy whose get trap throws | out=rejected Error (new: S-trap); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V14 thrown Symbol | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=2 | = |
| Q5c | pool removeConnection via maintenance (close throws) | V15 Error, name getter throws (message readable) | out=rejected Error (new: name boom); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V16 {message readable, toString throws} | out=rejected Error (new: ts boom); factoryCalls=2; removedEvents=0; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | DIFF |
| Q5c | pool removeConnection via maintenance (close throws) | V17 plain {message} | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | out=resolved; factoryCalls=3; removedEvents=2; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V01 ordinary Error | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | = |
| Q5d | pool maintenance interval | V02 Error, message getter throws | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=3 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V03 revoked Proxy | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V04 null | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V05 undefined | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V06 string | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | = |
| Q5d | pool maintenance interval | V07 number | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V08 Object.create(null) | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V09 {message: Symbol} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V10 {message: BigInt} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V11 {message: revoked Proxy} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V12 {message: obj whose toString throws} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
| Q5d | pool maintenance interval | V13 Proxy whose get trap throws | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=3 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V14 thrown Symbol | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=12 | = |
| Q5d | pool maintenance interval | V15 Error, name getter throws (message readable) | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V16 {message readable, toString throws} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=3; sentinelLines=0 | DIFF |
| Q5d | pool maintenance interval | V17 plain {message} | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | out=ran; ticksWithFactoryCalls=True; unhandledRejections=0; sentinelLines=0 | = |
