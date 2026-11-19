"""
Seed data generator for IndiGo Agent Gatekeeper (6E Guard)
Populates realistic demo agents, sample flights, and initial requests for MBA evaluation.
"""
from datetime import datetime, timedelta
from core.database import (
    register_agent,
    save_request,
    get_all_agents,
    update_agent_status,
    log_audit,
    get_current_timestamp,
)
from core.config import (
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_BOOKING,
    ACTION_REQUEST_REFUND,
    DECISION_ALLOW,
    DECISION_ASK_CUSTOMER,
    DECISION_BLOCK,
    STATUS_EXECUTED,
    STATUS_PENDING_CUSTOMER,
    STATUS_BLOCKED,
)

# Realistic IndiGo Flight Schedules for Demo Scenarios
SAMPLE_FLIGHTS = [
    {
        "flight_no": "6E-204",
        "route": "Delhi (DEL) -> Mumbai (BOM)",
        "dep_time": "08:30 AM",
        "arr_time": "10:45 AM",
        "fare": 4800.0,
        "class": "Economy - Saver"
    },
    {
        "flight_no": "6E-501",
        "route": "Delhi (DEL) -> Bengaluru (BLR)",
        "dep_time": "11:15 AM",
        "arr_time": "02:05 PM",
        "fare": 7200.0,
        "class": "Economy - Flexi Plus"
    },
    {
        "flight_no": "6E-802",
        "route": "Mumbai (BOM) -> Goa (GOI)",
        "dep_time": "04:45 PM",
        "arr_time": "05:55 PM",
        "fare": 9500.0,  # Exceeds ₹8,000 threshold to demonstrate ASK CUSTOMER
        "class": "Economy - Super 6E"
    },
    {
        "flight_no": "6E-103",
        "route": "Bengaluru (BLR) -> Hyderabad (HYD)",
        "dep_time": "07:10 PM",
        "arr_time": "08:20 PM",
        "fare": 3400.0,
        "class": "Economy - Saver"
    },
    {
        "flight_no": "6E-990",
        "route": "Kolkata (CCU) -> Chennai (MAA)",
        "dep_time": "09:00 AM",
        "arr_time": "11:30 AM",
        "fare": 6100.0,
        "class": "Economy - Standard"
    }
]

