# ✈️ IndiGo Airlines: Autonomous AI Agent Gatekeeper (6E Guard)
**MBA Capstone Assignment: Emerging Tech & Autonomous AI Governance**  
**Student Enrolment ID:** `PGD202564221` (Configurable Project Identifier)  
**Course:** MBA in Technology Management / Executive Business Analytics  

---

## 📌 1. Executive Summary & Business Rationale

As consumer travel booking transitions from manual web searches to **autonomous AI agents** (such as Google Gemini, MakeMyTrip bots, and personal travel concierges), commercial airlines face an unprecedented governance challenge:
* **Frictionless Automation:** Legitimate low-risk actions (checking fares, low-cost bookings) must execute seamlessly without human friction.
* **Financial & Schedule Exposure:** Actions exceeding pre-approved passenger budgets or altering complex flight schedules introduce substantial risk of hallucinations, dispute costs, and fraud.
* **Irreversible Downside:** Cancellations and refunds release airline seat inventory and trigger financial disbursements, demanding strict human-in-the-loop authorization.

The **IndiGo Agent Gatekeeper** acts as an enterprise zero-trust policy interceptor. Every request dispatched by an external AI agent is evaluated against deterministic airline governance rules before touching reservation systems, producing one of three verdicts:
1. 🟢 **`ALLOW`**: Pre-authorized, low-risk requests execute autonomously.
2. 🟡 **`ASK CUSTOMER`**: Sensitive, financial, or disruptive actions are routed to a passenger confirmation queue.
3. 🔴 **`BLOCK`**: Revoked credentials, unauthorized scopes, or policy violations are rejected immediately.

> ℹ️ **Educational Simulation Guarantee:** This system is an educational simulation designed for academic evaluation. No real external airline reservation systems, GDS APIs, or banking gateways are contacted. All state transitions (`PENDING_CUSTOMER` $\rightarrow$ `APPROVED` / `REJECTED`) operate in a secure, simulated local environment.

---

## ⚙️ 2. Key Architectural Rules Implemented

| Rule # | Requirement | Implementation Details |
| :---: | :--- | :--- |
| **1** | **Prominent Academic ID** | Enrolment Number **`PGD202564221`** is highlighted on the main dashboard header and sidebar. It is also dynamically configurable in Settings. |
| **2** | **Initial Booking Threshold** | Initial pre-approved flight booking limit is set to **₹8,000** (adjustable via UI settings). |
| **3** | **Booking Price Policy** | • Booking $\le$ ₹8,000 $\rightarrow$ 🟢 `ALLOW`<br>• Booking $>$ ₹8,000 $\rightarrow$ 🟡 `ASK CUSTOMER` |
| **4** | **Mandatory Human-in-the-Loop** | **Every flight change** and **every refund request** strictly requires customer confirmation (🟡 `ASK CUSTOMER`). |
| **5** | **Revoked Agent Lockdown** | Any agent marked as `REVOKED` (or `SUSPENDED`) immediately returns 🔴 **`BLOCK`** with zero exceptions across all actions. |
| **6** | **Permanent Timestamps** | SQLite database permanently stores ISO-8601 timestamps for `registered_at`, `revoked_at`, request arrivals, and customer approvals. |
| **7** | **Interactive 4-Tab Architecture** | Clean separation across Agent Simulation, Passenger Confirmation, Governance Kill-Switch, and Audit Analytics. |

---

## 📁 3. Project Directory Structure

```
agent_gatekeeper/
│
├── server.py                  # 🚀 Zero-Dependency Pure Python Web Dashboard (Runs out-of-the-box!)
├── run.bat                    # 🖱️ One-Click Windows launcher (Double-click to launch!)
├── app.py                     # Streamlit web application (alternative option)
├── test_gatekeeper.py         # Automated 10-test verification test suite
├── requirements.txt           # Optional dependencies for Streamlit: streamlit, pandas, plotly
├── README.md                  # Comprehensive documentation & test walkthrough
├── REPORT.md                  # 2-Page MBA Project Report
├── REPORT.pdf                 # Formatted 2-Page A4 PDF submission
├── RULES.md                   # 1-Page Business Governance Rules sheet
├── PROMPTS.md                 # AI Interaction Log & Human Verification Audit
│
├── core/                      # Clean modular architecture
│   ├── __init__.py
│   ├── config.py              # Configuration (Enrolment ID: PGD202564221, ₹8,000 Limit)
│   ├── database.py            # SQLite schema, persistent storage, timestamps & queries
│   ├── gatekeeper.py          # Gatekeeper Decision Engine (ALLOW / ASK CUSTOMER / BLOCK)
│   └── seed_data.py           # Pre-seeded sample agents (Active & Revoked) and flight itineraries
│
└── data/                      # Local database directory
    └── gatekeeper.db          # Auto-created SQLite persistent database
```

