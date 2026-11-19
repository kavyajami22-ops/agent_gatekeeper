# IndiGo Airlines Agent Gatekeeper — Business Governance Rules
**System:** IndiGo Airlines — Agent Gatekeeper (6E Guard)  
**Student Enrolment ID:** `PGD202564221` (Configurable Identifier)  
**Governance Scope:** Inbound Autonomous AI Agent Request Policy Matrix  
**Simulation Notice:** Educational simulation only; no real financial or reservation systems are touched.

---

### 1. The Tri-State Decision Model

Every inbound API request dispatched by an external AI agent is intercepted by the Gatekeeper and assigned one of three deterministic verdicts:
* 🟢 **`ALLOW`**: Safe, low-risk, or pre-authorized actions execute automatically without passenger friction.
* 🟡 **`ASK CUSTOMER`**: High-value, disruptive, or irreversible actions are placed in a holding state awaiting explicit human approval.
* 🔴 **`BLOCK`**: Invalid, out-of-scope, unregistered, or revoked agent attempts are denied immediately at the perimeter.

---

### 2. Master Policy Decision Table (The Six Core Scenarios)

The table below defines the deterministic decision matrix enforced by the Gatekeeper engine across all operating conditions:

| # | Test Scenario Description | Agent Directory Status | Action & Parameters | Gatekeeper Verdict | Resulting Request State | Policy Rationale |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | **Registered Active Agent Viewing Flight Fares** | `ACTIVE` (with `can_view_fares`) | Action: *View flight fares* (Read-only query, ₹0) | 🟢 **`ALLOW`** | `EXECUTED` | Safe informational retrieval. Auto-authorized without customer friction. |
| **2** | **Unknown or Unregistered Agent** | **Not Registered** in Directory | Any Action (Fare view, booking, change, refund) | 🔴 **`BLOCK`** | `BLOCKED` | Zero-Trust Perimeter Rule: Unknown agent identity cannot be verified or audited. |
| **3** | **Booking Amount Above ₹8,000 Threshold** | `ACTIVE` (with `can_book`) | Action: *Book a flight* (Transaction Amount $>$ ₹8,000) | 🟡 **`ASK CUSTOMER`** | `PENDING_CUSTOMER` | High financial exposure exceeds the pre-approved baseline. Requires explicit passenger consent. |
| **4** | **Booking Amount At or Below ₹8,000 Threshold** | `ACTIVE` (with `can_book`) | Action: *Book a flight* (Transaction Amount $\le$ ₹8,000) | 🟢 **`ALLOW`** | `EXECUTED` | Transaction is within pre-approved passenger budget. Auto-authorized. |
| **5** | **Revoked Agent Making Any Request** | **`REVOKED`** (or `SUSPENDED`) | Any Action (Even read-only fare inquiries) | 🔴 **`BLOCK`** | `BLOCKED` | Absolute Security Lockdown: Revocation overrides all scopes and forces immediate denial. |
| **6** | **Any Flight Change or Refund Request** | `ACTIVE` (with change/refund scope) | Action: *Change a flight booking* OR *Request a refund* | 🟡 **`ASK CUSTOMER`** | `PENDING_CUSTOMER` | Schedule disruption and ticket cancellation/payout risks demand mandatory human confirmation. |

---

### 3. Critical Governance & Operational Precedences

#### 3.1 Revocation Overrides All Permissions (Precedence Rule)
* **Status Supremacy:** Agent status is the **very first check** performed by the Gatekeeper engine.
* If an agent's status is set to `REVOKED` (or `SUSPENDED`), **all previously granted action scopes and spending limits are rendered completely void**.
* Even if a revoked agent possesses valid `can_view_fares` permission and requests a harmless ₹0 flight fare query, the Gatekeeper strictly returns **`BLOCK`**.
* Invoking the administrative Kill-Switch permanently writes an ISO-8601 timestamp to the agent's `revoked_at` field and generates an immutable security audit event.

#### 3.2 Customer Approval Required for Pending Actions (Human-in-the-Loop Rule)
* **Strict Two-Phase Commitment:** Any transaction returning **`ASK CUSTOMER`** enters the system in a temporary holding state: `PENDING_CUSTOMER`.
* **Zero Automatic Execution:** A pending request is **never treated as approved, executed, or booked** until explicit human action occurs.
* The transaction remains dormant in the customer queue until the passenger logs into **Tab 2 (Customer Confirmation Inbox)** and selects:
  1. **`Approve Action`**: The request transitions from `PENDING_CUSTOMER` $\rightarrow$ **`APPROVED`** (simulated execution confirmed), and an audit entry is permanently stamped.
  2. **`Reject Action`**: The request transitions from `PENDING_CUSTOMER` $\rightarrow$ **`REJECTED`** (action denied by customer), and an audit entry is permanently stamped.

---

### 4. Detailed Policy Specifications

* **Rule 1 — Agent Registration & Scope Scrutiny:** Every commercial AI agent must be registered with an `Agent ID`, `Agent Name`, `Developer Organization`, and granular permissions (`can_view_fares`, `can_book`, `can_change_booking`, `can_request_refund`). Missing scopes result in an immediate **`BLOCK`**.
* **Rule 2 — Configurable ₹8,000 Booking Threshold:** Baseline spending threshold is set to ₹8,000. Bookings $\le$ ₹8,000 evaluate to **`ALLOW`**; bookings $>$ ₹8,000 evaluate to **`ASK CUSTOMER`**. Configurable via `core/config.py` and UI Settings.
* **Rule 3 — Mandatory Flight Change Review:** Every flight rescheduling request alters passenger itineraries and risks change fees. Autonomous execution is prohibited; all requests evaluate to **`ASK CUSTOMER`**.
* **Rule 4 — Mandatory Refund Authorization:** Every ticket refund releases allocated seat inventory and triggers financial payout. To prevent fraudulent or accidental cancellations, all refund requests evaluate to **`ASK CUSTOMER`**.
* **Rule 5 — Permanent Audit Log & Non-Repudiation:** Every inbound request, perimeter decision, human approval/rejection, and lifecycle change is permanently logged to SQLite with immutable timestamps for DGCA and Indian DPDP Act regulatory compliance.
