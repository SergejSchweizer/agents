## Security

## Scope

Applies to configuration, credentials, secrets handling, runtime environment, external inputs, and sensitive data paths.

## Rules

- [MUST] Never commit secrets or credentials.
- [MUST] Keep sensitive values out of code, docs, and artifacts.
- [MUST] Document required runtime variables in canonical configuration.
- [MUST] Use one canonical runtime configuration source per repository.
- [MUST] Validate and sanitize external inputs at trust boundaries.
- [MUST] Prefer explicit allowlists over implicit trust.
- [MUST] Bound third-party calls with timeout, retry, and input validation.
- [SHOULD] Apply least privilege for runtime identities and permissions.
- [SHOULD] Treat logs, metrics, and traces as potential exfiltration paths.

## Agent Action Checklist

- Check for secrets exposure in code, docs, and logs.
- Verify config contract changes are documented in the same change set.
- Validate error messages are actionable without leaking sensitive data.
- Confirm external integrations are bounded and observable.

## Definition of Done

- No secrets exposed.
- Runtime and config contract is explicit and validated.
- Security-impacting changes include safeguards and docs updates.

## Security Checklist

- Secrets excluded from repo and docs.
- Config contract explicit.
- Access scopes minimized.
- Error handling safe and actionable.
- Third-party boundaries enforced.

## End Goal

Repositories using these instructions remain production-grade, reproducible, understandable, and extensible.
