## Security

Apply these rules when touching configuration, credentials, secrets handling, runtime environment, or sensitive data paths.

### Security Rules

- Never commit secrets or credentials.
- Keep sensitive values out of version control.
- Keep required runtime variables documented in canonical configuration.
- Do not place live secret values in docs.

### Security Engineering Practices

- Apply least privilege for runtime identities and permissions.
- Validate and sanitize external inputs at trust boundaries.
- Prefer explicit allowlists over implicit trust.
- Keep dependency and supply-chain risk visible.
- Treat logs/metrics/traces as potential exfiltration paths.

### Configuration Policy

- Use one canonical runtime configuration source per repository.
- Runtime usage without that canonical source is not allowed.
- Avoid ad-hoc local environment files as runtime source of truth.
- Update config structure and docs in the same change set when keys change.

### Security Checklist

- Are secrets excluded from code/docs/artifacts?
- Are config/runtime contracts explicit and validated?
- Are permissions and access scopes minimized?
- Are errors actionable without leaking sensitive data?
- Are third-party interactions bounded by timeout/retry/input validation?

---

## End Goal

Any repository using these instructions should remain:

- production-grade for engineers
- reproducible for operators/researchers
- understandable for reviewers
- extensible for future contributors and agents
