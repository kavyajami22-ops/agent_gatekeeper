"""
Automated Verification & Test Suite for IndiGo Agent Gatekeeper (6E Guard)
Validates the six required MBA project test scenarios.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.database import (
    init_db,
    reset_database,
    get_all_agents,
    get_agent,
    update_agent_status,
    register_agent,
    get_pending_requests,
    get_all_audit_logs,
    update_request_decision_by_customer,
    get_all_requests,
)
from core.seed_data import seed_sample_data
from core.gatekeeper import GatekeeperEngine
from core.config import (
    DECISION_ALLOW,
    DECISION_ASK_CUSTOMER,
    DECISION_BLOCK,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_BOOKING,
    ACTION_REQUEST_REFUND,
    STATUS_EXECUTED,
    STATUS_PENDING_CUSTOMER,
    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_BLOCKED,
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
)

def run_tests():
    print("=" * 70)
    print("✈️  INDIGO AIRLINES AGENT GATEKEEPER — AUTOMATED VERIFICATION TEST SUITE")
    print("=" * 70)

    # Initialize fresh database and seed data
    reset_database()
    seed_sample_data(force=True)
    engine = GatekeeperEngine(booking_threshold=8000.0)

    test_results = []

    # -------------------------------------------------------------------------
    # Scenario 1: Registered agent with read-only permission
    # -------------------------------------------------------------------------
    print("\n[Scenario 1] Testing registered agent with read-only permission...")
    # Register an agent with ONLY read-only scope (can_view_fares=True, all others False)
    register_agent(
        agent_id="AGT-READONLY-01",
        name="Skyscanner Fare Explorer",
        developer="Skyscanner Ltd",
        can_view_fares=True,
        can_book=False,
        can_change_booking=False,
        can_request_refund=False,
        custom_spending_limit=8000.0,
        status=AGENT_STATUS_ACTIVE
    )
    # 1A: Reading fares should be ALLOWED
    res_read = engine.evaluate_request(
        agent_id="AGT-READONLY-01",
        action=ACTION_VIEW_FARES,
        customer_id="CUST-6E-101",
        pnr="6E-R001",
        flight_details="DEL -> BOM | 6E-204",
        amount=0.0
    )
    # 1B: Attempting a booking without booking scope should be BLOCKED
    res_nobook = engine.evaluate_request(
        agent_id="AGT-READONLY-01",
        action=ACTION_BOOK_FLIGHT,
        customer_id="CUST-6E-101",
        pnr="6E-R002",
        flight_details="DEL -> BOM | 6E-204",
        amount=4500.0
    )

    s1_pass = (
        res_read["decision"] == DECISION_ALLOW and 
        res_read["status"] == STATUS_EXECUTED and
        res_nobook["decision"] == DECISION_BLOCK and
        res_nobook["status"] == STATUS_BLOCKED
    )
    test_results.append(("Scenario 1: Registered Agent with Read-Only Permission", "PASS" if s1_pass else "FAIL", 
                         f"Fare View: {res_read['decision']} | Booking without scope: {res_nobook['decision']}"))
    print(f"  -> Fare View Verdict: {res_read['decision']} (Status: {res_read['status']})")
    print(f"  -> Unauthorized Booking Verdict: {res_nobook['decision']} (Status: {res_nobook['status']})")
    print(f"  -> Result: {'PASS' if s1_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Scenario 2: Unknown or unregistered agent
    # -------------------------------------------------------------------------
    print("\n[Scenario 2] Testing unknown / unregistered agent...")
    res_unknown = engine.evaluate_request(
        agent_id="AGT-UNKNOWN-999",
        action=ACTION_VIEW_FARES,
        customer_id="CUST-6E-999",
        pnr="6E-X999",
        flight_details="DEL -> BLR | 6E-501",
        amount=0.0
    )
    s2_pass = (
        res_unknown["decision"] == DECISION_BLOCK and 
        res_unknown["status"] == STATUS_BLOCKED and
        "not registered" in res_unknown["reason"].lower()
    )
    test_results.append(("Scenario 2: Unknown / Unregistered Agent", "PASS" if s2_pass else "FAIL", 
                         f"Verdict: {res_unknown['decision']} | Reason: {res_unknown['reason']}"))
    print(f"  -> Verdict: {res_unknown['decision']} (Status: {res_unknown['status']})")
    print(f"  -> Reason: {res_unknown['reason']}")
    print(f"  -> Result: {'PASS' if s2_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Scenario 3: Booking above ₹8,000 threshold
    # -------------------------------------------------------------------------
    print("\n[Scenario 3] Testing booking above ₹8,000 threshold (₹9,500)...")
    res_above = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_BOOK_FLIGHT,
        customer_id="CUST-6E-202",
        pnr="6E-H7Y1Q",
        flight_details="BOM -> GOI | Flight 6E-802 (Fare: ₹9,500.00)",
        amount=9500.0
    )
    s3_pass = (
        res_above["decision"] == DECISION_ASK_CUSTOMER and 
        res_above["status"] == STATUS_PENDING_CUSTOMER
    )
    test_results.append(("Scenario 3: Booking Above ₹8,000 (₹9,500)", "PASS" if s3_pass else "FAIL", 
                         f"Verdict: {res_above['decision']} | Status: {res_above['status']}"))
    print(f"  -> Verdict: {res_above['decision']} (Status: {res_above['status']})")
    print(f"  -> Reason: {res_above['reason']}")
    print(f"  -> Result: {'PASS' if s3_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Scenario 4: Booking below ₹8,000 threshold
    # -------------------------------------------------------------------------
    print("\n[Scenario 4] Testing booking below ₹8,000 threshold (₹4,800)...")
    res_below = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_BOOK_FLIGHT,
        customer_id="CUST-6E-101",
        pnr="6E-K2L8M",
        flight_details="DEL -> BOM | Flight 6E-204 (Fare: ₹4,800.00)",
        amount=4800.0
    )
    s4_pass = (
        res_below["decision"] == DECISION_ALLOW and 
        res_below["status"] == STATUS_EXECUTED
    )
    test_results.append(("Scenario 4: Booking Below ₹8,000 (₹4,800)", "PASS" if s4_pass else "FAIL", 
                         f"Verdict: {res_below['decision']} | Status: {res_below['status']}"))
    print(f"  -> Verdict: {res_below['decision']} (Status: {res_below['status']})")
    print(f"  -> Reason: {res_below['reason']}")
    print(f"  -> Result: {'PASS' if s4_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Scenario 5: Revoked agent making a request
    # -------------------------------------------------------------------------
    print("\n[Scenario 5] Testing revoked agent making a request...")
    res_revoked = engine.evaluate_request(
        agent_id="AGT-ROG-005",  # Pre-seeded as REVOKED
        action=ACTION_VIEW_FARES,  # Even read-only request must be blocked
        customer_id="CUST-6E-555",
        pnr="6E-REV01",
        flight_details="DEL -> BOM | 6E-204",
        amount=0.0
    )
    s5_pass = (
        res_revoked["decision"] == DECISION_BLOCK and 
        res_revoked["status"] == STATUS_BLOCKED and
        "revoked" in res_revoked["reason"].lower()
    )
    test_results.append(("Scenario 5: Revoked Agent Attempt", "PASS" if s5_pass else "FAIL", 
                         f"Verdict: {res_revoked['decision']} | Reason: {res_revoked['reason']}"))
    print(f"  -> Verdict: {res_revoked['decision']} (Status: {res_revoked['status']})")
    print(f"  -> Reason: {res_revoked['reason']}")
    print(f"  -> Result: {'PASS' if s5_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Scenario 6: Custom Scenario — Mandatory Refund Request & Customer Approval
    # -------------------------------------------------------------------------
    print("\n[Scenario 6] Testing Custom Scenario: Mandatory Refund Request & Customer Sign-Off...")
    # Step A: Inbound refund request must return ASK CUSTOMER
    res_refund = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_REQUEST_REFUND,
        customer_id="CUST-6E-777",
        pnr="6E-REF88",
        flight_details="Cancel 6E-501 DEL->BLR and process ₹7,200.00 refund",
        amount=7200.0
    )
    refund_req_id = res_refund["request_id"]
    is_asked = (res_refund["decision"] == DECISION_ASK_CUSTOMER and 
                res_refund["status"] == STATUS_PENDING_CUSTOMER)

    # Step B: Customer confirms via portal; simulated status updates to APPROVED
    update_request_decision_by_customer(refund_req_id, "APPROVE", customer_notes="Customer confirmed cancellation via OTP simulation")
    all_reqs = get_all_requests()
    matched = next((r for r in all_reqs if r["request_id"] == refund_req_id), None)
    is_approved = matched is not None and matched["status"] == STATUS_APPROVED

    s6_pass = is_asked and is_approved
    test_results.append(("Scenario 6: Custom — Mandatory Refund & Customer Sign-Off", "PASS" if s6_pass else "FAIL", 
                         f"Initial: {res_refund['decision']} ({res_refund['status']}) -> After Customer Approval: {matched['status'] if matched else 'N/A'}"))
    print(f"  -> Initial Gatekeeper Verdict: {res_refund['decision']} (Status: {res_refund['status']})")
    print(f"  -> Post-Approval Status: {matched['status'] if matched else 'N/A'}")
    print(f"  -> Result: {'PASS' if s6_pass else 'FAIL'}")

    # -------------------------------------------------------------------------
    # Summary Report
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("📊 SUMMARY TEST REPORT — ALL SIX SCENARIOS")
    print("=" * 70)
    all_passed = True
    for name, result, details in test_results:
        symbol = "✅" if result == "PASS" else "❌"
        print(f"{symbol} [{result}] {name}")
        print(f"    Details: {details}")
        if result != "PASS":
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("🎉 ALL SIX REQUIRED TEST SCENARIOS PASSED SUCCESSFULLY!")
    else:
        print("⚠️ SOME TESTS FAILED. PLEASE REVIEW LOGS ABOVE.")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
