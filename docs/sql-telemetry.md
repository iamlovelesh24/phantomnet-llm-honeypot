# PhantomNet Member 3 — SQL, Context & Telemetry

## Scope

Member 3 provides the controlled synthetic SQL deception
layer, persistent context storage, and telemetry handoff
service.

## SQL Engine

Supported synthetic schemas:

- employees
- payroll
- departments
- projects
- tickets

Only read-only SELECT queries are accepted.

Destructive operations such as DROP, DELETE, UPDATE,
INSERT, ALTER, and TRUNCATE are blocked.

No real corporate or production database is contacted.

## Context Store

The context service stores synthetic generated facts by
session.

The active context window is 10 minutes / 600 seconds.

SQLite provides reliable local persistence.

ChromaDB availability is detected when installed and usable.

## Telemetry

Telemetry records include:

- session ID
- timestamp
- event type
- action/query
- response metadata
- module
- behavior indicators
- scenario
- risk level
- risk score

The persistent SQLite service exposes record_event()
and get_events() for downstream dashboard integration.

## Testing

Run:

python -m unittest discover -s tests -v

## Safety Boundary

This implementation is for authorized defensive research
and isolated demonstration environments only.

All data is synthetic.

No real employee, customer, corporate, or production
database should be connected to this component.

## SQL Contract

Member 3 exposes a controlled PostgreSQL-style mock SQL interface.
Supported operations are read-only SELECT queries against synthetic schemas.
SQL is validated before execution and unsupported or destructive statements are blocked.

## Synthetic Schemas

The mock database contains synthetic employees, payroll, departments, projects, and tickets data.
Returned rows are deterministic-looking demonstration data and must not represent real employees or customers.
No production database connection is required or permitted.

## SQL Safety Controls

Destructive SQL such as DELETE, UPDATE, DROP, ALTER, TRUNCATE, INSERT, and similar unsupported operations is rejected.
Unknown tables and columns are rejected instead of being passed through.
This boundary keeps the SQL component isolated from real corporate data.

## Context Continuity

ContextStore provides session-aware storage and retrieval of generated facts.
Retrieved facts use structured results so downstream modules can consume context consistently.
Context retention is bounded to the agreed ten-minute demonstration window.

## Session Isolation

Context records are associated with a session identifier.
Facts from one session must not leak into another session.
Session isolation is covered by the Member 3 test suite.

## Telemetry Event Contract

Telemetry records include event ID, session ID, timestamp, event type, action, scenario, risk level, risk score, and metadata.
Events are persisted through the telemetry service for downstream dashboard consumption.
The telemetry interface is designed for clean handoff to Member 4.

## Member 4 Handoff

Member 4 can consume the SQL, context, and telemetry interfaces without connecting to a real database.
The Member 3 verification suite currently covers schema discovery, SELECT queries, WHERE filtering, invalid tables, invalid columns, destructive SQL blocking, LLM request construction, ten-minute context, and session isolation.
All Member 3 test cases must pass before integration.

## SQL Contract
Member 3 exposes a controlled PostgreSQL-style mock SQL interface.
Supported operations are read-only SELECT queries against synthetic schemas.
SQL is validated before execution and unsupported or destructive statements are blocked.
