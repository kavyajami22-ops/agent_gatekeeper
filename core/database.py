"""
Database management for IndiGo Agent Gatekeeper (6E Guard)
Uses Python standard library sqlite3 for persistent, zero-dependency storage.
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.config import (
    DB_PATH,
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
    STATUS_PENDING_CUSTOMER,
    STATUS_EXECUTED,
    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_BLOCKED,
    DEFAULT_PRE_APPROVED_BOOKING_LIMIT,
)

def get_current_timestamp() -> str:
    """Returns current ISO-8601 formatted timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_connection() -> sqlite3.Connection:
    """Creates a connection with Row row_factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite schema for agents, requests, and permanent audit logs."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Agents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        agent_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        developer TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('ACTIVE', 'SUSPENDED', 'REVOKED')),
        can_view_fares INTEGER NOT NULL DEFAULT 1,
        can_book INTEGER NOT NULL DEFAULT 1,
        can_change_booking INTEGER NOT NULL DEFAULT 1,
        can_request_refund INTEGER NOT NULL DEFAULT 1,
        custom_spending_limit REAL DEFAULT 8000.0,
        registered_at TEXT NOT NULL,
        revoked_at TEXT
    )
    """)

    # 2. Simulated Requests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        request_id TEXT PRIMARY KEY,
        agent_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        pnr TEXT NOT NULL,
        action TEXT NOT NULL,
        flight_details TEXT NOT NULL,
        amount REAL NOT NULL DEFAULT 0.0,
        gatekeeper_decision TEXT NOT NULL,
        status TEXT NOT NULL,
        reason TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
    )
    """)

    # 3. Permanent Immutable Audit Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        request_id TEXT,
        agent_id TEXT,
        action TEXT,
        event_type TEXT NOT NULL,
        decision TEXT,
        status TEXT,
        notes TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# -------------------------------------------------------------
# Agent Management Functions
# -------------------------------------------------------------

def register_agent(
    agent_id: str,
    name: str,
    developer: str,
    can_view_fares: bool = True,
    can_book: bool = True,
    can_change_booking: bool = True,
    can_request_refund: bool = True,
    custom_spending_limit: float = DEFAULT_PRE_APPROVED_BOOKING_LIMIT,
    status: str = AGENT_STATUS_ACTIVE,
    registered_at: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a new external AI agent with permanent registration timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    ts = registered_at or get_current_timestamp()
    revoked_ts = ts if status == AGENT_STATUS_REVOKED else None

    cursor.execute("""
    INSERT OR REPLACE INTO agents (
        agent_id, name, developer, status,
        can_view_fares, can_book, can_change_booking, can_request_refund,
        custom_spending_limit, registered_at, revoked_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        agent_id, name, developer, status,
        int(can_view_fares), int(can_book), int(can_change_booking), int(can_request_refund),
        custom_spending_limit, ts, revoked_ts
    ))

    # Log registration in permanent audit trail
    log_audit(
        conn=conn,
        agent_id=agent_id,
        event_type="AGENT_REGISTERED",
        notes=f"Agent '{name}' ({agent_id}) registered with status '{status}' by developer '{developer}'."
    )

    conn.commit()
    conn.close()
    return get_agent(agent_id)

def update_agent_status(agent_id: str, new_status: str, reason: str = "") -> bool:
    """
    Updates an agent's status.
    If status is set to REVOKED, permanently timestamps 'revoked_at'.
    If reactivated, clears revoked_at.
    """
    conn = get_connection()
    cursor = conn.cursor()
    ts = get_current_timestamp()

    if new_status == AGENT_STATUS_REVOKED:
        cursor.execute("""
        UPDATE agents
        SET status = ?, revoked_at = ?
        WHERE agent_id = ?
        """, (new_status, ts, agent_id))
        event = "AGENT_REVOKED"
        note = f"Agent {agent_id} REVOKED at {ts}. Reason: {reason or 'Administrative revocation'}"
    else:
        cursor.execute("""
        UPDATE agents
        SET status = ?, revoked_at = NULL
        WHERE agent_id = ?
        """, (new_status, agent_id))
        event = "AGENT_STATUS_UPDATED"
        note = f"Agent {agent_id} status changed to {new_status} at {ts}."

    log_audit(
        conn=conn,
        agent_id=agent_id,
        event_type=event,
        notes=note
    )

    conn.commit()
    conn.close()
    return True

