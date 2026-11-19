"""
Configuration settings for IndiGo Agent Gatekeeper (6E Guard)
MBA Assignment Configuration
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "gatekeeper.db"

# Academic & Enrolment Information (Configurable)
DEFAULT_ENROLMENT_ID = "PGD202564221"
COURSE_TITLE = "MBA in Technology Management"
PROJECT_TITLE = "Agent Gatekeeper for IndiGo Airlines"
AIRLINE_CODE = "6E"
AIRLINE_NAME = "IndiGo Airlines"

# Policy Thresholds & Defaults
DEFAULT_PRE_APPROVED_BOOKING_LIMIT = 8000.0  # ₹8,000 INR

# Standard Gatekeeper Decisions
DECISION_ALLOW = "ALLOW"
DECISION_ASK_CUSTOMER = "ASK CUSTOMER"
DECISION_BLOCK = "BLOCK"

# Supported Actions
ACTION_VIEW_FARES = "View flight fares"
ACTION_BOOK_FLIGHT = "Book a flight"
ACTION_CHANGE_BOOKING = "Change a flight booking"
ACTION_REQUEST_REFUND = "Request a refund"

ALL_ACTIONS = [
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_BOOKING,
    ACTION_REQUEST_REFUND,
]

# Action Descriptions for Display
ACTION_METADATA = {
    ACTION_VIEW_FARES: {
        "risk_level": "Low",
        "description": "Read-only access to live flight inventory, routes, and fare rules.",
        "default_rule": "ALLOW if agent is active and holds fare viewing scope."
    },
    ACTION_BOOK_FLIGHT: {
        "risk_level": "Medium - High",
        "description": "Create a new flight reservation with financial transaction.",
        "default_rule": "ALLOW if <= pre-approved limit (₹8,000); ASK CUSTOMER if > ₹8,000."
    },
    ACTION_CHANGE_BOOKING: {
        "risk_level": "High",
        "description": "Reschedule travel dates or change flight sectors for an existing PNR.",
        "default_rule": "Always ASK CUSTOMER to verify schedule and change fees."
    },
    ACTION_REQUEST_REFUND: {
        "risk_level": "Critical",
        "description": "Cancel flight booking and initiate refund processing.",
        "default_rule": "Always ASK CUSTOMER to prevent accidental/fraudulent seat release."
    }
}

# Request & Action Statuses
STATUS_EXECUTED = "EXECUTED"
STATUS_PENDING_CUSTOMER = "PENDING_CUSTOMER"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
STATUS_BLOCKED = "BLOCKED"

# Agent Statuses
AGENT_STATUS_ACTIVE = "ACTIVE"
AGENT_STATUS_SUSPENDED = "SUSPENDED"
AGENT_STATUS_REVOKED = "REVOKED"
