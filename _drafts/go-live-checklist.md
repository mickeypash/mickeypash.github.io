# Go-live checklist for Production services

Software Architecture Documentation
Architectural overview in engineering docs
Link to components

CI/CD
Ensure all code is in a pipeline
Pipelines should automate the following:
Build a docker image
Lint the dockerfile
Lint the code
Test the code (unit + integration)
Release the docker image
Deploy to environments
Document the release process in the readme of each project


Disaster recovery
Document the DR plan
Play out the scenario
Test a restore and document it
Replay events through the system


Pre mortem
Figure out what happens when the system is impaired, loaded, or degraded, and how to remediate/circumvent issues. Outcome is to perform a Game day in which you simulate and document failure cases, and write playbooks, or update system to handle failure scenarios, improve observability.

Observability
Ensure SLOs are monitored and alerted on via alertmanager
The components log out relevant info in a sensible manner
Dashboards are present to illustrate our SLOs and KPIs

Rollout plan
Formulate and document a rollout plan
Brief overview
Route certain accounts to the snowflake ingestion pipeline
Backfill data for those accounts
Route all traffic and backfill all data.

Capacity planning
Run a load test to simulate production traffic
Simulate black friday load/projected peak load in 2 years time
Monitor SLOs when loadtesting

Security
Scan all app dependencies & docker images
Manage users, roles and permissions in a scalable way in snowflake
Segregate data for different account appropriately
Ensure all data in S3 is encrypted
Ensure it is GDPR compliant

Testing
Sufficient unit and integration test coverage
Tbc
Measure it somehow
Continuous e2e test running and alerted on




### Refs
https://jbd.dev/prod-readiness/
https://srcco.de/posts/web-service-on-kubernetes-production-checklist-2019.html
https://vorozhko.net/prepare-application-launch-checklist
https://landing.google.com/sre/sre-book/chapters/launch-checklist/
https://landing.google.com/sre/sre-book/chapters/reliable-product-launches/