def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves an agent by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_agents() -> List[Dict[str, Any]]:
    """Retrieves all agents ordered by registered_at desc."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agents ORDER BY registered_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# -------------------------------------------------------------
# Request & Audit Logging Functions
# -------------------------------------------------------------

def log_audit(
    conn: Optional[sqlite3.Connection] = None,
    request_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    action: Optional[str] = None,
    event_type: str = "SYSTEM_EVENT",
    decision: Optional[str] = None,
    status: Optional[str] = None,
    notes: str = ""
):
    """Appends an immutable entry to the permanent audit log."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    ts = get_current_timestamp()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO audit_log (
        timestamp, request_id, agent_id, action, event_type, decision, status, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, request_id, agent_id, action, event_type, decision, status, notes))

    if close_at_end:
        conn.commit()
        conn.close()

def save_request(
    request_id: str,
    agent_id: str,
    customer_id: str,
    pnr: str,
    action: str,
    flight_details: str,
    amount: float,
    gatekeeper_decision: str,
    status: str,
    reason: str
):
    """Saves a new request and creates its initial audit log entry."""
    conn = get_connection()
    cursor = conn.cursor()
    ts = get_current_timestamp()

    cursor.execute("""
    INSERT INTO requests (
        request_id, agent_id, customer_id, pnr, action, flight_details,
        amount, gatekeeper_decision, status, reason, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request_id, agent_id, customer_id, pnr, action, flight_details,
        amount, gatekeeper_decision, status, reason, ts, ts
    ))

    # Permanent audit log entry
    log_audit(
        conn=conn,
        request_id=request_id,
        agent_id=agent_id,
        action=action,
        event_type="REQUEST_INTERCEPTED",
        decision=gatekeeper_decision,
        status=status,
        notes=f"Decision: {gatekeeper_decision}. Initial status: {status}. Rationale: {reason}"
    )

    conn.commit()
    conn.close()

def update_request_decision_by_customer(
    request_id: str,
    customer_action: str,  # 'APPROVE' or 'REJECT'
    customer_notes: str = ""
) -> bool:
    """
    Handles customer confirmation for a pending request.
    Pure educational simulation: Never touches real bank accounts or airlines.
    Updates simulated request status to APPROVED or REJECTED.
    """
    conn = get_connection()
    cursor = conn.cursor()
    ts = get_current_timestamp()

    new_status = STATUS_APPROVED if customer_action.upper() == "APPROVE" else STATUS_REJECTED
    cursor.execute("""
    UPDATE requests
    SET status = ?, updated_at = ?
    WHERE request_id = ?
    """, (new_status, ts, request_id))

    # Fetch request details for audit logging
    cursor.execute("SELECT * FROM requests WHERE request_id = ?", (request_id,))
    req = cursor.fetchone()

    event = "CUSTOMER_APPROVED" if new_status == STATUS_APPROVED else "CUSTOMER_REJECTED"
    log_audit(
        conn=conn,
        request_id=request_id,
        agent_id=req["agent_id"] if req else None,
        action=req["action"] if req else None,
        event_type=event,
        decision="ASK CUSTOMER -> RESOLVED",
        status=new_status,
        notes=f"Customer {customer_action.upper()}ed request for PNR {req['pnr'] if req else 'N/A'}. {customer_notes} (Educational simulation state update)."
    )

    conn.commit()
    conn.close()
    return True

def get_pending_requests() -> List[Dict[str, Any]]:
    """Fetches all requests that are currently in PENDING_CUSTOMER status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT r.*, a.name as agent_name, a.developer as agent_developer
    FROM requests r
    LEFT JOIN agents a ON r.agent_id = a.agent_id
    WHERE r.status = ?
    ORDER BY r.created_at DESC
    """, (STATUS_PENDING_CUSTOMER,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_requests() -> List[Dict[str, Any]]:
    """Fetches all historical requests."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT r.*, a.name as agent_name
    FROM requests r
    LEFT JOIN agents a ON r.agent_id = a.agent_id
    ORDER BY r.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_audit_logs() -> List[Dict[str, Any]]:
    """Fetches all permanent audit log entries in reverse chronological order."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM audit_log ORDER BY log_id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def reset_database():
    """Drops and re-creates tables (used for testing or clean restarts)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS audit_log")
    cursor.execute("DROP TABLE IF EXISTS requests")
    cursor.execute("DROP TABLE IF EXISTS agents")
    conn.commit()
    conn.close()
    init_db()
