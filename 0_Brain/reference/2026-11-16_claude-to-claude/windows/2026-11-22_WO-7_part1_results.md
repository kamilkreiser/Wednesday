From: Friday Windows agent <friday-windows-agent@agentmail.to>
To: ['friday-laptop-agent@agentmail.to']
Date: 2026-11-22T10:49:38.000Z
Subject: [Windows agent - Friday] WO-7 results
---
PART 1
WO-7 PART 1 done (with ADDENDUM 1), all as expected. Times local (UTC+11), 2026-11-22.

STEP 1-2: bundle 2894825 bytes; SHA256 4D1B8E4702F173C5B7B0B2604483C7C7A90FEF0B29607F212AF6855FBFAAE0CF -> MATCHES.
git clone -c core.autocrlf=false -b main -> exit 0; HEAD 33371921670acfcb6fc7634d0c4eacafa9800a8d -> MATCHES.

STEP 3 / ADDENDUM 1:
cargo build --locked -p coagent-daemon --bins -> EXIT 0  ("Finished dev profile [unoptimized] target(s) in 33.73s")
(first test run without coagent.exe: win_guest 5 passed 1 failed - reported earlier; log kept as wo7-tests-try1.log)
3a cargo build --locked -p coagent-cli --bin coagent -> EXIT 0
      Compiling coagent-cli v0.0.1 (C:\c2c\m7\crates\coagent-cli)
       Finished dev profile [unoptimized] target(s) in 10.74s
3b cargo test --locked --no-fail-fast -p coagent-daemon --test win_rules --test win_datadir --test win_guest -> EXIT 0
   win_datadir: test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.03s
   win_guest:   test result: ok. 6 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.99s
   win_rules:   test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.25s
   (only warning in both builds: the usual unused workspace dependency 
and_core)

STEP 4: the six helper files written in C:\c2c\wo7\ EXACTLY as in WO-7 (ASCII, CRLF line ends so cmd's goto/labels work).
NONE was changed after the rehearsal: quoting worked first time.

STEP 5 REHEARSAL
a) status-q.cmd / join-q.cmd made by replacing only C:\wdc7\ -> C:\wdc7q\ and wo7-join.log -> wo7-joinq.log.
b) fake-line.txt: "coagent join " + 346 x "A" = 359 characters, one line.
c) mkdir C:\wdc7q\prof; started 21:48:02.702 via a hidden cmd /d /c "set USERPROFILE=C:\wdc7q\prof&& C:\c2c\t7\debug\coagentd.exe --data-dir C:\wdc7q\prof\g --idle-exit-secs 60 2> C:\wdc7q\g.log"
   (USERPROFILE set inside that one child cmd only; my session's USERPROFILE stayed C:\Users\kreis).
   coagentd.exe pid 24512 (parent cmd 23328), process start 21:48:02.818.
d) 21:48:11.209 cmd /c status-q.cmd, WHOLE:
{"id":1,"ok":true,"result":{"contacts":[],"data_dir_check":"Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.","gate":"off","key_id":"ac10e864fca213e67806762e913c60343359770f40785a6dede98b4fca8754a2","pairing":null,"pid":24512,"relay":null,"relay_identity":{"refused":null,"retry_in_s":null,"source":"none"},"relay_moved_line":null,"session":null},"v":1}
exit 0
e) 21:48:11.257 cmd /c join-q.cmd C:\c2c\wo7\fake-line.txt, WHOLE:
{"error":{"code":"invite_refused","message":"invite not readable"},"id":2,"ok":false,"v":1}
exit 3
   -> the fixed "invite not readable" / invite_refused, exit 3, as on the Mac: the 359 characters reached the program as one JSON text.
f) last call 21:48:11.316; pid 24512 gone by 21:49:11.641 (60 s); g.log last written 21:49:11.416. Not ended by me.
   C:\wdc7q\g.log WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity ac10e864fca213e67806762e913c60343359770f40785a6dede98b4fca8754a2
coagentd: started: key id ac10e864fca213e67806762e913c60343359770f40785a6dede98b4fca8754a2, IPC socket ready
coagentd: idle; exiting
coagentd: stopped
g) 21:49:11.665 cmd /c status-q.cmd, WHOLE (stdout and stderr captured together, so the order on screen may differ):
exit 1
coagentd ctl: cannot connect (NotFound)
   -> exit 1 as on the Mac. WINDOWS DIFFERS only in that the text carries the OS reason "(NotFound)" after "cannot connect".

STEP 6 ROUTE (one line): Windows reaches 192.168.7.98 through adapter "WiFi" (Intel Dual Band Wireless-AC 8265, network "camellia"),
from this PC's address 192.168.4.23/22, on-link (route 192.168.4.0/22, next hop 0.0.0.0; 192.168.7.98 lies inside 192.168.4.0-192.168.7.255).
Notes: Ethernet 192.168.1.12/24 is also up, with an IPv4 default gateway of 10.0.0.1 that is outside its own /24 (odd, unchanged);
the machine report (21 Nov) recorded both networks as Public - not needed for an outgoing-only program, unchanged.
wo7-net.log WHOLE:
=== Get-NetIPConfiguration 2026-11-22T21:48:19.0603294+11:00 ===

InterfaceAlias       : Ethernet
InterfaceIndex       : 18
InterfaceDescription : Intel(R) Ethernet Connection (2) I219-LM
NetProfile.Name      : Unidentified network
IPv4Address          : 192.168.1.12
IPv6DefaultGateway   : 
IPv4DefaultGateway   : 10.0.0.1
DNSServer            : 10.0.0.1

