# IndiGo Airlines Agent Gatekeeper — Business Governance Rules
**System:** IndiGo Airlines — Agent Gatekeeper (6E Guard)  
**Student Enrolment ID:** `PGD202564221` (Configurable Identifier)  
**Governance Scope:** Inbound Autonomous AI Agent Request Policy Matrix  
**Simulation Notice:** Educational simulation only; no real financial or reservation systems are touched.

---

### 1. The Tri-State Decision Model

Every request dispatched by an external AI agent is evaluated by the Gatekeeper and assigned one of three deterministic verdicts:
* 🟢 **`ALLOW`**: Safe, low-risk, or pre-authorized actions execute automatically without passenger friction.
* 🟡 **`ASK CUSTOMER`**: High-value, disruptive, or irreversible actions are held in a pending state until explicit passenger approval is received.
* 🔴 **`BLOCK`**: Invalid, unauthorized, out-of-scope, or revoked agent attempts are immediately rejected at the perimeter.

---

### 2. Core Business Rules & Policy Thresholds

#### Rule 1: Agent Registration & Permission Scopes
* External AI agents must be formally onboarded into the Agent Directory with an assigned `Agent ID`, `Agent Name`, `Developer Organization`, and initial status (`ACTIVE`).
* Permissions are granularly assigned across four discrete action scopes:
  1. `can_view_fares` (View flight fares)
  2. `can_book` (Book a flight)
  3. `can_change_booking` (Change a flight booking)
  4. `can_request_refund` (Request a refund)
* If an active agent attempts an action without holding the specific scope, the Gatekeeper returns **`BLOCK`** (`Permission Denied: Missing Scope`).

#### Rule 2: Booking Value Threshold Policy (Initial Limit: ₹8,000)
* **Bookings $\le$ ₹8,000:** Automatically evaluate to **`ALLOW`**, provided the agent is `ACTIVE` and holds `can_book` permission. The transaction is marked `EXECUTED` immediately.
* **Bookings $>$ ₹8,000:** Financial exposure exceeds the pre-approved baseline. The Gatekeeper strictly returns **`ASK CUSTOMER`**, moving the transaction to `PENDING_CUSTOMER` status for passenger sign-off.
* *Note:* The ₹8,000 threshold is configurable via `core/config.py` and the UI settings panel.

#### Rule 3: Mandatory Customer Confirmation for Flight Modifications
* **Every flight change request** strictly returns **`ASK CUSTOMER`**, regardless of transaction amount or fee waiver.
* *Rationale:* Flight changes alter passenger itineraries, risk missed connections, and may trigger change fees. Autonomous execution is prohibited without human review.

#### Rule 4: Mandatory Customer Confirmation for Ticket Refunds
* **Every refund request** strictly returns **`ASK CUSTOMER`**, regardless of refund value.
* *Rationale:* Ticket refunds permanently cancel allocated seat inventory and initiate financial disbursements. To prevent accidental or malicious seat cancellations, explicit passenger consent is mandatory.

#### Rule 5: Absolute Lockdown for Revoked Agents
* Any agent with status **`REVOKED`** (or `SUSPENDED`) immediately returns **`BLOCK`** for **all four actions** (including read-only fare inquiries) with zero exceptions.
* Invoking the administrative Kill-Switch permanently records an ISO-8601 timestamp in `revoked_at`. Subsequent attempts remain strictly blocked until explicitly reactivated.

#### Rule 6: Permanent Audit Trail & Timestamping
* All incoming requests, policy decisions, customer confirmations (`APPROVED` / `REJECTED`), and administrative status changes are permanently recorded in the SQLite `audit_log` ledger with immutable timestamps.
