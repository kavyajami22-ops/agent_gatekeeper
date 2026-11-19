# Project Report: IndiGo Airlines — Agent Gatekeeper (6E Guard)
**Course:** MBA in Technology Management / Executive Business Analytics  
**Candidate Enrolment ID:** `PGD202564221` (Configurable Project Identifier)  
**System Title:** IndiGo Airlines — Agent Gatekeeper (6E Guard)  
**Academic Context:** Educational Simulation — Autonomous AI Agent Governance  

---

### 1. Executive Summary & Business Problem

As consumer commerce rapidly evolves from human-driven web interfaces to autonomous AI agents (such as MakeMyTrip bots, Expedia assistants, and Google Gemini personal concierges), commercial airlines face an unprecedented governance challenge. Autonomous travel agents can search, reserve, reschedule, and cancel flights on behalf of passengers. While this creates a frictionless booking experience, it introduces substantial enterprise risks:
* **Financial Risk & Hallucination Exposure:** Autonomous agents may misinterpret user intent or hallucinate booking criteria, triggering high-value financial charges without explicit passenger awareness.
* **Operational Disruption:** Arbitrary flight schedule modifications disrupt passenger itineraries, mismanage connection windows, and incur unforeseen airline change fees.
* **Irreversible Inventory Depletion:** Cancellation and refund requests instantly release airline seat inventory and initiate financial disbursements, creating opportunities for dispute claims, malicious cancellations, or severe passenger dissatisfaction.

Traditional security systems rely on CAPTCHAs and session cookies designed for human browsers, which fail to manage machine-to-machine agentic commerce. Airlines require an intelligent, zero-trust policy interceptor—an **Agent Gatekeeper**—to evaluate incoming AI agent requests before they reach core reservation infrastructure.

> **Educational Simulation Notice:** This project is an educational simulation developed strictly for academic purposes. It operates in a safe, sandboxed environment. No real airline reservation systems (PSS/GDS), airline inventory feeds, or real payment gateways are connected or transacted.

---

### 2. Project Objectives

The primary objective of the **IndiGo Agent Gatekeeper (6E Guard)** is to design, implement, and validate an automated policy management gateway that enforces customer sovereignty and airline security over external AI agents. Specific objectives include:
1. **Tri-State Deterministic Governance:** Classifying every inbound agent request into one of three distinct outcomes: `ALLOW`, `ASK CUSTOMER`, or `BLOCK`.
2. **Pre-Approved Spending Controls:** Automating low-risk transactions while holding transactions above an initial configurable threshold of **₹8,000** for human verification.
3. **Mandatory Human-in-the-Loop Safeguards:** Enforcing mandatory passenger sign-off on all schedule modifications and refund requests.
4. **Agent Access Control & Revocation:** Providing an administrative kill-switch to immediately revoke compromised agents and record permanent timestamps.
5. **Regulatory Auditability:** Maintaining an immutable, persistent audit log to guarantee non-repudiation and compliance readiness.

---

### 3. How the Gatekeeper Works

The Gatekeeper functions as an intermediary policy layer positioned between external AI agents and IndiGo's simulated reservation engine. Every inbound transaction is processed sequentially through four evaluation stages:

1. **Identity & Status Verification:** The Gatekeeper checks if the calling agent exists in the registered directory. If the agent's status is `REVOKED` or `SUSPENDED`, the request is instantly **BLOCKED** with zero exceptions.
2. **Permission Scope Check:** The system verifies whether the agent's registered profile explicitly permits the requested action (`View flight fares`, `Book a flight`, `Change a flight booking`, or `Request a refund`). If unpermitted, the request is **BLOCKED**.
3. **Risk & Policy Matrix Evaluation:**
   * *View flight fares:* Classified as low risk (read-only). Automatically **ALLOWED**.
   * *Book a flight:* Compared against the pre-approved limit (default ₹8,000). Values $\le$ ₹8,000 are **ALLOWED**; values $>$ ₹8,000 return **ASK CUSTOMER**.
   * *Change a flight booking:* Operational disruption risk. Always returns **ASK CUSTOMER**.
   * *Request a refund:* Financial and inventory release risk. Always returns **ASK CUSTOMER**.
4. **Customer Confirmation & Simulated Execution:** Requests marked `ALLOW` update internal state to `EXECUTED`. Requests marked `ASK CUSTOMER` enter a pending queue where the passenger can click **Approve** or **Reject**, transitioning the simulated state to `APPROVED` or `REJECTED`. Every transition appends an immutable record to the audit ledger.

---

### 4. Technology Stack & System Architecture

