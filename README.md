# Plain Language Check

Maintains a document version history and accepts a proposed plain-language revision only when consensus finds it clear and faithful.

## Core workflow

- The owner stores an audience, clarity standard, and initial document.
- Any caller may propose one pending revision.
- Validators grade clarity A through D and separately decide whether material meaning is preserved.
- Only a faithful A or B revision becomes the next immutable document version.

## Reuse model

One deployment represents one evolving document and retains every accepted version. Rejected proposals never overwrite the current text.

## Why GenLayer

Clarity for an audience and faithful preservation of meaning are semantic judgments. GenLayer consensus gates the version transition while deterministic storage preserves history.

## Evidence and source boundary

The audience, clarity standard, current document, and proposed revision are the entire evidence set. No dictionary, law, or outside style guide is silently added.

## Safety boundary

It cannot prove legal equivalence, accessibility compliance, or that the document is suitable for every reader. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/plain_language_check.py
genvm-lint typecheck contracts/plain_language_check.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. Live StudioNet testing is opt-in and uses dedicated owner-specific keys outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority and collection limits
- AUDIT.md: review-readiness checks and residual limitations
