# Security Policy

## This repository contains intentional vulnerabilities

RedLayer is a **security demonstration**. The mock Accounts Payable Agent is deliberately
built to be exploitable so the demo can prove a layered prompt-injection attack and its
mitigation. This is by design.

- **Do not deploy this against, or connect it to, any real financial, payment, or
  production system.**
- All amounts, accounts, vendors, and approvals are **simulated**. There is no real money,
  payment rail, or exposure being measured.
- The "attacker" payloads exist only to attack the bundled mock target.

Reports that the mock target is exploitable are expected and not treated as
vulnerabilities.

## Reporting a real vulnerability

If you find a security issue in the **tooling itself** — for example, the demo harness
reaching outside its sandbox, leaking real secrets, or executing untrusted input in a way
that affects the host — please report it privately rather than opening a public issue.

Use GitHub's [private vulnerability reporting](https://github.com/joggerjoel/RedLayer/security/advisories/new)
for this repository, or contact the maintainer directly. Please include steps to reproduce
and the potential impact.
