# Remote Provider-Agnostic Browser Plane 2026-10-01

The web automation plane should be portable across Android, Oracle Cloud, AWS, OCI, and future workers. It should not be structurally coupled to OpenClaw on the Grasshopper Oracle host.

Canonical live system identifiers:

- Android edge: RDC `localhost` / `566d623e-df45-4b16-b2be-4cbd08567a49`
- Oracle control workstation: RDC `grasshopper-workstation` / `0852e6f4-2507-4d0f-9d62-f6eda8cdd169`
- AWS worker candidate: RDC `ip-172-31-8-59` / `882f1036-235b-4669-acaf-1e1135b156bd` / EC2 `i-03b6a82d46271d9cd`

Use isolated persistent browser profiles per provider/account/workspace. Keep profile data on protected runtime storage, never in Git or logs.

A common provider adapter contract should expose open, observe, find, act, verify, checkpoint, humanGate, and close. Provider-specific UI semantics stay inside adapters.

Human gates remain fail-closed: stop mutation, checkpoint, expose the live browser to the user, notify, wait, reobserve, verify completion, then resume the same loop. Never bypass CAPTCHA, MFA, biometric or security verification.

Evidence:
- architecture DESIGN
- Playwright persistent-profile capability SUPPORTED BY DOCUMENTATION
- live ChatGPT/Grok/Gemini remote profiles NOT_PROVEN
- cross-provider automation NOT_PROVEN
- remote-browser human-gate resume NOT_PROVEN
