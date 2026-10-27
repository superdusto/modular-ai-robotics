# Security Policy

## Project status
Modular AI Robotics is a research-stage public repository, with no released executable mod.

## Reporting
Do not publish exploit details, credentials, private world data, or sensitive security information in public issues. Contact the repository owner through an appropriate private GitHub communication channel before disclosing sensitive findings. No dedicated private reporting address or vulnerability-disclosure mechanism has been configured yet.

## Design requirements
- Authoritative world mutation must be performed server-side by explicit validated actions.
- Robot hardware capability does not confer player authorization.
- Respect chunk claims, protected locations, server rules and optional mod protections.
- Do not interpret an unsupported permission check as permission.
- Imported knowledge files are untrusted data: no arbitrary code execution, macros, shell commands, or unsandboxed network calls.
- External AI services are optional future tooling, not runtime dependencies.
- Avoid storing secrets in repository files or published examples.
- Use bounded job retries and reconcile resource transfers after interruption/restart.

## Scope
Until code exists, this document sets design expectations rather than asserting implemented enforcement.
