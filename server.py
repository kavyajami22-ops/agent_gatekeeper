"""
Zero-Dependency Web Server for IndiGo Agent Gatekeeper (6E Guard)
Runs on 100% Pure Python Standard Library (no pip install required!)
Includes interactive HTML5/CSS/JS Dashboard with all 4 Tabs.
"""
import sys
import os
import json
import sqlite3
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

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
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
    STATUS_APPROVED,
    STATUS_REJECTED,
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

# Initialize backend on startup
init_db()
seed_sample_data(force=False)

# Runtime config (modifiable in UI)
app_state = {
    "enrolment_id": DEFAULT_ENROLMENT_ID,
    "booking_limit": DEFAULT_PRE_APPROVED_BOOKING_LIMIT,
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IndiGo Airlines — Agent Gatekeeper</title>
    <style>
        :root {
            --indigo-blue: #001b94;
            --indigo-light: #0040c1;
            --accent-blue: #0077b6;
            --bg-gray: #f8fafc;
            --text-dark: #0f172a;
            --card-border: #e2e8f0;
            --allow-green: #10b981;
            --ask-amber: #f59e0b;
            --block-red: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg-gray); color: var(--text-dark); line-height: 1.5; }
        
        .header {
            background: linear-gradient(135deg, var(--indigo-blue) 0%, var(--indigo-light) 60%, var(--accent-blue) 100%);
            color: white; padding: 20px 30px; box-shadow: 0 4px 12px rgba(0,27,148,0.2);
        }
        .header h1 { font-size: 24px; font-weight: 700; }
        .header p { font-size: 14px; opacity: 0.9; margin-top: 4px; }
        .badges { margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap; }
        .badge {
            background: #ffd166; color: var(--indigo-blue); font-weight: 800;
            padding: 4px 14px; border-radius: 20px; font-size: 13px;
        }
        .pill {
            background: rgba(255,255,255,0.2); color: white; padding: 4px 12px;
            border-radius: 20px; font-size: 13px; border: 1px solid rgba(255,255,255,0.3);
        }

        .container { max-width: 1250px; margin: 20px auto; padding: 0 20px; }

        /* Tabs */
        .tabs { display: flex; gap: 8px; border-bottom: 2px solid #e2e8f0; margin-bottom: 20px; }
        .tab-btn {
            background: none; border: none; padding: 12px 20px; font-size: 15px; font-weight: 600;
            color: #64748b; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s;
        }
        .tab-btn:hover { color: var(--indigo-blue); }
        .tab-btn.active { color: var(--indigo-blue); border-bottom-color: var(--indigo-blue); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* Cards */
        .card {
            background: white; border: 1px solid var(--card-border); border-radius: 10px;
            padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .card h3 { font-size: 18px; margin-bottom: 12px; color: var(--indigo-blue); }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 850px) { .grid-2 { grid-template-columns: 1fr; } }

        /* Form elements */
        label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 4px; color: #334155; }
        input, select {
            width: 100%; padding: 9px 12px; border: 1px solid #cbd5e1; border-radius: 6px;
            font-size: 14px; margin-bottom: 14px; background: white;
        }
        .btn {
            padding: 10px 18px; font-size: 14px; font-weight: 600; border-radius: 6px;
            border: none; cursor: pointer; transition: 0.2s;
        }
        .btn-primary { background: var(--indigo-blue); color: white; }
        .btn-primary:hover { background: var(--indigo-light); }
        .btn-success { background: var(--allow-green); color: white; }
        .btn-danger { background: var(--block-red); color: white; }
        .btn-warning { background: var(--ask-amber); color: white; }
        .btn-outline { background: white; border: 1px solid #cbd5e1; color: #334155; }

        /* Verdict card */
        .verdict-box {
            padding: 20px; border-radius: 10px; margin-top: 15px; border-left: 6px solid #cbd5e1;
        }
        .verdict-ALLOW { background: #ecfdf5; border-left-color: var(--allow-green); }
        .verdict-ASK { background: #fffbeb; border-left-color: var(--ask-amber); }
        .verdict-BLOCK { background: #fef2f2; border-left-color: var(--block-red); }

        /* Tables */
        table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 10px; }
        th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background: #f1f5f9; color: #475569; font-weight: 600; }
        tr:hover { background: #f8fafc; }

        /* KPIs */
        .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
        .kpi-tile { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }
        .kpi-tile .num { font-size: 26px; font-weight: 700; color: var(--indigo-blue); }
        .kpi-tile .lbl { font-size: 13px; color: #64748b; margin-top: 4px; }

        .pending-item {
            border: 1px solid var(--ask-amber); background: #fffdf5; border-radius: 8px;
            padding: 16px; margin-bottom: 14px;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="max-width: 1250px; margin: 0 auto;">
        <h1>✈️ IndiGo Airlines — Autonomous AI Agent Gatekeeper</h1>
        <p>Intelligent Zero-Trust Permission Gateway & Policy Interceptor for Third-Party AI Agents</p>
        <div class="badges">
            <span class="badge" id="bannerEnrolment">🎓 Enrolment No: Loading...</span>
            <span class="pill">🛡️ Mode: Safe Educational Simulation</span>
            <span class="pill" id="bannerThreshold">⚡ Booking Threshold: ₹8,000</span>
        </div>
    </div>
</div>

<div class="container">
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab(1)">🛫 Tab 1: Live Agent Simulator</button>
        <button class="tab-btn" onclick="switchTab(2)" id="tab2Btn">👤 Tab 2: Confirmation Inbox (0)</button>
        <button class="tab-btn" onclick="switchTab(3)">🤖 Tab 3: Agent Directory & Revocation</button>
        <button class="tab-btn" onclick="switchTab(4)">📜 Tab 4: Audit Log & Analytics</button>
        <button class="tab-btn" onclick="switchTab(5)">⚙️ Settings & Reset</button>
    </div>

    <!-- TAB 1: SIMULATOR -->
    <div class="tab-content active" id="tab1">
        <div class="grid-2">
            <div class="card">
                <h3>1. Inbound Request Configuration</h3>
                <label>Select External AI Agent:</label>
                <select id="simAgentSelect" onchange="onAgentChanged()"></select>
                <div id="simAgentInfo" style="font-size: 12px; background: #f1f5f9; padding: 8px; border-radius: 6px; margin-bottom: 12px;"></div>

                <label>Select Action:</label>
                <select id="simActionSelect" onchange="onActionChanged()">
                    <option value="View flight fares">1. View flight fares (Read-Only)</option>
                    <option value="Book a flight" selected>2. Book a flight (Financial)</option>
                    <option value="Change a flight booking">3. Change a flight booking (Schedule Change)</option>
                    <option value="Request a refund">4. Request a refund (Seat Cancellation)</option>
                </select>

                <label>Choose Flight / Preset Itinerary:</label>
                <select id="simFlightPreset" onchange="onPresetChanged()"></select>

                <div class="grid-2">
                    <div>
                        <label>PNR / Booking Reference:</label>
                        <input type="text" id="simPnr" value="6E-M9K2L">
                    </div>
                    <div>
                        <label>Transaction Amount (₹):</label>
                        <input type="number" id="simAmount" value="7200" step="500">
                    </div>
                </div>

                <button class="btn btn-primary" style="width: 100%;" onclick="dispatchSimRequest()">🚀 Dispatch Request to Gatekeeper</button>
            </div>

            <div class="card">
                <h3>2. Gatekeeper Policy Evaluation</h3>
                <div id="verdictContainer">
                    <p style="color: #64748b; font-size: 14px;">Select parameters on the left and click <strong>Dispatch Request</strong> to observe the Gatekeeper's real-time evaluation.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: PENDING APPROVALS -->
    <div class="tab-content" id="tab2">
        <div class="card">
            <h3>👤 Passenger Confirmation Inbox (Human-in-the-Loop)</h3>
            <p style="color: #475569; font-size: 14px; margin-bottom: 15px;">
                Actions marked as <strong>ASK CUSTOMER</strong> (bookings > threshold, flight changes, and refunds) require passenger confirmation here.
            </p>
            <div id="pendingList"></div>
        </div>
    </div>

    <!-- TAB 3: AGENT DIRECTORY & REVOCATION -->
    <div class="tab-content" id="tab3">
        <div class="card">
            <h3>🤖 Registered Agent Directory</h3>
            <div style="overflow-x: auto;">
                <table id="agentsTable">
                    <thead>
                        <tr>
                            <th>Agent ID</th><th>Name</th><th>Developer</th><th>Status</th>
                            <th>Fares</th><th>Book</th><th>Change</th><th>Refund</th>
                            <th>Limit (₹)</th><th>Registered At</th><th>Revoked At</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <h3>🚨 Revocation Kill-Switch</h3>
                <label>Select Agent to Manage:</label>
                <select id="revokeAgentSelect"></select>
                <button class="btn btn-danger" onclick="toggleAgentRevocation('REVOKED')">🚨 Revoke Agent Access</button>
                <button class="btn btn-success" onclick="toggleAgentRevocation('ACTIVE')">✅ Reactivate Agent</button>
            </div>

            <div class="card">
                <h3>➕ Register New Customer AI Agent</h3>
                <label>Agent Name:</label>
                <input type="text" id="newAgentName" placeholder="e.g. Cleartrip Autonomous Bot">
                <label>Developer Organization:</label>
                <input type="text" id="newAgentDev" placeholder="e.g. Cleartrip India">
                <label>Spending Limit (₹):</label>
                <input type="number" id="newAgentLimit" value="8000">
                <button class="btn btn-primary" onclick="registerNewAgent()">Register Agent</button>
            </div>
        </div>
    </div>

    <!-- TAB 4: AUDIT LOG -->
    <div class="tab-content" id="tab4">
        <div class="kpi-row">
            <div class="kpi-tile"><div class="num" id="kpiTotal">0</div><div class="lbl">Total Interceptions</div></div>
            <div class="kpi-tile"><div class="num" id="kpiAllowed" style="color: var(--allow-green);">0</div><div class="lbl">Auto-Allowed (ALLOW)</div></div>
            <div class="kpi-tile"><div class="num" id="kpiAsk" style="color: var(--ask-amber);">0</div><div class="lbl">Customer Inquiries</div></div>
            <div class="kpi-tile"><div class="num" id="kpiBlocked" style="color: var(--block-red);">0</div><div class="lbl">Blocked Violations</div></div>
        </div>

        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>📜 Permanent Audit Log (Immutable Ledger)</h3>
                <a href="/api/export-csv" class="btn btn-primary" download style="text-decoration: none;">📥 Export CSV</a>
            </div>
            <div style="overflow-x: auto; max-height: 450px; overflow-y: auto;">
                <table id="auditTable">
                    <thead>
                        <tr>
                            <th>Log ID</th><th>Timestamp</th><th>Request ID</th><th>Agent ID</th>
                            <th>Action</th><th>Decision</th><th>Status</th><th>Notes</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- TAB 5: SETTINGS -->
    <div class="tab-content" id="tab5">
        <div class="card">
            <h3>⚙️ Academic & Policy Settings</h3>
            <label>Student Enrolment ID (Configurable):</label>
            <input type="text" id="cfgEnrolment" value="PGD202564221">

            <label>Pre-Approved Booking Limit (₹):</label>
            <input type="number" id="cfgLimit" value="8000" step="500">

            <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #e2e8f0;"/>
            <button class="btn btn-outline" onclick="resetDemo()">🔄 Reset Database & Re-seed Sample Data</button>
        </div>
    </div>
</div>

<script>
let stateData = {};

function switchTab(idx) {
    document.querySelectorAll('.tab-btn').forEach((b, i) => b.classList.toggle('active', i === idx-1));
    document.querySelectorAll('.tab-content').forEach((c, i) => c.classList.toggle('active', i === idx-1));
    if (idx === 2 || idx === 3 || idx === 4) loadState();
}

async function loadState() {
    try {
        const res = await fetch('/api/state');
        stateData = await res.json();
        renderState();
    } catch (e) {
        console.error('Failed to load state', e);
    }
}

function renderState() {
    // Header
    document.getElementById('bannerEnrolment').innerText = '🎓 Enrolment No: ' + stateData.config.enrolment_id;
    document.getElementById('bannerThreshold').innerText = '⚡ Booking Threshold: ₹' + Number(stateData.config.booking_limit).toLocaleString('en-IN');
    document.getElementById('cfgEnrolment').value = stateData.config.enrolment_id;
    document.getElementById('cfgLimit').value = stateData.config.booking_limit;

    // Agent dropdown
    const agentSelect = document.getElementById('simAgentSelect');
    const revokeSelect = document.getElementById('revokeAgentSelect');
    agentSelect.innerHTML = '';
    revokeSelect.innerHTML = '';

    stateData.agents.forEach(a => {
        const opt1 = new Option(`${a.name} (${a.agent_id}) — ${a.status}`, a.agent_id);
        const opt2 = new Option(`${a.name} (${a.agent_id}) — ${a.status}`, a.agent_id);
        agentSelect.add(opt1);
        revokeSelect.add(opt2);
    });
    onAgentChanged();

    // Flight presets
    const flightSelect = document.getElementById('simFlightPreset');
    if (flightSelect.options.length === 0) {
        stateData.sample_flights.forEach((f, i) => {
            const opt = new Option(`${f.route} | ${f.flight_no} (${f.class}) — ₹${f.fare.toLocaleString('en-IN')}`, i);
            flightSelect.add(opt);
        });
    }

    // Pending Requests (Tab 2)
    const pending = stateData.pending_requests;
    document.getElementById('tab2Btn').innerText = `👤 Tab 2: Confirmation Inbox (${pending.length})`;
    const pendingContainer = document.getElementById('pendingList');
    if (pending.length === 0) {
        pendingContainer.innerHTML = '<div style="color: #10b981; font-weight: 600;">🎉 All clear! No requests currently waiting for customer confirmation.</div>';
    } else {
        pendingContainer.innerHTML = pending.map(r => `
            <div class="pending-item">
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: #92400e;">
                    <span>⚠️ Pending Action: ${r.action}</span>
                    <span>Req ID: ${r.request_id}</span>
                </div>
                <div style="margin: 8px 0; font-size: 14px;">
                    <strong>Agent:</strong> ${r.agent_name || r.agent_id} | <strong>PNR:</strong> <code>${r.pnr}</code><br/>
                    <strong>Details:</strong> ${r.flight_details}<br/>
                    <strong>Transaction Amount:</strong> <span style="font-size: 16px; font-weight: bold; color: #001b94;">₹${Number(r.amount).toLocaleString('en-IN')}</span><br/>
                    <small style="color: #64748b;">${r.reason}</small>
                </div>
                <div>
                    <button class="btn btn-success" onclick="resolveRequest('${r.request_id}', 'APPROVE')">✅ Approve Action</button>
                    <button class="btn btn-danger" onclick="resolveRequest('${r.request_id}', 'REJECT')">❌ Reject Action</button>
                </div>
            </div>
        `).join('');
    }

    // Agents Table (Tab 3)
    const tbodyAgents = document.querySelector('#agentsTable tbody');
    tbodyAgents.innerHTML = stateData.agents.map(a => `
        <tr>
            <td><code>${a.agent_id}</code></td>
            <td><strong>${a.name}</strong></td>
            <td>${a.developer}</td>
            <td><span style="font-weight: bold; color: ${a.status === 'ACTIVE' ? '#10b981' : '#ef4444'}">${a.status}</span></td>
            <td>${a.can_view_fares ? '✅' : '❌'}</td>
            <td>${a.can_book ? '✅' : '❌'}</td>
            <td>${a.can_change_booking ? '✅' : '❌'}</td>
            <td>${a.can_request_refund ? '✅' : '❌'}</td>
            <td>₹${Number(a.custom_spending_limit).toLocaleString('en-IN')}</td>
            <td><small>${a.registered_at}</small></td>
            <td><small>${a.revoked_at || '—'}</small></td>
        </tr>
    `).join('');

    // KPIs & Audit Table (Tab 4)
    const total = stateData.requests.length;
    const allowed = stateData.requests.filter(r => r.gatekeeper_decision === 'ALLOW').length;
    const ask = stateData.requests.filter(r => r.gatekeeper_decision === 'ASK CUSTOMER').length;
    const blocked = stateData.requests.filter(r => r.gatekeeper_decision === 'BLOCK').length;

    document.getElementById('kpiTotal').innerText = total;
    document.getElementById('kpiAllowed').innerText = allowed;
    document.getElementById('kpiAsk').innerText = ask;
    document.getElementById('kpiBlocked').innerText = blocked;

    const tbodyAudit = document.querySelector('#auditTable tbody');
    tbodyAudit.innerHTML = stateData.audit_logs.map(l => `
        <tr>
            <td>${l.log_id}</td>
            <td><small>${l.timestamp}</small></td>
            <td><code>${l.request_id || '—'}</code></td>
            <td>${l.agent_id || '—'}</td>
            <td>${l.action || '—'}</td>
            <td><strong style="color: ${l.decision === 'ALLOW' ? '#10b981' : l.decision === 'BLOCK' ? '#ef4444' : '#f59e0b'}">${l.decision || '—'}</strong></td>
            <td>${l.status || '—'}</td>
            <td><small>${l.notes}</small></td>
        </tr>
    `).join('');
}

function onAgentChanged() {
    const aid = document.getElementById('simAgentSelect').value;
    const a = stateData.agents.find(x => x.agent_id === aid);
    if (!a) return;
    document.getElementById('simAgentInfo').innerHTML = `
        <strong>Developer:</strong> ${a.developer} | <strong>Status:</strong> ${a.status} | 
        <strong>Permissions:</strong> Fares: ${a.can_view_fares?'✅':'❌'}, Book: ${a.can_book?'✅':'❌'}, Change: ${a.can_change_booking?'✅':'❌'}, Refund: ${a.can_request_refund?'✅':'❌'}
    `;
}

function onActionChanged() {
    const act = document.getElementById('simActionSelect').value;
    if (act === 'View flight fares') {
        document.getElementById('simAmount').value = 0;
    } else {
        onPresetChanged();
    }
}

function onPresetChanged() {
    const idx = document.getElementById('simFlightPreset').value;
    const f = stateData.sample_flights[idx];
    if (f && document.getElementById('simActionSelect').value !== 'View flight fares') {
        document.getElementById('simAmount').value = f.fare;
    }
}

async function dispatchSimRequest() {
    const aid = document.getElementById('simAgentSelect').value;
    const act = document.getElementById('simActionSelect').value;
    const pnr = document.getElementById('simPnr').value;
    const amt = parseFloat(document.getElementById('simAmount').value) || 0;
    const idx = document.getElementById('simFlightPreset').value;
    const f = stateData.sample_flights[idx];
    const details = `${f.route} | Flight ${f.flight_no} (${f.class})`;

    const res = await fetch('/api/dispatch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ agent_id: aid, action: act, pnr, amount: amt, flight_details: details })
    });
    const result = await res.json();

    const vClass = result.decision === 'ALLOW' ? 'verdict-ALLOW' : result.decision === 'BLOCK' ? 'verdict-BLOCK' : 'verdict-ASK';
    const vIcon = result.decision === 'ALLOW' ? '🟢' : result.decision === 'BLOCK' ? '🔴' : '🟡';

    document.getElementById('verdictContainer').innerHTML = `
        <div class="verdict-box ${vClass}">
            <h2 style="margin-bottom: 8px;">${vIcon} VERDICT: ${result.decision}</h2>
            <p><strong>Status:</strong> ${result.status} | <strong>Request ID:</strong> <code>${result.request_id}</code></p>
            <p style="margin-top: 10px;"><strong>Policy Rationale:</strong><br/>${result.reason}</p>
        </div>
        <div style="margin-top: 12px; font-size: 13px; color: #475569;">
            ${result.decision === 'ASK CUSTOMER' ? '👉 Request forwarded to <strong>Tab 2: Confirmation Inbox</strong>.' : 'Recorded in permanent audit log.'}
        </div>
    `;
    loadState();
}

async function resolveRequest(reqId, action) {
    await fetch('/api/customer-action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ request_id: reqId, action: action })
    });
    loadState();
}

async function toggleAgentRevocation(status) {
    const aid = document.getElementById('revokeAgentSelect').value;
    await fetch('/api/toggle-agent', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ agent_id: aid, status: status })
    });
    loadState();
}

async function registerNewAgent() {
    const name = document.getElementById('newAgentName').value;
    const dev = document.getElementById('newAgentDev').value;
    const limit = parseFloat(document.getElementById('newAgentLimit').value) || 8000;
    if (!name || !dev) { alert('Please enter name and developer'); return; }

    await fetch('/api/register-agent', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, developer: dev, limit })
    });
    document.getElementById('newAgentName').value = '';
    document.getElementById('newAgentDev').value = '';
    loadState();
}

