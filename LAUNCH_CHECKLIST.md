Launch Checklist — Nexora Suite

Pre-launch
- [ ] Finalize production secrets (`NEXORA_HOME_SECRET`, `JWT_SECRET`, `DATABASE_URL`).
- [ ] Build frontend assets and verify they are accessible under `/module/<name>/`.
- [ ] Run full automated test suite and E2E user flows.
- [ ] Run a security scan (dependencies and basic SAST).
- [ ] Configure TLS and DNS.

Configuration
- [ ] Configure process manager (systemd/supervisor) with auto-restart.
- [ ] Configure Nginx reverse proxy and health check endpoint.
- [ ] Configure log rotation and monitoring (Sentry/Prometheus).

Data & Backups
- [ ] Ensure DB backups are scheduled and tested.
- [ ] Ensure media/static backups and CDN invalidation plan.

Operational
- [ ] Run smoke tests: register/login/dashboard/module open for 5 sample modules.
- [ ] Validate user sessions and concurrent module usage.
- [ ] Ensure rate-limits and abuse protections.

Launch
- [ ] Switch DNS to new deployment.
- [ ] Monitor logs and metrics for first 24 hours.
- [ ] Keep rollback plan and previous release available.

Post-launch
- [ ] Run post-deploy regression tests.
- [ ] Confirm backups, monitoring, and alerting are successful.
- [ ] Communicate release notes to stakeholders.

Optional
- [ ] Configure auto-scaling (K8s/HPA) and horizontal DB scaling if needed.
