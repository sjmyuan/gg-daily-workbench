# API and Event Design Standards

Backs the `<api-design-standards>` knowledge entry, used by **design-api-event-schema**.

## REST / RPC contract

Each contract documents: **endpoint name** + HTTP method (or channel/queue); **request/response schema** (JSON, Protobuf, Avro); **authentication & authorization** (OAuth2, API key, mTLS); **error handling** conventions (status codes, error body); **rate limiting, pagination, idempotency** where relevant.

## Async events

Event schemas also document: schema versioning strategy, DLQ handling, and ordering guarantees.
