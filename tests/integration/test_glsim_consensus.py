from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently assess a proposed plain-language"
ARGS = ["Adults applying for their first community-library membership", "Use common words, short sentences, direct actions, and preserve every deadline, fee, eligibility rule, and exception.", "Applicants must furnish documentary proof of residence before a library card may be issued. Cards expire after one year."]

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"grade": "A", "faithful": True})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_document_version():
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "plain_language_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed))
    proposed = contract.propose_revision(args=["Show proof that you live locally before we issue your library card. Your card expires after one year."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(proposed)
    reviewed = contract.review_revision(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(reviewed)
    assert contract.get_document(args=[]).call()["version"] == 2