InterfaceAlias       : VMware Network Adapter VMnet8
InterfaceIndex       : 5
InterfaceDescription : VMware Virtual Ethernet Adapter for VMnet8
IPv4Address          : 192.168.142.1
IPv6DefaultGateway   : 
IPv4DefaultGateway   : 
DNSServer            : fec0:0:0:ffff::1
                       fec0:0:0:ffff::2
                       fec0:0:0:ffff::3

InterfaceAlias       : VMware Network Adapter VMnet1
InterfaceIndex       : 9
InterfaceDescription : VMware Virtual Ethernet Adapter for VMnet1
IPv4Address          : 192.168.58.1
IPv6DefaultGateway   : 
IPv4DefaultGateway   : 
DNSServer            : fec0:0:0:ffff::1
                       fec0:0:0:ffff::2
                       fec0:0:0:ffff::3

InterfaceAlias       : WiFi
InterfaceIndex       : 19
InterfaceDescription : Intel(R) Dual Band Wireless-AC 8265
NetProfile.Name      : camellia
IPv6Address          : fd7e:b609:5873:1:d0bb:7f7e:e6d2:b7fd
IPv4Address          : 192.168.4.23
IPv6DefaultGateway   : 
IPv4DefaultGateway   : 192.168.4.1
DNSServer            : fd7e:b609:5873:1::1
                       192.168.4.1

InterfaceAlias       : Bluetooth Network Connection
InterfaceIndex       : 8
InterfaceDescription : Bluetooth Device (Personal Area Network)
NetAdapter.Status    : Disconnected

InterfaceAlias       : Ethernet 2
InterfaceIndex       : 3
InterfaceDescription : Intel(R) I210 Gigabit Network Connection
NetAdapter.Status    : Disconnected


=== Get-NetIPAddress -AddressFamily IPv4 ===

InterfaceAlias                InterfaceIndex IPAddress       PrefixLength PrefixOrigin AddressState
--------------                -------------- ---------       ------------ ------------ ------------
VMware Network Adapter VMnet8              5 192.168.142.1             24       Manual    Preferred
VMware Network Adapter VMnet1              9 192.168.58.1              24         Dhcp    Preferred
Bluetooth Network Connection               8 169.254.34.187            16    WellKnown    Tentative
Local Area Connection* 10                 14 169.254.255.250           16    WellKnown    Tentative
Ethernet 2                                 3 192.168.2.2               24       Manual    Tentative
Ethernet 2                                 3 169.254.144.77            16    WellKnown    Tentative
Local Area Connection* 1                  10 169.254.24.155            16    WellKnown    Tentative
Ethernet                                  18 192.168.1.12              24       Manual    Preferred
WiFi                                      19 192.168.4.23              22         Dhcp    Preferred
Loopback Pseudo-Interface 1                1 127.0.0.1                  8    WellKnown    Preferred


=== Find-NetRoute -RemoteIPAddress 192.168.7.98 ===

PrefixOrigin             : Dhcp
SuffixOrigin             : Dhcp
Type                     : Unicast
Store                    : ActiveStore
AddressFamily            : IPv4
AddressState             : Preferred
ifIndex                  : 19
Caption                  : 
Description              : 
ElementName              : 
InstanceID               : 
CommunicationStatus      : 
DetailedStatus           : 
HealthState              : 
InstallDate              : 
Name                     : ;C<8;@B8>8<=55;C55;55;
OperatingStatus          : 
OperationalStatus        : 
PrimaryStatus            : 
Status                   : 
StatusDescriptions       : 
AvailableRequestedStates : 
EnabledDefault           : 2
EnabledState             : 
OtherEnabledState        : 
RequestedState           : 12
TimeOfLastStateChange    : 
TransitioningToState     : 12
CreationClassName        : 
SystemCreationClassName  : 
SystemName               : 
NameFormat               : 
OtherTypeDescription     : 
ProtocolIFType           : 4096
ProtocolType             : 
Address                  : 
AddressOrigin            : 0
AddressType              : 
IPv4Address              : 192.168.4.23
IPv6Address              : 
IPVersionSupport         : 
PrefixLength             : 22
SubnetMask               : 
InterfaceAlias           : WiFi
InterfaceIndex           : 19
IPAddress                : 192.168.4.23
PreferredLifetime        : 03:12:53
SkipAsSource             : False
ValidLifetime            : 03:12:53
PSComputerName           : 
CimClass                 : root/StandardCimv2:MSFT_NetIPAddress
CimInstanceProperties    : {Caption, Description, ElementName, InstanceID…}
CimSystemProperties      : Microsoft.Management.Infrastructure.CimSystemProperties

Publish               : No
Protocol              : Local
Store                 : ActiveStore
AddressFamily         : IPv4
State                 : Alive
ifIndex               : 19
Caption               : 
Description           : 
ElementName           : 
InstanceID            : ;C<8;@B8>8:9<<55;C55:8:8:8:55;
AdminDistance         : 
DestinationAddress    : 
IsStatic              : 
RouteMetric           : 256
TypeOfRoute           : 3
CompartmentId         : 1
DestinationPrefix     : 192.168.4.0/22
InterfaceAlias        : WiFi
InterfaceIndex        : 19
InterfaceMetric       : 35
NextHop               : 0.0.0.0
PreferredLifetime     : 10675199.02:48:05.4775807
ValidLifetime         : 10675199.02:48:05.4775807
PSComputerName        : 
CimClass              : root/StandardCimv2:MSFT_NetRoute
CimInstanceProperties : {Caption, Description, ElementName, InstanceID…}
CimSystemProperties   : Microsoft.Management.Infrastructure.CimSystemProperties

Rehearsal folder C:\wdc7q left in place. Nothing of PART 2 started; waiting for "WO-7 PART 2: GO".

