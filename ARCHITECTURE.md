# Architecture

## Responsibility boundary

The application may collect inputs and display state. PlainLanguageCheck owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

No pending proposal -> pending proposal -> ACCEPTED new version or REJECTED unchanged version.

## Storage model

The contract stores owner, audience, clarity standard, current text, accepted version history, pending proposal/author, version number, and last assessment. Text is normalized and field-length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed output fail closed.

## Authorization and invariants

Anyone may propose when no proposal is pending. Review is permissionless. Only consensus can replace the current document.

## Reuse and distinctness

One deployment represents one evolving document and retains every accepted version. Rejected proposals never overwrite the current text.

This is consensus-gated document version control with faithfulness protection, not translation acceptance or a one-time readability score.
