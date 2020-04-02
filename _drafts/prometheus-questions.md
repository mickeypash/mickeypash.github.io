# Prometheus questions
- How many types of metric are available?
- What are they?
- `Counters` are monotonic. What does that mean?
- What is the suffix appended to counters? Why is it added and what happens if it already exists?
- What is the problem with using Prometheus and multi-processing?
- Where should you instantiate your metrics classes?
- When monitoring services how can they be categorised?
- Should you count queries at the start or the end of the code? Why?
- For offline processing systems why is it useful to have a heartbeat?
- What is the difference between batch jobs and offline processing?
- What is the key metric of a batch job?
- What are other useful metrics? How are they instrumented?
- When should batch jobs be converted to offline processing jobs?
- Name the various subsystems for which metrics are required?
- Which subsystem should provide instrumentation with no configuration required?

## References
- https://prometheus.io/docs/practices/instrumentation/