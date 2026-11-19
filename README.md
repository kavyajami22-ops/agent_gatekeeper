# ✈️ IndiGo Airlines: Autonomous AI Agent Gatekeeper (6E Guard)
**MBA Capstone Assignment: Emerging Tech & Autonomous AI Governance**  
**Student Enrolment ID:** `PGD202564221` (Prominently displayed & configurable)  
**Course:** MBA in Technology Management / Executive Business Analytics  

---

## 📌 1. Executive Summary & Business Rationale

As consumer travel booking transitions from manual web searches to **autonomous AI agents** (such as Google Gemini, MakeMyTrip bots, and personal travel concierges), airlines face an unprecedented governance challenge:
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
| **3** | **Booking Price Policy** | • Booking $\le$ ₹8,000 $\rightarrow$ `ALLOW`<br>• Booking $>$ ₹8,000 $\rightarrow$ `ASK CUSTOMER` |
| **4** | **Mandatory Human-in-the-Loop** | **Every flight change** and **every refund request** strictly requires customer confirmation (`ASK CUSTOMER`). |
| **5** | **Revoked Agent Lockdown** | Any agent marked as `REVOKED` (or `SUSPENDED`) immediately returns **`BLOCK`** with zero exceptions across all actions. |
| **6** | **Permanent Timestamps** | SQLite database permanently stores ISO-8601 timestamps for `registered_at`, `revoked_at`, request arrivals, and customer approvals. |
| **7** | **Interactive 4-Tab Architecture** | Clean separation across Agent Simulation, Passenger Confirmation, Governance Kill-Switch, and Audit Analytics. |

---

## 📁 3. Project Directory Structure

```
agent_gatekeeper/
│
├── server.py                  # 🚀 Zero-Dependency Pure Python Web Dashboard (Runs out-of-the-box!)
├── run.bat                    # 🖱️ One-Click Windows launcher (Just double click to launch!)
├── app.py                     # Streamlit web application (alternative option)
├── test_gatekeeper.py         # Automated 10-test verification test suite
├── requirements.txt           # Optional dependencies for Streamlit: streamlit, pandas, plotly
├── README.md                  # Project documentation & MBA evaluation walkthrough
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

## 🚀 4. How to Launch and Run the Application

You have **two simple ways** to run the project:

### Option A: Pure Python Mode (Recommended — Zero Setup Needed!)
Since you only have Python installed, you don't need to install any external packages at all:
1. Open PowerShell or Command Prompt in the project folder and type:
   ```powershell
   python server.py
   ```
   *(Or simply double-click **`run.bat`** in Windows File Explorer)*
2. Open your web browser and visit: **`http://localhost:8501`**
3. The complete 4-tab IndiGo Gatekeeper dashboard is ready to use!

---

### Option B: Streamlit Mode (If you install packages)
If you wish to run it using Streamlit:
1. Install dependencies:
   ```powershell
   pip install streamlit pandas plotly
   ```
2. Launch the Streamlit app:
   ```powershell
   streamlit run app.py
   ```

---

## 🧪 5. Automated Verification Tests

You can run the automated verification test suite to prove that all 10 project requirements, policy thresholds, and edge cases are strictly enforced:
```powershell
python test_gatekeeper.py
```
*Expected result: `🎉 ALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY!`*

---

## 🎯 6. Step-by-Step MBA Grading & Evaluator Walkthrough

To demonstrate the full capability of the Gatekeeper during your presentation or evaluation, follow this 6-scenario demonstration script:

### 🔹 Scenario 1: Autonomous Execution (`ALLOW`)
1. Open **Tab 1: Live Agent Simulator**.
2. Select **MakeMyTrip Autonomous Booker (AGT-MMT-001)** (Status: `ACTIVE`).
3. Select Action: **View flight fares** (or **Book a flight** with fare ₹4,800 or ₹7,200 $\le$ ₹8,000 limit).
4. Click **🚀 Dispatch Request to Gatekeeper**.
5. **Expected Outcome:** Green 🟢 **VERDICT: ALLOW**. Explains that booking is within pre-approved limit of ₹8,000 and auto-executes without passenger friction.

### 🔹 Scenario 2: High-Value Booking Requiring Consent (`ASK CUSTOMER`)
1. In **Tab 1**, choose Action: **Book a flight**.
2. Select the itinerary: **Mumbai (BOM) -> Goa (GOI) (Fare: ₹9,500)** or enter any amount $> ₹8,000$.
3. Click **🚀 Dispatch Request to Gatekeeper**.
4. **Expected Outcome:** Amber 🟡 **VERDICT: ASK CUSTOMER**. Explains that ₹9,500 exceeds the ₹8,000 limit and informs that the request was routed to Tab 2.
5. Switch to **Tab 2: Customer Confirmation Inbox**:
   * Observe the pending request card showing the ₹9,500 transaction and rationale.
   * Click **✅ Approve Action** or **❌ Reject Action**.
   * Note the instant simulated state update and permanent audit entry.

### 🔹 Scenario 3: Mandatory Flight Change Consent (`ASK CUSTOMER`)
1. In **Tab 1**, select Action: **Change a flight booking**.
2. Click **🚀 Dispatch Request to Gatekeeper**.
3. **Expected Outcome:** Amber 🟡 **VERDICT: ASK CUSTOMER**. Demonstrates that regardless of fare, every schedule modification requires passenger sign-off.

### 🔹 Scenario 4: Mandatory Refund Request Consent (`ASK CUSTOMER`)
1. In **Tab 1**, select Action: **Request a refund**.
2. Click **🚀 Dispatch Request to Gatekeeper**.
3. **Expected Outcome:** Amber 🟡 **VERDICT: ASK CUSTOMER**. Demonstrates strict human authorization before releasing ticket inventory and triggering refund payouts.

### 🔹 Scenario 5: Emergency Revocation Kill-Switch (`BLOCK`)
1. Open **Tab 3: Agent Directory & Revocation**.
2. Locate the **Revocation & Access Control** section.
3. Select an active agent (e.g., `AGT-EXP-002`) and click **🚨 Revoke Agent Access**.
4. Notice that the status changes to `REVOKED` and the exact timestamp is recorded in the table.
5. Return to **Tab 1** and try sending any request (even a simple Fare View) using that agent.
6. **Expected Outcome:** Red 🔴 **VERDICT: BLOCK**. Explains that the agent was revoked and all requests are strictly denied.

### 🔹 Scenario 6: Permanent Audit Trail & Executive Reporting
1. Open **Tab 4: Audit Log & Analytics**.
2. Review the top KPI cards (Total Interceptions, Auto-Allowed %, Sent to Customer %, Blocked %).
3. Inspect the audit log with all chronological entries.
4. Click **📥 Export CSV** to download the complete audit trail for compliance auditing (DGCA / Indian DPDP Act).
