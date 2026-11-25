# API and Event Design Standards

Backs the `<api-design-standards>` knowledge entry, used by **design-api-event-schema**.

## REST / RPC contract

Each contract documents: **endpoint name** + HTTP method (or channel/queue); **request and response schemas** as a **code block** (JSON, Protobuf, Avro); **authentication & authorization** (OAuth2, API key, mTLS); **error handling** conventions (status codes, error body); **rate limiting, pagination, idempotency** where relevant.

The schema is the source of truth. Tables carry metadata and validation only — field, type, required, constraint. A field-description table never substitutes for the schema.

## Async events

Event schemas also document: schema versioning strategy, DLQ handling, ordering guarantees, and the partition key. Same rule: the schema is a code block; the table carries metadata.