To ensure operational reliability and simplicity for academic grading, the system was built using a clean, zero-external-dependency core architecture:

* **Programming Language:** Python 3.11 with clean modular separation (`core/config.py`, `core/database.py`, `core/gatekeeper.py`, `core/seed_data.py`).
* **Persistent Database Layer:** SQLite (`sqlite3` standard library), providing ACID-compliant relational storage across three tables: `agents`, `requests`, and `audit_log`.
* **Zero-Dependency Web Server:** Built-in Python `http.server` ([server.py](file:///c%3A/Users/kavya/OneDrive/Desktop/agent_gatekeeper/server.py)) serving a responsive HTML5/CSS/JavaScript dashboard at `http://localhost:8501`. Enables immediate execution on any machine with only base Python installed.
* **Streamlit Framework:** Optional modern interactive dashboard ([app.py](file:///c%3A/Users/kavya/OneDrive/Desktop/agent_gatekeeper/app.py)) with Plotly visual analytics for environments with installed dependencies.
* **One-Click Windows Launcher:** Provided via [run.bat](file:///c%3A/Users/kavya/OneDrive/Desktop/agent_gatekeeper/run.bat).

---

### 5. Key Functional Modules

1. **Tab 1 — Live Agent Simulator & Sandbox:** Allows administrators or evaluators to select registered commercial agents (MakeMyTrip, Expedia, Gemini Assistant, or Rogue bots), configure flight itineraries and transaction amounts, and dispatch requests to witness real-time Gatekeeper evaluation cards.
2. **Tab 2 — Passenger Confirmation Inbox (Human-in-the-Loop):** Dedicated portal displaying all actions held in `ASK CUSTOMER` status. Passengers review flight details, financial impact, and policy rationale, then approve or reject the request.
3. **Tab 3 — Agent Governance & Revocation Kill-Switch:** Complete directory displaying all agents, permission toggles, and permanent lifecycle timestamps (`registered_at`, `revoked_at`). Includes an emergency revocation button that instantly terminates an agent's access.
4. **Tab 4 — Permanent Audit Log & Executive Analytics:** Real-time KPI summary (Total Interceptions, Auto-Allowed %, Sent to Customer %, Blocked %), searchable audit table, and one-click CSV export for regulatory auditing.

---

### 6. Empirical Testing & Validation Results

The application's policy engine and business logic were rigorously verified using the automated test suite ([test_gatekeeper.py](file:///c%3A/Users/kavya/OneDrive/Desktop/agent_gatekeeper/test_gatekeeper.py)). All six required Gatekeeper test scenarios passed completely:

| Scenario Name | Expected Decision | Actual Decision | Final Status |
| :--- | :--- | :--- | :---: |
| **1. Registered Agent with Read-Only Permission** | `ALLOW` (Fare query) / `BLOCK` (Booking attempt) | `ALLOW` (Fare query) / `BLOCK` (Booking attempt) | **PASS** |
| **2. Unknown or Unregistered Agent** | `BLOCK` | `BLOCK` | **PASS** |
| **3. Booking Amount Above ₹8,000 Threshold** | `ASK CUSTOMER` | `ASK CUSTOMER` | **PASS** |
| **4. Booking Amount At or Below ₹8,000 Threshold** | `ALLOW` | `ALLOW` | **PASS** |
| **5. Revoked Agent Attempting Any Request** | `BLOCK` | `BLOCK` | **PASS** |
| **6. Custom Scenario: Mandatory Refund & Customer Sign-Off** | `ASK CUSTOMER → PENDING_CUSTOMER → APPROVED after customer approval` | `ASK CUSTOMER → PENDING_CUSTOMER → APPROVED after customer approval` | **PASS** |

---

### 7. Strategic MBA Takeaways & Conclusion

The IndiGo Agent Gatekeeper demonstrates that managing autonomous AI agents in commercial aviation requires a balanced governance model:
1. **Risk-Calibrated Automation:** Full automation creates unacceptable liability, while zero automation eliminates the efficiency of AI. By establishing an intelligent threshold (₹8,000) and isolating sensitive operations (changes/refunds), airlines achieve optimal friction-to-security balance.
2. **Zero-Trust Architecture:** External AI agents cannot be implicitly trusted based on API keys alone. Every incoming payload must be verified against real-time agent status, scopes, and transaction limits.
3. **Non-Repudiation & Legal Compliance:** By maintaining immutable timestamps and audit trails of agent requests and human customer confirmations, airlines safeguard against consumer disputes, chargebacks, and regulatory compliance scrutiny under consumer protection and data protection frameworks.