def seed_sample_data(force: bool = False):
    """
    Seeds initial agents and sample transactions if database is fresh.
    Ensures MBA grading demonstrations have rich data immediately on startup.
    """
    existing_agents = get_all_agents()
    if existing_agents and not force:
        return

    now = datetime.now()
    two_days_ago = (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    five_days_ago = (now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    one_day_ago = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    # 1. Register Verified Commercial Agents
    register_agent(
        agent_id="AGT-MMT-001",
        name="MakeMyTrip Autonomous Booker",
        developer="MakeMyTrip India Pvt Ltd",
        can_view_fares=True,
        can_book=True,
        can_change_booking=True,
        can_request_refund=True,
        custom_spending_limit=8000.0,
        status=AGENT_STATUS_ACTIVE,
        registered_at=five_days_ago
    )

    register_agent(
        agent_id="AGT-EXP-002",
        name="Expedia Travel Assistant",
        developer="Expedia Group Global",
        can_view_fares=True,
        can_book=True,
        can_change_booking=True,
        can_request_refund=False,  # Intentionally missing refund scope for demo
        custom_spending_limit=8000.0,
        status=AGENT_STATUS_ACTIVE,
        registered_at=five_days_ago
    )

    register_agent(
        agent_id="AGT-GEM-003",
        name="Personal Gemini Travel Agent",
        developer="Google Assistant / Gemini Ecosystem",
        can_view_fares=True,
        can_book=True,
        can_change_booking=True,
        can_request_refund=True,
        custom_spending_limit=12000.0,
        status=AGENT_STATUS_ACTIVE,
        registered_at=two_days_ago
    )

    register_agent(
        agent_id="AGT-CORP-004",
        name="TCS Corporate Travel Agent",
        developer="Tata Consultancy Services Ltd",
        can_view_fares=True,
        can_book=True,
        can_change_booking=True,
        can_request_refund=True,
        custom_spending_limit=15000.0,
        status=AGENT_STATUS_ACTIVE,
        registered_at=five_days_ago
    )

    # 2. Register a REVOKED Agent (Demonstrating Strict Rule #5)
    register_agent(
        agent_id="AGT-ROG-005",
        name="ScraperBot BlackHat AI",
        developer="Untrusted Anonymous Dev",
        can_view_fares=True,
        can_book=True,
        can_change_booking=False,
        can_request_refund=False,
        custom_spending_limit=0.0,
        status=AGENT_STATUS_REVOKED,
        registered_at=five_days_ago
    )
    # Ensure revoked_at is explicitly logged in the past
    update_agent_status(
        agent_id="AGT-ROG-005",
        new_status=AGENT_STATUS_REVOKED,
        reason="Detected automated rate abuse and scraping violation"
    )

    # 3. Pre-seed Historical Requests to demonstrate all 3 Verdicts in Tab 4

    # (A) Auto-Allowed Fare View
    save_request(
        request_id="REQ-6E-INIT01",
        agent_id="AGT-MMT-001",
        customer_id="CUST-6E-101",
        pnr="6E-P9A4X",
        action=ACTION_VIEW_FARES,
        flight_details="DEL -> BOM | Flight 6E-204",
        amount=0.0,
        gatekeeper_decision=DECISION_ALLOW,
        status=STATUS_EXECUTED,
        reason="Read-Only Query: Low-risk information retrieval. Auto-approved by Gatekeeper policy."
    )

    # (B) Auto-Allowed Booking below ₹8,000 limit
    save_request(
        request_id="REQ-6E-INIT02",
        agent_id="AGT-MMT-001",
        customer_id="CUST-6E-101",
        pnr="6E-K2L8M",
        action=ACTION_BOOK_FLIGHT,
        flight_details="DEL -> BLR | Flight 6E-501 (Fare: ₹7,200.00)",
        amount=7200.0,
        gatekeeper_decision=DECISION_ALLOW,
        status=STATUS_EXECUTED,
        reason="Booking value of ₹7,200.00 is within the pre-approved limit of ₹8,000.00. Auto-authorized."
    )

    # (C) Pre-seed a Pending Request (> ₹8,000) for Tab 2 Customer Confirmation Demo!
    save_request(
        request_id="REQ-6E-INIT03",
        agent_id="AGT-GEM-003",
        customer_id="CUST-6E-202",
        pnr="6E-H7Y1Q",
        action=ACTION_BOOK_FLIGHT,
        flight_details="BOM -> GOI | Flight 6E-802 (Fare: ₹9,500.00)",
        amount=9500.0,
        gatekeeper_decision=DECISION_ASK_CUSTOMER,
        status=STATUS_PENDING_CUSTOMER,
        reason="Booking value of ₹9,500.00 EXCEEDS the pre-approved limit of ₹8,000.00. Sent to Customer Confirmation Portal."
    )

    # (D) Pre-seed a Pending Flight Change for Tab 2
    save_request(
        request_id="REQ-6E-INIT04",
        agent_id="AGT-EXP-002",
        customer_id="CUST-6E-303",
        pnr="6E-T5R8V",
        action=ACTION_CHANGE_BOOKING,
        flight_details="Reschedule 6E-103 BLR->HYD to evening departure (Change fee: ₹1,500.00)",
        amount=1500.0,
        gatekeeper_decision=DECISION_ASK_CUSTOMER,
        status=STATUS_PENDING_CUSTOMER,
        reason="Policy Requirement: Every flight schedule modification requires passenger consent."
    )

    # (E) Pre-seed a BLOCKED request from Revoked Agent
    save_request(
        request_id="REQ-6E-INIT05",
        agent_id="AGT-ROG-005",
        customer_id="CUST-6E-999",
        pnr="6E-FAKE1",
        action=ACTION_VIEW_FARES,
        flight_details="DEL -> BOM | Flight 6E-204",
        amount=0.0,
        gatekeeper_decision=DECISION_BLOCK,
        status=STATUS_BLOCKED,
        reason="Security Lockdown: Agent 'ScraperBot BlackHat AI' (AGT-ROG-005) access was REVOKED. All incoming requests are strictly BLOCKED."
    )