---

## 🚀 4. How to Run the Project and Demonstrate the Six Test Cases

### 4.1 Simple Windows Launch Instructions

You can run the application with **zero external dependencies** using Python's built-in standard library:

1. **One-Click Launch (Recommended for Windows):**
   * Open the `agent_gatekeeper` project folder in Windows File Explorer.
   * Simply **double-click** on **`run.bat`**.
   * A terminal window will open and start the local web server.

2. **Command Line Launch (Alternative):**
   * Open PowerShell or Command Prompt in the project folder and type:
     ```powershell
     python server.py
     ```

3. **Open the Dashboard in Your Web Browser:**
   * Open any browser (Edge, Chrome, Firefox) and navigate to:
     👉 **`http://localhost:8501`**
   * *(Note: If port 8501 is busy on your machine, the server will automatically fall back to `http://localhost:8000`).*

---

### 4.2 Architecture of the Four Main Dashboard Tabs

The web interface is organized into four intuitive, functional tabs:

1. **🛫 Tab 1: Live Agent Simulator & Sandbox**
   * Serves as the external test harness.
   * Allows the evaluator to select an external AI agent (*MakeMyTrip*, *Expedia*, *Google Gemini*, or a *Revoked Rogue Bot*), pick an action, configure flight/fare details, and click **🚀 Dispatch Request to Gatekeeper**.
   * Renders real-time visual verdict cards showing the Gatekeeper's decision (🟢 `ALLOW`, 🟡 `ASK CUSTOMER`, or 🔴 `BLOCK`) and the exact policy rationale.

2. **👤 Tab 2: Passenger Confirmation Inbox (Human-in-the-Loop)**
   * Displays all high-stakes or sensitive requests held in `PENDING_CUSTOMER` state.
   * Shows passenger details (PNR, customer ID, requested flight change/refund, financial impact, and reason for confirmation).
   * Provides **`✅ Approve Action`** and **`❌ Reject Action`** buttons that update the simulated request state in real time.

3. **🤖 Tab 3: Agent Directory & Revocation (The Kill Switch)**
   * Provides an administrative overview of all registered customer AI agents, their permissions, spending limits, and permanent `registered_at` and `revoked_at` timestamps.
   * Features the **Emergency Revocation Kill-Switch** allowing administrators to immediately revoke any agent or reactivate them.
   * Includes an onboarding form to register new external AI agents with granular permission scopes.

4. **📜 Tab 4: Permanent Audit Log & Executive Analytics**
   * Displays high-level executive KPI metrics: Total Interceptions, Auto-Allowed %, Sent to Customer %, and Blocked Breaches %.
   * Features a complete, searchable, immutable ledger of all historical events and status changes stored in SQLite.
   * Includes an **`📥 Export CSV`** button for regulatory compliance auditing (DGCA / Indian DPDP Act).

---

### 4.3 Step-by-Step Demonstration of the Six Test Cases

Follow these six step-by-step test scenarios during your grading evaluation or demonstration to prove that all Gatekeeper governance rules are strictly enforced:

```
+-----------------------------------------------------------------------------------------------------+
| Test Case | Scenario Description          | Key Parameter / Condition | Expected Gatekeeper Verdict |
+-----------------------------------------------------------------------------------------------------+
| Case 1    | Low-Value Booking / Fare View | Booking <= Rs. 8,000      | 🟢 ALLOW (Auto-Executed)    |
| Case 2    | High-Value Flight Booking     | Booking > Rs. 8,000       | 🟡 ASK CUSTOMER (Held)      |
| Case 3    | Flight Modification Request   | Any Flight Change         | 🟡 ASK CUSTOMER (Mandatory) |
| Case 4    | Ticket Refund Request         | Any Refund Request        | 🟡 ASK CUSTOMER (Mandatory) |
| Case 5    | Revoked Agent Attempt         | Agent Status: REVOKED     | 🔴 BLOCK (Access Denied)    |
| Case 6    | Permanent Audit Trail & Export| Full Transaction History  | ✅ Immutable Log & CSV Export|
+-----------------------------------------------------------------------------------------------------+
```

