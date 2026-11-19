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
├── test_gatekeeper.py         # Automated 6-scenario verification test suite
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

#### 🔹 Test Case 1: Registered Agent with Read-Only Permission
* **Goal:** Verify that a registered agent with read-only permissions can view fares without friction, but is blocked from booking flights.
* **Steps:**
  1. Open **Tab 1: Live Agent Simulator**.
  2. Select Agent: **`AGT-READONLY-01`** (or `AGT-MMT-001` with *View flight fares*).
  3. Action A: Select **View flight fares** $\rightarrow$ Click **🚀 Dispatch Request**.
  4. Action B: Select **Book a flight** $\rightarrow$ Click **🚀 Dispatch Request**.
* **Expected Outcome:** 
  * Fare Query: 🟢 **`ALLOW`** (Status: `EXECUTED`).
  * Booking Attempt: 🔴 **`BLOCK`** (Status: `BLOCKED` — *Permission Denied: Missing Scope*).

---

#### 🔹 Test Case 2: Unknown or Unregistered Agent
* **Goal:** Verify that unverified or unregistered agent IDs are denied at the perimeter.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, dispatch a request using an unregistered agent ID (`AGT-UNKNOWN-999`).
* **Expected Outcome:** 🔴 **`BLOCK`**
  * Status: `BLOCKED`.
  * Policy rationale confirms: *"Security Violation: Agent ID 'AGT-UNKNOWN-999' is not registered in the IndiGo Agent Directory."*

---

#### 🔹 Test Case 3: High-Value Booking Above Threshold ($>$ ₹8,000)
* **Goal:** Verify that transactions exceeding the ₹8,000 limit trigger human-in-the-loop protection.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **Personal Gemini Travel Agent (`AGT-GEM-003`)**.
  2. Select Action: **Book a flight**.
  3. Select Itinerary: **Mumbai (BOM) $\rightarrow$ Goa (GOI) | Flight 6E-802 (Fare: ₹9,500.00)** (or enter any amount $> ₹8,000$).
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟡 **`ASK CUSTOMER`**
  * Status is marked as `PENDING_CUSTOMER`.
  * Rationale explains: *"Booking value of ₹9,500.00 EXCEEDS the pre-approved limit of ₹8,000.00. Sent to Customer Confirmation Portal."*
  * **Demonstrate Confirmation:** Switch to **Tab 2: Confirmation Inbox**, review the pending ₹9,500 booking, and click **`✅ Approve Action`**. Notice the status immediately transitions to `APPROVED`.

---

#### 🔹 Test Case 4: Booking Below ₹8,000 Threshold ($\le$ ₹8,000)
* **Goal:** Verify that booking transactions at or below ₹8,000 execute autonomously without friction.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **MakeMyTrip Autonomous Booker (`AGT-MMT-001`)**.
  2. Select Action: **Book a flight**.
  3. Select Itinerary: **Delhi (DEL) $\rightarrow$ Mumbai (BOM) | Flight 6E-204 (Fare: ₹4,800.00)** ($\le$ ₹8,000).
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🟢 **`ALLOW`**
  * Status is marked as `EXECUTED`.
  * Rationale confirms: *"Booking value of ₹4,800.00 is within the pre-approved limit of ₹8,000.00. Auto-authorized without human friction."*

---

#### 🔹 Test Case 5: Revoked Agent Attempting Any Request
* **Goal:** Verify that revoked agents are completely locked down across all operations.
* **Steps:**
  1. Open **Tab 3: Agent Directory & Revocation**.
  2. Select an active agent (e.g. `AGT-EXP-002`) and click **`🚨 Invoke Kill Switch: REVOKE AGENT`** (or select pre-seeded revoked agent `AGT-ROG-005`).
  3. In **Tab 1**, attempt any request (even a read-only *View flight fares*) using the revoked agent.
  4. Click **🚀 Dispatch Request to Gatekeeper**.
* **Expected Outcome:** 🔴 **`BLOCK`**
  * Status is marked as `BLOCKED`.
  * Rationale explains: *"Security Lockdown: Agent access was REVOKED. All incoming requests are strictly BLOCKED."*

---

#### 🔹 Test Case 6: Custom Scenario — Mandatory Refund & Customer Sign-Off
* **Goal:** Verify that ticket refunds strictly require passenger authorization and follow the two-phase lifecycle: `ASK CUSTOMER` $\rightarrow$ `PENDING_CUSTOMER` $\rightarrow$ `APPROVED`.
* **Steps:**
  1. In **Tab 1: Live Agent Simulator**, select Agent: **MakeMyTrip Autonomous Booker (`AGT-MMT-001`)**.
  2. Select Action: **Request a refund** (Amount: ₹7,200.00 for flight 6E-501).
  3. Click **🚀 Dispatch Request to Gatekeeper**.
  4. Switch to **Tab 2: Confirmation Inbox** and click **`✅ Approve Action`**.
* **Expected Outcome:** 
  * Initial Verdict: 🟡 **`ASK CUSTOMER`** (Status: `PENDING_CUSTOMER`).
  * Post-Approval Status: **`APPROVED`** (Simulated execution confirmed and permanently logged in SQLite).

---

## 🧪 5. Automated Verification Tests

You can execute the automated test suite directly from your terminal:

```powershell
python test_gatekeeper.py
```

### Official Automated Test Results Table