async function saveSettings() {
    const enrolment = document.getElementById('cfgEnrolment').value;
    const limit = parseFloat(document.getElementById('cfgLimit').value) || 8000;
    await fetch('/api/update-config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ enrolment_id: enrolment, booking_limit: limit })
    });
    alert('Settings saved!');
    loadState();
}

async function resetDemo() {
    if (!confirm('Reset database to clean sample data?')) return;
    await fetch('/api/reset', { method: 'POST' });
    alert('Database reset!');
    loadState();
}

loadState();
</script>
</body>
</html>
"""

class GatekeeperHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif path == "/api/state":
            data = {
                "config": app_state,
                "agents": get_all_agents(),
                "pending_requests": get_pending_requests(),
                "requests": get_all_requests(),
                "audit_logs": get_all_audit_logs(),
                "sample_flights": SAMPLE_FLIGHTS,
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif path == "/api/export-csv":
            logs = get_all_audit_logs()
            csv_lines = ["log_id,timestamp,request_id,agent_id,action,event_type,decision,status,notes"]
            for l in logs:
                notes_clean = f'"{l["notes"].replace(chr(34), chr(39))}"'
                csv_lines.append(f"{l['log_id']},{l['timestamp']},{l['request_id']},{l['agent_id']},{l['action']},{l['event_type']},{l['decision']},{l['status']},{notes_clean}")
            csv_data = "\n".join(csv_lines).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", "attachment; filename=IndiGo_Gatekeeper_AuditLog.csv")
            self.end_headers()
            self.wfile.write(csv_data)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body) if body else {}

        if path == "/api/dispatch":
            engine = GatekeeperEngine(booking_threshold=app_state["booking_limit"])
            verdict = engine.evaluate_request(
                agent_id=payload.get("agent_id"),
                action=payload.get("action"),
                customer_id=payload.get("customer_id", "CUST-6E-801"),
                pnr=payload.get("pnr", "6E-DEMO"),
                flight_details=payload.get("flight_details", "General Flight Inquiry"),
                amount=float(payload.get("amount", 0.0)),
                booking_threshold_override=app_state["booking_limit"]
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(verdict).encode("utf-8"))

        elif path == "/api/customer-action":
            req_id = payload.get("request_id")
            action = payload.get("action", "APPROVE")
            update_request_decision_by_customer(req_id, action, "Customer confirmed in Web Portal")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        elif path == "/api/toggle-agent":
            aid = payload.get("agent_id")
            status = payload.get("status", "ACTIVE")
            reason = "Administrative policy toggle via Portal"
            update_agent_status(aid, status, reason=reason)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        elif path == "/api/register-agent":
            name = payload.get("name")
            dev = payload.get("developer")
            limit = float(payload.get("limit", 8000))
            aid = f"AGT-CUSTOM-{len(get_all_agents())+1:03d}"
            register_agent(
                agent_id=aid,
                name=name,
                developer=dev,
                custom_spending_limit=limit,
                status=AGENT_STATUS_ACTIVE
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "agent_id": aid}).encode("utf-8"))

        elif path == "/api/update-config":
            if "enrolment_id" in payload:
                app_state["enrolment_id"] = payload["enrolment_id"]
            if "booking_limit" in payload:
                app_state["booking_limit"] = float(payload["booking_limit"])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "config": app_state}).encode("utf-8"))

        elif path == "/api/reset":
            reset_database()
            seed_sample_data(force=True)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8501):
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, GatekeeperHTTPHandler)
    except OSError:
        # Fallback port if 8501 is busy
        port = 8000
        server_address = ("127.0.0.1", port)
        httpd = HTTPServer(server_address, GatekeeperHTTPHandler)

    print("=" * 65)
    print(f"✈️  IndiGo Airlines — Agent Gatekeeper Web Server Started!")
    print(f"🎓 Enrolment Number: {app_state['enrolment_id']}")
    print(f"⚡ Policy Booking Limit: ₹{app_state['booking_limit']:,.0f}")
    print(f"🔗 Open your browser at: http://localhost:{port}")
    print("=" * 65)
    httpd.serve_forever()

if __name__ == "__main__":
    port = 8501
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