#### 🔹 Test Case 1: Autonomous Allowed Booking ($\le$ ₹8,000)
* **Goal:** Verify that pre-authorized, low-risk requests execute without human friction.
* **Steps:**
  1. Open **Tab 1: Live Agent Simulator**.
  2. Select Agent: **MakeMyTrip Autonomous Booker (`AGT-MMT-001`)** (Status: `ACTIVE`).
  3. Select Action: **Book a flight**.
  4. Select Itinerary: **Delhi (DEL) $\rightarrow$ Bengaluru (BLR) | Flight 6E-501 (Fare: ₹7,200.00)**.
  5. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟢 **`VERDICT: ALLOW`**
  * Status is marked as `EXECUTED`.
  * Policy rationale confirms: *"Booking value of ₹7,200.00 is within the pre-approved limit of ₹8,000.00. Auto-authorized without human friction."*

---

#### 🔹 Test Case 2: High-Value Booking Above Threshold ($>$ ₹8,000)
* **Goal:** Verify that transactions exceeding the ₹8,000 limit trigger human-in-the-loop protection.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **Personal Gemini Travel Agent (`AGT-GEM-003`)**.
  2. Select Action: **Book a flight**.
  3. Select Itinerary: **Mumbai (BOM) $\rightarrow$ Goa (GOI) | Flight 6E-802 (Fare: ₹9,500.00)** (or enter any amount $> ₹8,000$).
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟡 **`VERDICT: ASK CUSTOMER`**
  * Status is marked as `PENDING_CUSTOMER`.
  * Rationale explains: *"Booking value of ₹9,500.00 EXCEEDS the pre-approved limit of ₹8,000.00. Sent to Customer Confirmation Portal."*
  * **Demonstrate Confirmation:** Switch to **Tab 2: Confirmation Inbox**, review the pending ₹9,500 booking, and click **`✅ Approve Action`**. Notice the status immediately transitions to `APPROVED`.

---

#### 🔹 Test Case 3: Mandatory Customer Confirmation for Flight Changes
* **Goal:** Verify that schedule modifications strictly require human authorization to prevent itinerary clashes and change fees.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **Expedia Travel Assistant (`AGT-EXP-002`)**.
  2. Select Action: **Change a flight booking**.
  3. Enter PNR: `6E-K9P2X` and change fee amount: `₹1,500.00`.
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟡 **`VERDICT: ASK CUSTOMER`**
  * Status is marked as `PENDING_CUSTOMER`.
  * Rationale explains: *"Policy Requirement: Every flight schedule modification requires passenger consent to confirm flight timings and potential fare difference/change fees."*

---

#### 🔹 Test Case 4: Mandatory Customer Confirmation for Refund Requests
* **Goal:** Verify that ticket cancellations and refunds strictly require human sign-off to protect seat inventory and financial payouts.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **MakeMyTrip Autonomous Booker (`AGT-MMT-001`)**.
  2. Select Action: **Request a refund**.
  3. Enter PNR: `6E-M9K2L` and refundable fare: `₹4,800.00`.
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟡 **`VERDICT: ASK CUSTOMER`**
  * Status is marked as `PENDING_CUSTOMER`.
  * Rationale explains: *"Policy Requirement: Every refund request releases airline seat inventory and triggers payout. Mandatory passenger confirmation required to prevent unauthorized ticket cancellation."*

---

#### 🔹 Test Case 5: Emergency Revocation Kill-Switch (`BLOCK`)
* **Goal:** Verify that revoked agents are completely locked down across all operations.
* **Steps:**
  1. Open **Tab 3: Agent Directory & Revocation**.
  2. Under **Revocation & Access Control**, select an active agent: **Expedia Travel Assistant (`AGT-EXP-002`)**.
  3. Click **`🚨 Invoke Kill Switch: REVOKE AGENT`**.
  4. Observe that the status immediately turns to **`REVOKED`** and a permanent timestamp is recorded in the table under `Revoked At`.
  5. Return to **Tab 1: Live Agent Simulator**, select `AGT-EXP-002`, and attempt any action (even a harmless read-only *View flight fares*).
  6. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🔴 **`VERDICT: BLOCK`**
  * Status is marked as `BLOCKED`.
  * Rationale explains: *"Security Lockdown: Agent access was REVOKED. All incoming requests are strictly BLOCKED."*

