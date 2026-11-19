"""
IndiGo Airlines — Agent Gatekeeper (6E Guard)
MBA Capstone Assignment: Autonomous AI Agent Governance System
Student Enrolment ID: PGD202564221
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, Any

from core.config import (
    DEFAULT_ENROLMENT_ID,
    DEFAULT_PRE_APPROVED_BOOKING_LIMIT,
    DECISION_ALLOW,
    DECISION_ASK_CUSTOMER,
    DECISION_BLOCK,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_BOOKING,
    ACTION_REQUEST_REFUND,
    ALL_ACTIONS,
    ACTION_METADATA,
    STATUS_EXECUTED,
    STATUS_PENDING_CUSTOMER,
    STATUS_APPROVED,
    STATUS_REJECTED,
    STATUS_BLOCKED,
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
    AGENT_STATUS_SUSPENDED,
)
from core.database import (
    init_db,
    get_all_agents,
    get_agent,
    update_agent_status,
    register_agent,
    get_pending_requests,
    get_all_requests,
    get_all_audit_logs,
    update_request_decision_by_customer,
    reset_database,
)
from core.seed_data import seed_sample_data, SAMPLE_FLIGHTS
from core.gatekeeper import GatekeeperEngine

# -------------------------------------------------------------
# Streamlit Page Setup & Custom IndiGo Theme
# -------------------------------------------------------------
st.set_page_config(
    page_title="IndiGo Agent Gatekeeper",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (IndiGo Navy Blue #001b94, Sky Blue #0077b6)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #001b94 0%, #0040c1 60%, #0077b6 100%);
        padding: 22px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0, 27, 148, 0.25);
    }
    .main-header h1 {
        color: white !important;
        font-size: 26px;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .enrolment-badge {
        display: inline-block;
        background-color: #ffd166;
        color: #001b94;
        font-weight: 800;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 14px;
        margin-top: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .simulation-pill {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        margin-left: 10px;
        border: 1px solid rgba(255,255,255,0.4);
    }
    .verdict-card {
        padding: 22px;
        border-radius: 12px;
        margin: 16px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }
    .verdict-allow {
        background-color: #ecfdf5;
        border-left: 7px solid #10b981;
    }
    .verdict-ask {
        background-color: #fffbeb;
        border-left: 7px solid #f59e0b;
    }
    .verdict-block {
        background-color: #fef2f2;
        border-left: 7px solid #ef4444;
    }
    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Database Initialization & Seed Data Setup
# -------------------------------------------------------------
@st.cache_resource
def setup_application_backend():
    init_db()
    seed_sample_data(force=False)
    return True

setup_application_backend()

# -------------------------------------------------------------
# Session State & Sidebar Configuration
# -------------------------------------------------------------
if "enrolment_id" not in st.session_state:
    st.session_state["enrolment_id"] = DEFAULT_ENROLMENT_ID

if "booking_limit" not in st.session_state:
    st.session_state["booking_limit"] = DEFAULT_PRE_APPROVED_BOOKING_LIMIT

if "last_verdict" not in st.session_state:
    st.session_state["last_verdict"] = None

# Sidebar Controls
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/9f/IndiGo_Airlines_logo.svg", width=180)
    st.markdown("### ✈️ **6E Gatekeeper Controls**")
    
    st.markdown("---")
    st.markdown("#### 🎓 **Academic Metadata**")
    enrolment_input = st.text_input(
        "Enrolment Number (Configurable):",
        value=st.session_state["enrolment_id"],
        help="Display identification for MBA submission."
    )
    if enrolment_input != st.session_state["enrolment_id"]:
        st.session_state["enrolment_id"] = enrolment_input
        st.rerun()

    st.markdown("---")
    st.markdown("#### ⚙️ **Gatekeeper Policy Threshold**")
    limit_input = st.number_input(
        "Pre-approved Booking Limit (₹):",
        min_value=1000.0,
        max_value=50000.0,
        value=float(st.session_state["booking_limit"]),
        step=500.0,
        help="Initial limit is ₹8,000. Bookings above this require customer confirmation."
    )
    if limit_input != st.session_state["booking_limit"]:
        st.session_state["booking_limit"] = limit_input
        st.success(f"Threshold updated to ₹{limit_input:,.2f}")

    st.markdown(f"""
    **Current Policy Rules:**
    * Fares View: **ALLOW**
    * Bookings $\le$ ₹{st.session_state['booking_limit']:,.0f}: **ALLOW**
    * Bookings $>$ ₹{st.session_state['booking_limit']:,.0f}: **ASK CUSTOMER**
    * Flight Changes: **ASK CUSTOMER**
    * Refund Requests: **ASK CUSTOMER**
    * Revoked Agents: **BLOCK**
    """)

    st.markdown("---")
    st.markdown("#### 🛠️ **Demo & Data Tools**")
    col_reset, col_reseed = st.columns(2)
    with col_reset:
        if st.button("🔄 Reset Demo", help="Re-seeds realistic sample data"):
            reset_database()
            seed_sample_data(force=True)
            st.session_state["last_verdict"] = None
            st.toast("Database reset and sample data re-seeded!", icon="✅")
            st.rerun()

    st.caption("🔒 **Educational Simulation Only:** No live booking APIs or banking gateways are triggered.")

# -------------------------------------------------------------
# Main Application Header
# -------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <h1>✈️ IndiGo Airlines — Autonomous AI Agent Gatekeeper</h1>
    <p style="margin-top: 6px; font-size: 15px; opacity: 0.95;">
        Intelligent Zero-Trust Policy Management & Permission Gateway for Third-Party AI Agents
    </p>
    <div>
        <span class="enrolment-badge">🎓 Enrolment No: {st.session_state["enrolment_id"]}</span>
        <span class="simulation-pill">🛡️ Simulation Mode: Safe Sandbox</span>
        <span class="simulation-pill">⚡ Booking Threshold: ₹{st.session_state["booking_limit"]:,.0f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Gatekeeper Engine Instance
# -------------------------------------------------------------
engine = GatekeeperEngine(booking_threshold=st.session_state["booking_limit"])

# Query live pending count for dynamic tab badge
pending_count = len(get_pending_requests())
tab_badge = f" ({pending_count} PENDING)" if pending_count > 0 else " (0)"

# -------------------------------------------------------------
# Define the 4 Main Tabs
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛫 Tab 1: Live Agent Simulator",
    f"👤 Tab 2: Customer Confirmation Inbox{tab_badge}",
    "🤖 Tab 3: Agent Directory & Revocation",
    "📜 Tab 4: Audit Log & Executive Analytics"
])

# =============================================================
# TAB 1: LIVE AGENT SIMULATOR & GATEKEEPER SANDBOX
# =============================================================
with tab1:
    st.markdown("### 🛫 **Simulate Incoming AI Agent Requests**")
    st.markdown(
        "Select an external customer AI agent, pick an action, and dispatch a request to see the Gatekeeper evaluate it in real time."
    )

    agents = get_all_agents()
    agent_options = {f"{a['name']} ({a['agent_id']}) — Status: {a['status']}": a['agent_id'] for a in agents}

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("#### 1. Inbound Request Parameters")
        
        selected_agent_label = st.selectbox(
            "Select Requesting AI Agent:",
            options=list(agent_options.keys()),
            help="Choose from active commercial agents or a revoked agent to test policy enforcement."
        )
        selected_agent_id = agent_options[selected_agent_label]
        agent_data = get_agent(selected_agent_id)

        # Show selected agent's permissions pill
        if agent_data:
            status_color = "#10b981" if agent_data["status"] == "ACTIVE" else "#ef4444"
            st.markdown(f"""
            <div style="font-size: 13px; margin-bottom: 12px; padding: 8px 12px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
                <strong>Developer:</strong> {agent_data['developer']} | 
                <strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{agent_data['status']}</span><br/>
                <strong>Permissions:</strong> Fares: {'✅' if agent_data['can_view_fares'] else '❌'} | 
                Book: {'✅' if agent_data['can_book'] else '❌'} | 
                Change: {'✅' if agent_data['can_change_booking'] else '❌'} | 
                Refund: {'✅' if agent_data['can_request_refund'] else '❌'}
            </div>
            """, unsafe_allow_html=True)

        action_choice = st.selectbox(
            "Select Action:",
            options=ALL_ACTIONS,
            index=1,
            help="The 4 supported actions defined in the assignment."
        )

        # Action Metadata Preview
        action_meta = ACTION_METADATA.get(action_choice, {})
        st.caption(f"ℹ️ **Action Type:** {action_choice} | **Risk:** {action_meta.get('risk_level')} | **Policy:** {action_meta.get('default_rule')}")

        # Flight presets or custom input
        st.markdown("##### Flight & Passenger Details")
        flight_preset = st.selectbox(
            "Choose Sample Flight Itinerary:",
            options=[f"{f['route']} | {f['flight_no']} ({f['class']}) — ₹{f['fare']:,.0f}" for f in SAMPLE_FLIGHTS] + ["Custom Flight Details"]
        )

        if flight_preset == "Custom Flight Details":
            flight_detail_text = st.text_input("Flight / Sector Details:", value="Delhi (DEL) -> Mumbai (BOM) | 6E-204")
            pnr_input = st.text_input("PNR / Booking Reference:", value="6E-K9P2X")
            amount_input = st.number_input("Transaction Amount (₹):", min_value=0.0, value=7500.0, step=500.0)
        else:
            # Extract from preset
            idx = [f"{f['route']} | {f['flight_no']} ({f['class']}) — ₹{f['fare']:,.0f}" for f in SAMPLE_FLIGHTS].index(flight_preset)
            matched_flight = SAMPLE_FLIGHTS[idx]
            flight_detail_text = f"{matched_flight['route']} | Flight {matched_flight['flight_no']} ({matched_flight['class']})"
            pnr_input = f"6E-PNR{idx+1}0"
            default_fare = 0.0 if action_choice == ACTION_VIEW_FARES else matched_flight["fare"]
            amount_input = st.number_input(
                "Transaction Amount (₹):",
                min_value=0.0,
                value=float(default_fare),
                step=500.0,
                help="Amount is automatically populated from flight fare; adjust as needed to test thresholds."
            )

        customer_id_input = st.text_input("Customer ID:", value="CUST-6E-801")

        dispatch_clicked = st.button("🚀 Dispatch Request to Gatekeeper", type="primary", use_container_width=True)

        if dispatch_clicked:
            verdict = engine.evaluate_request(
                agent_id=selected_agent_id,
                action=action_choice,
                customer_id=customer_id_input,
                pnr=pnr_input,
                flight_details=flight_detail_text,
                amount=amount_input,
                booking_threshold_override=st.session_state["booking_limit"]
            )
            st.session_state["last_verdict"] = verdict
            st.rerun()

    with col_output:
        st.markdown("#### 2. Gatekeeper Policy Evaluation")
        
        last_v = st.session_state.get("last_verdict")

        if not last_v:
            st.info("👈 Configure and dispatch an AI agent request on the left to see the Gatekeeper's decision.")
            st.markdown("""
            **How the Gatekeeper Decides:**
            * 🟢 **ALLOW**: Automatically authorizes safe, pre-approved requests (e.g. view fares, booking $\le$ ₹8,000).
            * 🟡 **ASK CUSTOMER**: Routes to Tab 2 for human-in-the-loop sign-off (e.g. booking $>$ ₹8,000, changes, refunds).
            * 🔴 **BLOCK**: Instantly denies revoked agents, missing action permissions, or invalid credentials.
            """)
        else:
            dec = last_v["decision"]
            card_class = (
                "verdict-allow" if dec == DECISION_ALLOW 
                else "verdict-ask" if dec == DECISION_ASK_CUSTOMER 
                else "verdict-block"
            )
            badge_icon = "🟢" if dec == DECISION_ALLOW else "🟡" if dec == DECISION_ASK_CUSTOMER else "🔴"

            st.markdown(f"""
            <div class="verdict-card {card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin: 0; color: #0f172a;">{badge_icon} VERDICT: {dec}</h2>
                    <span style="font-size: 13px; font-weight: bold; background: white; padding: 4px 10px; border-radius: 6px; border: 1px solid #cbd5e1;">
                        Status: {last_v['status']}
                    </span>
                </div>
                <hr style="margin: 12px 0; border: none; border-top: 1px solid rgba(0,0,0,0.1);"/>
                <p style="font-size: 15px; margin-bottom: 8px;"><strong>Reason / Policy Rationale:</strong></p>
                <p style="font-size: 14px; color: #334155; line-height: 1.5;">{last_v['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Details card
            st.markdown("##### 📋 Intercepted Request Summary")
            st.markdown(f"""
            * **Request ID:** `{last_v['request_id']}`
            * **Agent:** **{last_v['agent_name']}** (`{last_v['agent_id']}`)
            * **Action:** `{last_v['action']}`
            * **Itinerary:** {last_v['flight_details']}
            * **Amount:** ₹{last_v['amount']:,.2f}
            * **Timestamp:** `{last_v['timestamp']}`
            """)

            if dec == DECISION_ASK_CUSTOMER:
                st.warning("👉 **Next Step:** This request requires passenger confirmation. Open **Tab 2: Customer Confirmation Inbox** to approve or deny it.")
            elif dec == DECISION_ALLOW:
                st.success("✅ **Simulated Execution:** Action completed safely within policy limits. Recorded in permanent audit log.")
            elif dec == DECISION_BLOCK:
                st.error("🛑 **Access Blocked:** Request was denied before touching any reservation systems. Incident recorded in audit log.")

# =============================================================
# TAB 2: CUSTOMER CONFIRMATION INBOX (HUMAN-IN-THE-LOOP)
# =============================================================
with tab2:
    st.markdown("### 👤 **Passenger Confirmation Inbox (Human-in-the-Loop)**")
    st.markdown(
        "Sensitive or high-value actions flagged with **`ASK CUSTOMER`** wait here for your explicit authorization."
    )

    pending_list = get_pending_requests()

    if not pending_list:
        st.success("🎉 **All Clear!** There are currently no pending requests requiring customer confirmation.")
        st.info("Tip: Go to **Tab 1** and trigger a booking over ₹8,000, a flight change, or a refund request to see it appear here.")
    else:
        st.warning(f"⚠️ You have **{len(pending_list)} pending action(s)** awaiting your review.")

        for req in pending_list:
            with st.container():
                st.markdown(f"""
                <div style="background: white; border: 1px solid #f59e0b; border-radius: 10px; padding: 18px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(245, 158, 11, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #92400e;">⚠️ Action Pending: {req['action']}</h4>
                        <span style="background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 13px;">
                            Req ID: {req['request_id']}
                        </span>
                    </div>
                    <p style="margin: 10px 0 6px 0; font-size: 14px;">
                        <strong>Requesting Agent:</strong> {req.get('agent_name', req['agent_id'])} ({req.get('agent_developer', 'External Partner')})<br/>
                        <strong>Passenger PNR:</strong> <code>{req['pnr']}</code> | <strong>Customer ID:</strong> <code>{req['customer_id']}</code><br/>
                        <strong>Itinerary / Details:</strong> {req['flight_details']}<br/>
                        <strong>Financial Impact:</strong> <span style="font-size: 16px; font-weight: bold; color: #001b94;">₹{req['amount']:,.2f}</span>
                    </p>
                    <div style="background: #f8fafc; padding: 8px 12px; border-radius: 6px; font-size: 13px; color: #475569; margin-top: 8px;">
                        <strong>Why Confirmation is Needed:</strong> {req['reason']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_app, col_rej, col_spacer = st.columns([1, 1, 3])
                with col_app:
                    if st.button(f"✅ Approve Action", key=f"app_{req['request_id']}", type="primary"):
                        update_request_decision_by_customer(
                            request_id=req['request_id'],
                            customer_action="APPROVE",
                            customer_notes="Passenger manually confirmed via 6E Customer Portal."
                        )
                        st.toast(f"Request {req['request_id']} APPROVED!", icon="✅")
                        st.rerun()

                with col_rej:
                    if st.button(f"❌ Reject Action", key=f"rej_{req['request_id']}"):
                        update_request_decision_by_customer(
                            request_id=req['request_id'],
                            customer_action="REJECT",
                            customer_notes="Passenger declined transaction in 6E Customer Portal."
                        )
                        st.toast(f"Request {req['request_id']} REJECTED!", icon="🛑")
                        st.rerun()

                st.markdown("---")

# =============================================================
# TAB 3: AGENT DIRECTORY & REVOCATION (THE KILL SWITCH)
# =============================================================
with tab3:
    st.markdown("### 🤖 **Agent Governance & Revocation (The Kill Switch)**")
    st.markdown(
        "Manage external AI agent credentials, configure action permissions, or invoke the emergency revocation kill-switch."
    )

    all_agents = get_all_agents()
    active_count = sum(1 for a in all_agents if a['status'] == AGENT_STATUS_ACTIVE)
    revoked_count = sum(1 for a in all_agents if a['status'] == AGENT_STATUS_REVOKED)

    # Top KPI Metrics
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Registered Agents", len(all_agents))
    with kpi2:
        st.metric("Active & Permitted", active_count)
    with kpi3:
        st.metric("Revoked Agents", revoked_count, delta="Zero-Tolerance Lockdown", delta_color="inverse")

    st.markdown("---")
    st.markdown("#### 1. Registered Agent Directory")

    # Format table for display
    display_rows = []
    for a in all_agents:
        display_rows.append({
            "Agent ID": a["agent_id"],
            "Agent Name": a["name"],
            "Developer": a["developer"],
            "Status": a["status"],
            "View Fares": "✅" if a["can_view_fares"] else "❌",
            "Book": "✅" if a["can_book"] else "❌",
            "Change": "✅" if a["can_change_booking"] else "❌",
            "Refund": "✅" if a["can_request_refund"] else "❌",
            "Limit (₹)": f"₹{a['custom_spending_limit']:,.0f}",
            "Registered At": a["registered_at"],
            "Revoked At": a["revoked_at"] if a["revoked_at"] else "—"
        })

    df_agents = pd.DataFrame(display_rows)
    st.dataframe(df_agents, use_container_width=True, hide_index=True)

    st.markdown("---")
    col_manage, col_register = st.columns([1, 1], gap="large")

    with col_manage:
        st.markdown("#### 2. Revocation & Access Control (Kill Switch)")
        st.markdown(
            "Immediately terminate an agent's access if suspicious activity is detected. Permanent timestamps are logged."
        )

        agent_to_alter_label = st.selectbox(
            "Select Agent to Manage:",
            options=[f"{a['name']} ({a['agent_id']}) — Status: {a['status']}" for a in all_agents],
            key="manage_agent_selector"
        )
        selected_aid = agent_to_alter_label.split("(")[1].split(")")[0]
        selected_a_obj = get_agent(selected_aid)

        if selected_a_obj:
            curr_status = selected_a_obj["status"]
            if curr_status == AGENT_STATUS_ACTIVE:
                st.warning(f"⚠️ Agent **{selected_a_obj['name']}** is currently **ACTIVE**.")
                revoke_reason = st.text_input("Reason for Revocation:", value="Administrative security review / policy violation")
                if st.button("🚨 Invoke Kill Switch: REVOKE AGENT", type="primary", use_container_width=True):
                    update_agent_status(selected_aid, AGENT_STATUS_REVOKED, reason=revoke_reason)
                    st.toast(f"Agent {selected_aid} has been REVOKED permanently!", icon="🛑")
                    st.rerun()
            else:
                st.error(f"🛑 Agent **{selected_a_obj['name']}** is **{curr_status}** (Revoked At: {selected_a_obj.get('revoked_at')}).")
                if st.button("✅ Reactivate Agent Access", use_container_width=True):
                    update_agent_status(selected_aid, AGENT_STATUS_ACTIVE, reason="Re-instated by IndiGo Security Admin")
                    st.toast(f"Agent {selected_aid} is now ACTIVE!", icon="✅")
                    st.rerun()

    with col_register:
        st.markdown("#### 3. Onboard New Customer AI Agent")
        with st.form("register_agent_form"):
            new_id = st.text_input("Agent ID:", value=f"AGT-CUSTOM-{len(all_agents)+1:03d}")
            new_name = st.text_input("Agent Name:", placeholder="e.g. Cleartrip Autonomous Booker")
            new_dev = st.text_input("Developer / Organization:", placeholder="e.g. Cleartrip Pvt Ltd")
            
            st.markdown("**Permission Scopes:**")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                scope_view = st.checkbox("View Flight Fares", value=True)
                scope_book = st.checkbox("Book Flight", value=True)
            with col_p2:
                scope_change = st.checkbox("Change Flight Booking", value=True)
                scope_refund = st.checkbox("Request Refund", value=False)

            new_limit = st.number_input("Custom Spending Limit (₹):", min_value=1000.0, value=8000.0, step=500.0)
            
            submit_agent = st.form_submit_button("➕ Register AI Agent", use_container_width=True)

            if submit_agent:
                if not new_name or not new_dev:
                    st.error("Please provide both an Agent Name and Developer Organization.")
                else:
                    register_agent(
                        agent_id=new_id,
                        name=new_name,
                        developer=new_dev,
                        can_view_fares=scope_view,
                        can_book=scope_book,
                        can_change_booking=scope_change,
                        can_request_refund=scope_refund,
                        custom_spending_limit=new_limit,
                        status=AGENT_STATUS_ACTIVE
                    )
                    st.toast(f"Agent '{new_name}' registered successfully!", icon="🎉")
                    st.rerun()

# =============================================================
# TAB 4: PERMANENT AUDIT LOG & EXECUTIVE ANALYTICS
# =============================================================
with tab4:
    st.markdown("### 📜 **Permanent Audit Log & Executive Analytics**")
    st.markdown(
        "An immutable chronological record of every incoming request, Gatekeeper evaluation, human customer confirmation, and administrative lifecycle change."
    )

    all_logs = get_all_audit_logs()
    all_requests = get_all_requests()

    # Executive KPI Summary
    total_reqs = len(all_requests)
    allowed_count = sum(1 for r in all_requests if r["gatekeeper_decision"] == DECISION_ALLOW)
    ask_count = sum(1 for r in all_requests if r["gatekeeper_decision"] == DECISION_ASK_CUSTOMER)
    blocked_count = sum(1 for r in all_requests if r["gatekeeper_decision"] == DECISION_BLOCK)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Interceptions", total_reqs)
    with k2:
        allow_pct = (allowed_count / total_reqs * 100) if total_reqs else 0
        st.metric("Auto-Allowed (ALLOW)", f"{allowed_count} ({allow_pct:.0f}%)")
    with k3:
        ask_pct = (ask_count / total_reqs * 100) if total_reqs else 0
        st.metric("Customer Inquiries", f"{ask_count} ({ask_pct:.0f}%)")
    with k4:
        block_pct = (blocked_count / total_reqs * 100) if total_reqs else 0
        st.metric("Blocked Breaches", f"{blocked_count} ({block_pct:.0f}%)")

    st.markdown("---")

    # Visual Charts
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("##### 📊 Gatekeeper Decision Distribution")
        if total_reqs > 0:
            df_dec = pd.DataFrame({
                "Decision": [DECISION_ALLOW, DECISION_ASK_CUSTOMER, DECISION_BLOCK],
                "Count": [allowed_count, ask_count, blocked_count]
            })
            fig_pie = px.pie(
                df_dec,
                names="Decision",
                values="Count",
                color="Decision",
                color_discrete_map={
                    DECISION_ALLOW: "#10b981",
                    DECISION_ASK_CUSTOMER: "#f59e0b",
                    DECISION_BLOCK: "#ef4444"
                },
                hole=0.45
            )
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No requests recorded yet.")

    with col_chart2:
        st.markdown("##### 📈 Activity by Action Type")
        if total_reqs > 0:
            df_req = pd.DataFrame(all_requests)
            action_counts = df_req["action"].value_counts().reset_index()
            action_counts.columns = ["Action", "Requests"]
            fig_bar = px.bar(
                action_counts,
                x="Requests",
                y="Action",
                orientation="h",
                color="Action",
                color_discrete_sequence=["#001b94", "#0077b6", "#00b4d8", "#90e0ef"]
            )
            fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No requests recorded yet.")

    st.markdown("---")
    st.markdown("#### Searchable Permanent Audit Ledger")

    # Filter Controls
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        decision_filter = st.selectbox(
            "Filter by Gatekeeper Decision:",
            options=["ALL", DECISION_ALLOW, DECISION_ASK_CUSTOMER, DECISION_BLOCK]
        )
    with col_f2:
        search_term = st.text_input("Search Logs (by Agent, PNR, or keyword):", placeholder="e.g. AGT-MMT-001 or 6E-204")

    # Filtered view of audit log
    df_logs = pd.DataFrame(all_logs)
    if not df_logs.empty:
        if decision_filter != "ALL":
            df_logs = df_logs[df_logs["decision"].fillna("").str.contains(decision_filter, case=False)]
        if search_term:
            mask = (
                df_logs["notes"].str.contains(search_term, case=False, na=False) |
                df_logs["agent_id"].fillna("").str.contains(search_term, case=False) |
                df_logs["request_id"].fillna("").str.contains(search_term, case=False)
            )
            df_logs = df_logs[mask]

        st.dataframe(
            df_logs[["log_id", "timestamp", "request_id", "agent_id", "action", "decision", "status", "notes"]],
            use_container_width=True,
            hide_index=True
        )

        # Download Audit Trail as CSV
        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Permanent Audit Log to CSV",
            data=csv_data,
            file_name=f"IndiGo_Gatekeeper_AuditLog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("Audit log is currently empty.")
