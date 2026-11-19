"""
Automated Verification & Test Suite for IndiGo Agent Gatekeeper (6E Guard)
Validates all MBA project rules, thresholds, and edge cases.
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

def run_all_tests():
    print("=" * 65)
    print("✈️  STARTING INDIGO AGENT GATEKEEPER VERIFICATION TEST SUITE")
    print("=" * 65)

    # 1. Initialize & Seed DB
    print("\n[Test 1] Initializing SQLite database and seeding sample data...")
    reset_database()
    seed_sample_data(force=True)
    agents = get_all_agents()
    assert len(agents) >= 5, f"Expected at least 5 seeded agents, found {len(agents)}"
    print(f"✅ DB initialized with {len(agents)} agents.")

    engine = GatekeeperEngine(booking_threshold=8000.0)

    # 2. Test Rule #1: View Fares -> ALLOW
    print("\n[Test 2] Testing Action 1: 'View flight fares'...")
    res = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_VIEW_FARES,
        customer_id="CUST-001",
        pnr="6E-10101",
        flight_details="DEL -> BOM | 6E-204",
        amount=0.0
    )
    assert res["decision"] == DECISION_ALLOW, f"Expected ALLOW, got {res['decision']}"
    assert res["status"] == STATUS_EXECUTED, f"Expected EXECUTED, got {res['status']}"
    print(f"✅ View fares passed: Verdict={res['decision']}, Status={res['status']}")

    # 3. Test Rule #2: Booking <= ₹8,000 -> ALLOW
    print("\n[Test 3] Testing Action 2: Booking <= ₹8,000 (₹4,800)...")
    res = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_BOOK_FLIGHT,
        customer_id="CUST-001",
        pnr="6E-10102",
        flight_details="DEL -> BOM | 6E-204",
        amount=4800.0
    )
    assert res["decision"] == DECISION_ALLOW, f"Expected ALLOW, got {res['decision']}"
    assert res["status"] == STATUS_EXECUTED, f"Expected EXECUTED, got {res['status']}"
    print(f"✅ Booking <= ₹8,000 passed: Verdict={res['decision']}, Status={res['status']}")

    # 4. Test Rule #3: Booking > ₹8,000 -> ASK CUSTOMER
    print("\n[Test 4] Testing Action 2: Booking > ₹8,000 (₹9,500)...")
    res = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_BOOK_FLIGHT,
        customer_id="CUST-001",
        pnr="6E-10103",
        flight_details="BOM -> GOI | 6E-802",
        amount=9500.0
    )
    assert res["decision"] == DECISION_ASK_CUSTOMER, f"Expected ASK CUSTOMER, got {res['decision']}"
    assert res["status"] == STATUS_PENDING_CUSTOMER, f"Expected PENDING_CUSTOMER, got {res['status']}"
    req_to_approve = res["request_id"]
    print(f"✅ Booking > ₹8,000 passed: Verdict={res['decision']}, Status={res['status']}")

    # 5. Test Rule #4A: Change Booking -> Mandatory ASK CUSTOMER
    print("\n[Test 5] Testing Action 3: 'Change a flight booking'...")
    res = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_CHANGE_BOOKING,
        customer_id="CUST-001",
        pnr="6E-10104",
        flight_details="Reschedule 6E-204 to evening",
        amount=1200.0
    )
    assert res["decision"] == DECISION_ASK_CUSTOMER, f"Expected ASK CUSTOMER, got {res['decision']}"
    assert res["status"] == STATUS_PENDING_CUSTOMER, f"Expected PENDING_CUSTOMER, got {res['status']}"
    print(f"✅ Flight change passed: Verdict={res['decision']}, Status={res['status']}")

    # 6. Test Rule #4B: Request Refund -> Mandatory ASK CUSTOMER
    print("\n[Test 6] Testing Action 4: 'Request a refund'...")
    res = engine.evaluate_request(
        agent_id="AGT-MMT-001",
        action=ACTION_REQUEST_REFUND,
        customer_id="CUST-001",
        pnr="6E-10105",
        flight_details="Cancel 6E-204 and refund fare",
        amount=4800.0
    )
    assert res["decision"] == DECISION_ASK_CUSTOMER, f"Expected ASK CUSTOMER, got {res['decision']}"
    assert res["status"] == STATUS_PENDING_CUSTOMER, f"Expected PENDING_CUSTOMER, got {res['status']}"
    print(f"✅ Refund request passed: Verdict={res['decision']}, Status={res['status']}")

    # 7. Test Rule #5: Revoked Agent -> Always BLOCK
    print("\n[Test 7] Testing Rule #5: Revoked agent must ALWAYS return BLOCK...")
    res_revoked = engine.evaluate_request(
        agent_id="AGT-ROG-005",  # Pre-seeded as REVOKED
        action=ACTION_VIEW_FARES,  # Even safe fare view must be blocked!
        customer_id="CUST-001",
        pnr="6E-10106",
        flight_details="DEL -> BOM",
        amount=0.0
    )
    assert res_revoked["decision"] == DECISION_BLOCK, f"Expected BLOCK, got {res_revoked['decision']}"
    assert res_revoked["status"] == STATUS_BLOCKED, f"Expected BLOCKED, got {res_revoked['status']}"
    print(f"✅ Revoked agent test passed: Verdict={res_revoked['decision']}, Reason={res_revoked['reason']}")

    # 8. Test Dynamic Revocation Kill-Switch & Timestamps
    print("\n[Test 8] Testing Dynamic Revocation Kill-Switch & Permanent Timestamps...")
    agent_before = get_agent("AGT-EXP-002")
    assert agent_before["status"] == AGENT_STATUS_ACTIVE
    assert agent_before["revoked_at"] is None

    # Trigger revocation
    update_agent_status("AGT-EXP-002", AGENT_STATUS_REVOKED, reason="Suspicious API rate limit breach")
    agent_after = get_agent("AGT-EXP-002")
    assert agent_after["status"] == AGENT_STATUS_REVOKED
    assert agent_after["revoked_at"] is not None
    print(f"✅ Agent AGT-EXP-002 revoked successfully. Revoked timestamp: {agent_after['revoked_at']}")

    # Verify requests from newly revoked agent are now BLOCKED
    res_newly_revoked = engine.evaluate_request(
        agent_id="AGT-EXP-002",
        action=ACTION_VIEW_FARES,
        customer_id="CUST-001",
        pnr="6E-10107",
        flight_details="DEL -> BOM",
        amount=0.0
    )
    assert res_newly_revoked["decision"] == DECISION_BLOCK
    print(f"✅ Newly revoked agent request instantly BLOCKED.")

    # 9. Test Customer Confirmation State Updates (Educational Simulation)
    print("\n[Test 9] Testing Human-in-the-Loop Customer Approval...")
    pending_before = get_pending_requests()
    assert any(p["request_id"] == req_to_approve for p in pending_before)

    # Approve request
    update_request_decision_by_customer(req_to_approve, "APPROVE", customer_notes="Verified via SMS OTP simulation")
    
    # Check updated request
    all_reqs = get_all_requests()
    matched = next((r for r in all_reqs if r["request_id"] == req_to_approve), None)
    assert matched is not None
    assert matched["status"] == STATUS_APPROVED
    print(f"✅ Customer confirmation passed: Request {req_to_approve} status updated to {matched['status']}")

    # 10. Verify Permanent Audit Log Entries
    print("\n[Test 10] Verifying Permanent Audit Log integrity...")
    audit_entries = get_all_audit_logs()
    assert len(audit_entries) >= 10, f"Expected at least 10 audit entries, found {len(audit_entries)}"
    print(f"✅ Permanent Audit Log contains {len(audit_entries)} immutable entries.")

    print("\n" + "=" * 65)
    print("🎉 ALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_all_tests()
