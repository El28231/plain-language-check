from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

ARGS = ["Adults applying for their first community-library membership", "Use common words, short sentences, direct actions, and preserve every deadline, fee, eligibility rule, and exception.", "Applicants must furnish documentary proof of residence before a library card may be issued. Cards expire after one year."]

@pytest.mark.integration
def test_studionet_document_revision(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "plain_language_check.py")
    deployed = factory.deploy_contract_tx(args=ARGS, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    proposed = contract.propose_revision(args=["Show proof that you live locally before we issue your library card. Your card expires after one year."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(proposed)
    reviewed = contract.review_revision(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(reviewed)
    document = contract.get_document(args=[]).call()
    assert document["last_grade"] in ("A", "B", "C", "D")
    assert document["last_outcome"] in ("ACCEPTED", "REJECTED")
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={reviewed['hash']}")
    print(f"STUDIONET_RESULT={document['last_outcome']}")