| Scenario Name | Expected Decision | Actual Decision | Final Status |
| :--- | :--- | :--- | :---: |
| **1. Registered Agent with Read-Only Permission** | `ALLOW` (Fare query) / `BLOCK` (Booking attempt) | `ALLOW` (Fare query) / `BLOCK` (Booking attempt) | **PASS** |
| **2. Unknown or Unregistered Agent** | `BLOCK` | `BLOCK` | **PASS** |
| **3. Booking Amount Above ₹8,000 Threshold** | `ASK CUSTOMER` | `ASK CUSTOMER` | **PASS** |
| **4. Booking Amount At or Below ₹8,000 Threshold** | `ALLOW` | `ALLOW` | **PASS** |
| **5. Revoked Agent Attempting Any Request** | `BLOCK` | `BLOCK` | **PASS** |
| **6. Custom Scenario: Mandatory Refund & Customer Sign-Off** | `ASK CUSTOMER → PENDING_CUSTOMER → APPROVED after customer approval` | `ASK CUSTOMER → PENDING_CUSTOMER → APPROVED after customer approval` | **PASS** |

### Raw Terminal Output:
```text
======================================================================
✈️  INDIGO AIRLINES AGENT GATEKEEPER — AUTOMATED VERIFICATION TEST SUITE
======================================================================

[Scenario 1] Testing registered agent with read-only permission...
  -> Fare View Verdict: ALLOW (Status: EXECUTED)
  -> Unauthorized Booking Verdict: BLOCK (Status: BLOCKED)
  -> Result: PASS

[Scenario 2] Testing unknown / unregistered agent...
  -> Verdict: BLOCK (Status: BLOCKED)
  -> Reason: Security Violation: Agent ID 'AGT-UNKNOWN-999' is not registered in the IndiGo Agent Directory.
  -> Result: PASS

[Scenario 3] Testing booking above ₹8,000 threshold (₹9,500)...
  -> Verdict: ASK CUSTOMER (Status: PENDING_CUSTOMER)
  -> Reason: Booking value of ₹9,500.00 EXCEEDS the pre-approved limit of ₹8,000.00. Sent to Customer Confirmation Portal for explicit approval.
  -> Result: PASS

[Scenario 4] Testing booking below ₹8,000 threshold (₹4,800)...
  -> Verdict: ALLOW (Status: EXECUTED)
  -> Reason: Booking value of ₹4,800.00 is within the pre-approved limit of ₹8,000.00. Auto-authorized without human friction.
  -> Result: PASS

[Scenario 5] Testing revoked agent making a request...
  -> Verdict: BLOCK (Status: BLOCKED)
  -> Reason: Security Lockdown: Agent 'ScraperBot BlackHat AI' (AGT-ROG-005) access was REVOKED on 2026-11-19 18:18:59. All incoming requests are strictly BLOCKED.
  -> Result: PASS

[Scenario 6] Testing Custom Scenario: Mandatory Refund Request & Customer Sign-Off...
  -> Initial Gatekeeper Verdict: ASK CUSTOMER (Status: PENDING_CUSTOMER)
  -> Post-Approval Status: APPROVED
  -> Result: PASS

======================================================================
📊 SUMMARY TEST REPORT — ALL SIX SCENARIOS
======================================================================
✅ [PASS] Scenario 1: Registered Agent with Read-Only Permission
    Details: Fare View: ALLOW | Booking without scope: BLOCK
✅ [PASS] Scenario 2: Unknown / Unregistered Agent
    Details: Verdict: BLOCK | Reason: Security Violation: Agent ID 'AGT-UNKNOWN-999' is not registered in the IndiGo Agent Directory.
✅ [PASS] Scenario 3: Booking Above ₹8,000 (₹9,500)
    Details: Verdict: ASK CUSTOMER | Status: PENDING_CUSTOMER
✅ [PASS] Scenario 4: Booking Below ₹8,000 (₹4,800)
    Details: Verdict: ALLOW | Status: EXECUTED
✅ [PASS] Scenario 5: Revoked Agent Attempt
    Details: Verdict: BLOCK | Reason: Security Lockdown: Agent 'ScraperBot BlackHat AI' (AGT-ROG-005) access was REVOKED on 2026-11-19 18:18:59. All incoming requests are strictly BLOCKED.
✅ [PASS] Scenario 6: Custom — Mandatory Refund & Customer Sign-Off
    Details: Initial: ASK CUSTOMER (PENDING_CUSTOMER) -> After Customer Approval: APPROVED
======================================================================
🎉 ALL SIX REQUIRED TEST SCENARIOS PASSED SUCCESSFULLY!
======================================================================
```

---

## 🏛️ 6. Core Business & Governance Takeaways for MBA Discussion

1. **Zero-Trust Architecture for Agentic Commerce:** Airlines cannot treat autonomous AI agents like standard human browser sessions. Every transaction must be validated against real-time agent registration, granular permissions, and dynamic financial thresholds.
2. **Optimal Risk-to-Friction Balance:** Forcing human sign-off on every trivial query destroys the utility of AI assistants; conversely, auto-approving high-value transactions introduces severe dispute liability. The Gatekeeper’s ₹8,000 threshold and mandatory change/refund triggers strike the optimal commercial balance.
3. **Legal Defensibility & Audit Compliance:** Under emerging global AI governance standards and the Indian Digital Personal Data Protection (DPDP) framework, maintaining immutable audit trails of AI intent versus human customer consent is essential for mitigating chargebacks, dispute claims, and regulatory penalties.
