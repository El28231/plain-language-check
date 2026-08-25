from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "plain_language_check.py"
SDK = "v0.2.16"
PROMPT = "independently assess a proposed plain-language"
ARGS = (
    "Adults applying for their first community-library membership",
    "Use common words, short sentences, direct actions, and preserve every deadline, fee, eligibility rule, and exception.",
    "Applicants are required to furnish documentary proof of residence before a library card may be issued. Cards expire after one year.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def test_consensus_gated_document_versioning(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    contract.propose_revision("Show proof that you live locally before we issue your library card. Your card expires after one year.")
    direct_vm.mock_llm(PROMPT, json.dumps({"grade": "A", "faithful": True}))
    contract.review_revision()
    state = contract.get_document()
    assert state["version"] == 2
    assert state["last_outcome"] == "ACCEPTED"
    assert contract.get_version(1).startswith("Applicants")
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_unfaithful_revision_is_rejected_without_overwrite(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    original = contract.get_document()["current_text"]
    contract.propose_revision("Bring any document and get a permanent card immediately, with no residence requirement at all.")
    direct_vm.mock_llm(PROMPT, json.dumps({"grade": "A", "faithful": False}))
    contract.review_revision()
    assert contract.get_document()["current_text"] == original
    assert contract.get_document()["last_outcome"] == "REJECTED"


def test_malformed_assessment_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.propose_revision("Show proof of local residence before we issue a card. The card expires after one year.")
    direct_vm.mock_llm(PROMPT, json.dumps({"grade": "A", "faithful": "yes"}))
    with direct_vm.expect_revert("invalid_assessment"):
        contract.review_revision()
    assert contract.get_document()["pending"] is True