---

#### 🔹 Test Case 6: Permanent Audit Trail & Regulatory CSV Export
* **Goal:** Verify that every transaction, decision, and customer approval is permanently preserved in the immutable SQLite ledger and exportable for audit compliance.
* **Steps:**
  1. Open **Tab 4: Audit Log & Analytics**.
  2. Observe the KPI summary tiles displaying total intercepted requests, allowed percentages, customer inquiries, and blocked violations.
  3. Inspect the audit log table: verify that every action from Test Cases 1 through 5 is recorded in chronological order with exact timestamps, agent IDs, decisions, and outcomes.
  4. Click the **`📥 Export CSV`** button at the top right of the table.
* **Expected Outcome:** ✅ **`Permanent Immutable Verification & Download`**
  * The browser immediately downloads `IndiGo_Gatekeeper_AuditLog.csv`.
  * Open the CSV file in Excel or Notepad to verify complete data integrity and non-repudiation under DGCA and Indian DPDP Act standards.

---

## 🧪 5. Automated Verification Tests

In addition to manual UI testing, you can execute the automated test suite directly from your terminal:

```powershell
python test_gatekeeper.py
```

### Actual Test Suite Execution Results:
```text
=================================================================
✈️  STARTING INDIGO AGENT GATEKEEPER VERIFICATION TEST SUITE
=================================================================
[Test 1] Initializing SQLite database and seeding sample data...
✅ DB initialized with 5 agents.

[Test 2] Testing Action 1: 'View flight fares'...
✅ View fares passed: Verdict=ALLOW, Status=EXECUTED

[Test 3] Testing Action 2: Booking <= ₹8,000 (₹4,800)...
✅ Booking <= ₹8,000 passed: Verdict=ALLOW, Status=EXECUTED

[Test 4] Testing Action 2: Booking > ₹8,000 (₹9,500)...
✅ Booking > ₹8,000 passed: Verdict=ASK CUSTOMER, Status=PENDING_CUSTOMER

[Test 5] Testing Action 3: 'Change a flight booking'...
✅ Flight change passed: Verdict=ASK CUSTOMER, Status=PENDING_CUSTOMER

[Test 6] Testing Action 4: 'Request a refund'...
✅ Refund request passed: Verdict=ASK CUSTOMER, Status=PENDING_CUSTOMER

[Test 7] Testing Rule #5: Revoked agent must ALWAYS return BLOCK...
✅ Revoked agent test passed: Verdict=BLOCK

[Test 8] Testing Dynamic Revocation Kill-Switch & Permanent Timestamps...
✅ Agent AGT-EXP-002 revoked successfully. Revoked timestamp logged.
✅ Newly revoked agent request instantly BLOCKED.

[Test 9] Testing Human-in-the-Loop Customer Approval...
✅ Customer confirmation passed: Status updated to APPROVED

[Test 10] Verifying Permanent Audit Log integrity...
✅ Permanent Audit Log contains 20 immutable entries.

=================================================================
🎉 ALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY!
=================================================================
```

---

## 🏛️ 6. Core Business & Governance Takeaways for MBA Discussion

1. **Zero-Trust Architecture for Agentic Commerce:** Airlines cannot treat autonomous AI agents like standard human browser sessions. Every transaction must be validated against real-time agent registration, granular permissions, and dynamic financial thresholds.
2. **Optimal Risk-to-Friction Balance:** Forcing human sign-off on every trivial query destroys the utility of AI assistants; conversely, auto-approving high-value transactions introduces severe dispute liability. The Gatekeeper’s ₹8,000 threshold and mandatory change/refund triggers strike the optimal commercial balance.
3. **Legal Defensibility & Audit Compliance:** Under emerging global AI governance standards and the Indian Digital Personal Data Protection (DPDP) framework, maintaining immutable audit trails of AI intent versus human customer consent is essential for mitigating chargebacks, dispute claims, and regulatory penalties.
