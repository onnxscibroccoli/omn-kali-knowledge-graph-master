# Two public URLs, two machines

Operator confirmation 2026-09-29 plus public HTTP checks and helix repo config.

## Path A — intentional hypervisor console

URL: `https://d22bad48irrbqe.cloudfront.net/novnc/vnc.html`

Lands on the EC2 host desktop. This is intended direct hypervisor access, not a defect.

Evidence:
- Public GET returns 200 noVNC page.
- Operator: this URL opens Debian and should stay.
- `uname` in that session: `root@ip-172-31-8-59` / `6.12.107+deb13-cloud-amd64`.
- Unit `production/desktop/helix-novnc.service`:
  `websockify --web=/usr/share/novnc 127.0.0.1:6080 127.0.0.1:5900`

Status: OBSERVED, accepted by operator as hypervisor access.

## Path B — authenticated Kali control plane

URL: `https://d22bad48irrbqe.cloudfront.net/auth/login`

Product path: Cognito → Helix session → Launch desktop → ticketed WSS → guest VNC for `helix-omnikali`.

Status: OBSERVED authenticated guest path by operator.

## Rule

```
/novnc/vnc.html  = Debian hypervisor console (intentional)
/auth/login      = control plane → Kali guest helix-omnikali
```

Do not collapse these. Do not remove Path A unless the operator asks.
