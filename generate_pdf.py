"""
PDF Generator for IndiGo Airlines Agent Gatekeeper Report (6E Guard)
Zero-dependency, pure standard library script.
Generates an exact 2-page A4 PDF compliant with the PDF-1.4 specification.
"""
import os
import sys

def build_pdf():
    # PDF 1.4 objects storage
    objects = []
    
    def add_obj(content):
        objects.append(content)
        return len(objects)

    # 1. Catalog
    add_obj("<< /Type /Catalog /Pages 2 0 R >>")
    # 2. Pages
    add_obj("<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>")
    # 3. Page 1 (Placeholder, updated below)
    add_obj("")
    # 4. Page 2 (Placeholder, updated below)
    add_obj("")
    # 5. Content Stream Page 1 (Placeholder)
    add_obj("")
    # 6. Content Stream Page 2 (Placeholder)
    add_obj("")
    # 7. Resources
    add_obj("<< /Font << /F1 8 0 R /F2 9 0 R /F3 10 0 R >> /ProcSet [/PDF /Text /ImageC] >>")
    # 8. Font F1 (Helvetica)
    add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    # 9. Font F2 (Helvetica-Bold)
    add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    # 10. Font F3 (Helvetica-Oblique)
    add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")

    # Update Page 1 & Page 2 definitions
    objects[2] = "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 5 0 R /Resources 7 0 R >>"
    objects[3] = "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 6 0 R /Resources 7 0 R >>"

    # -------------------------------------------------------------
    # PAGE 1 CONTENT STREAM
    # -------------------------------------------------------------
    p1 = []
    
    # Header Banner Background
    p1.append("q")
    p1.append("0.0 0.106 0.58 rg")  # IndiGo Navy Blue
    p1.append("36 740 523.28 72 re f")
    
    # Gold Enrolment Badge
    p1.append("1.0 0.82 0.4 rg")     # Gold
    p1.append("48 748 215 17 re f")
    
    # Enrolment Text
    p1.append("BT /F2 8.5 Tf 0.0 0.106 0.58 rg 56 753.5 Td (Candidate Enrolment ID: PGD202564221) Tj ET")
    
    # Simulation Pill
    p1.append("0.15 0.3 0.7 rg")
    p1.append("270 748 185 17 re f")
    p1.append("BT /F1 8 Tf 1 1 1 rg 278 753.5 Td (Simulation Mode: Educational Sandbox) Tj ET")

    # Title & Subtitle in Banner
    p1.append("BT /F2 15 Tf 1 1 1 rg 48 788 Td (IndiGo Airlines - Agent Gatekeeper \\(6E Guard\\)) Tj ET")
    p1.append("BT /F1 8.5 Tf 0.9 0.95 1 rg 48 774 Td (MBA Project Report | Emerging Tech & Autonomous AI Agent Governance System) Tj ET")
    p1.append("Q")

    # SECTION 1: Executive Summary & Business Problem
    p1.append("q")
    p1.append("0.0 0.106 0.58 rg 36 718 523.28 1.5 re f")  # Accent line
    p1.append("BT /F2 11 Tf 0.0 0.106 0.58 rg 36 724 Td (1. Executive Summary & Business Problem) Tj ET")
    
    # Prose lines
    y = 704
    p1.append(f"BT /F1 8 Tf 0.15 0.18 0.22 rg 36 {y} Td (As consumer travel booking transitions from manual web searches to autonomous AI agents \\(e.g., MakeMyTrip bots, Expedia concierges,) Tj ET")
    y -= 11
    p1.append(f"BT /F1 8 Tf 0.15 0.18 0.22 rg 36 {y} Td (and Google Gemini personal assistants\\), commercial airlines face an unprecedented governance challenge. Autonomous agents can search,) Tj ET")
    y -= 11
    p1.append(f"BT /F1 8 Tf 0.15 0.18 0.22 rg 36 {y} Td (book, modify, and cancel flights on behalf of passengers. While frictionless, this introduces critical operational and commercial risks:) Tj ET")
    
    # Bullets
    bullets_s1 = [
        ("Financial Risk & Hallucination Exposure:", "Agents may misinterpret intent or hallucinate booking criteria, causing unexpected charges."),
        ("Operational & Itinerary Disruption:", "Arbitrary schedule changes disrupt itineraries, risk missed connections, and incur airline fees."),
        ("Irreversible Inventory Depletion:", "Cancellations and refunds release airline seat inventory and trigger payouts, demanding strict oversight.")
    ]
    y -= 14
    for b_title, b_desc in bullets_s1:
        p1.append(f"BT /F2 8 Tf 0.0 0.106 0.58 rg 46 {y} Td (\\(o\\) {b_title}) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( {b_desc}) Tj ET")
        y -= 11

    # Gray Callout Box for Simulation Notice
    y -= 4
    box_h = 32
    p1.append(f"0.95 0.96 0.98 rg 36 {y - box_h + 8} 523.28 {box_h} re f")
    p1.append(f"0.8 0.84 0.88 RG 0.75 w 36 {y - box_h + 8} 523.28 {box_h} re S")
    p1.append(f"BT /F2 7.5 Tf 0.6 0.2 0.0 rg 44 {y - 4} Td (EDUCATIONAL SIMULATION NOTICE:) Tj /F1 7.5 Tf 0.25 0.25 0.25 rg ( This project is an educational simulation developed strictly for academic evaluation.) Tj ET")
    p1.append(f"BT /F1 7.5 Tf 0.25 0.25 0.25 rg 44 {y - 15} Td (It operates in a local sandboxed environment. No real airline reservation systems \\(PSS/GDS\\), live inventory, or banking gateways are touched.) Tj ET")
    p1.append("Q")

    # SECTION 2: Project Objectives
    y -= 46
    p1.append("q")
    p1.append(f"0.0 0.106 0.58 rg 36 {y} 523.28 1.5 re f")
    p1.append(f"BT /F2 11 Tf 0.0 0.106 0.58 rg 36 {y + 6} Td (2. Project Objectives) Tj ET")
    
    objs = [
        ("Tri-State Deterministic Governance:", "Classify all inbound AI agent requests into ALLOW, ASK CUSTOMER, or BLOCK."),
        ("Pre-Approved Spending Controls:", "Automate low-risk transactions while holding bookings above an initial limit of Rs. 8,000."),
        ("Mandatory Human-in-the-Loop:", "Enforce explicit passenger confirmation on all flight changes and refund requests."),
        ("Agent Governance & Kill-Switch:", "Provide one-click administrative revocation of compromised agents with permanent timestamps."),
        ("Regulatory Auditability:", "Maintain an immutable, permanent SQLite audit log guaranteeing non-repudiation and compliance.")
    ]
    y -= 13
    for o_title, o_desc in objs:
        p1.append(f"BT /F2 8 Tf 0.0 0.106 0.58 rg 46 {y} Td (\\(o\\) {o_title}) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( {o_desc}) Tj ET")
        y -= 11.5
    p1.append("Q")

    # SECTION 3: How the Gatekeeper Works (System Workflow)
    y -= 4
    p1.append("q")
    p1.append(f"0.0 0.106 0.58 rg 36 {y} 523.28 1.5 re f")
    p1.append(f"BT /F2 11 Tf 0.0 0.106 0.58 rg 36 {y + 6} Td (3. How the Gatekeeper Works \\(Four-Stage Policy Evaluation Flow\\)) Tj ET")
    
    steps = [
        ("Step 1 - Identity & Status Verification:", "Gatekeeper checks agent directory. If status is REVOKED or SUSPENDED, request is instantly BLOCKED."),
        ("Step 2 - Permission Scope Verification:", "Verifies agent has active scope for the action (View Fares, Book, Change, Refund). If missing, request is BLOCKED."),
        ("Step 3 - Risk Matrix & Threshold Evaluation:", "Fares: ALLOW (read-only). Bookings <= Rs. 8,000: ALLOW. Bookings > Rs. 8,000: ASK CUSTOMER. Changes & Refunds: strictly ASK CUSTOMER."),
        ("Step 4 - Customer Confirmation & Audit:", "Pending requests enter passenger inbox. Approval/Rejection updates simulated state and appends immutable audit log.")
    ]
    y -= 13
    for s_title, s_desc in steps:
        p1.append(f"BT /F2 8 Tf 0.0 0.106 0.58 rg 46 {y} Td ({s_title}) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( {s_desc}) Tj ET")
        y -= 11.5
    p1.append("Q")

    # Page 1 Footer
    p1.append("q")
    p1.append("0.8 0.82 0.85 RG 0.5 w 36 38 523.28 0 re S")
    p1.append("BT /F1 7.5 Tf 0.45 0.5 0.55 rg 36 28 Td (IndiGo Airlines \\(6E Guard\\) - MBA Assignment Documentation | Candidate Enrolment ID: PGD202564221) Tj ET")
    p1.append("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 520 28 Td (Page 1 of 2) Tj ET")
    p1.append("Q")

    # -------------------------------------------------------------
    # PAGE 2 CONTENT STREAM
    # -------------------------------------------------------------
    p2 = []
    
    # Page 2 Top Header
    p2.append("q")
    p2.append("BT /F2 8.5 Tf 0.0 0.106 0.58 rg 36 808 Td (IndiGo Airlines - Agent Gatekeeper \\(6E Guard\\) | Technical & Empirical Report) Tj ET")
    p2.append("BT /F2 8.5 Tf 0.6 0.3 0.0 rg 420 808 Td (Candidate Enrolment ID: PGD202564221) Tj ET")
    p2.append("0.8 0.82 0.85 RG 0.5 w 36 802 523.28 0 re S")
    p2.append("Q")

    # SECTION 4: Technology Stack & Architecture
    y2 = 786
    p2.append("q")
    p2.append(f"0.0 0.106 0.58 rg 36 {y2} 523.28 1.5 re f")
    p2.append(f"BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 {y2 + 5} Td (4. Technology Stack & Architecture) Tj ET")
    
    tech_items = [
        ("Programming Language:", "Python 3.11 with clean modular separation (core/config.py, core/database.py, core/gatekeeper.py)."),
        ("Persistent Database:", "SQLite (sqlite3 built-in), ACID relational persistence, permanent registered_at & revoked_at timestamps."),
        ("Zero-Dependency Server:", "Built-in Python http.server (server.py) serving responsive HTML5/CSS/JS dashboard at http://localhost:8501."),
        ("Streamlit Interface:", "Streamlit dashboard (app.py) with Plotly analytics for environments with optional packages installed.")
    ]
    y2 -= 12
    for t_title, t_desc in tech_items:
        p2.append(f"BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 {y2} Td (\\(o\\) {t_title}) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( {t_desc}) Tj ET")
        y2 -= 10
    p2.append("Q")

    # SECTION 5: Key Functional Modules
    y2 -= 4
    p2.append("q")
    p2.append(f"0.0 0.106 0.58 rg 36 {y2} 523.28 1.5 re f")
    p2.append(f"BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 {y2 + 5} Td (5. Key Functional Modules \\(The 4 Dashboard Tabs\\)) Tj ET")
    
    modules = [
        ("Tab 1 - Live Agent Simulator:", "Dispatch simulated requests across all 4 actions; observe real-time ALLOW, ASK, or BLOCK verdict cards."),
        ("Tab 2 - Confirmation Inbox:", "Human-in-the-loop passenger inbox where held actions are reviewed and confirmed with Approve/Reject buttons."),
        ("Tab 3 - Governance & Kill-Switch:", "Onboard new customer AI agents, configure action scopes, and invoke the one-click emergency revocation switch."),
        ("Tab 4 - Audit Log & Analytics:", "Searchable immutable transaction ledger with decision distribution chart and one-click CSV compliance export.")
    ]
    y2 -= 12
    for m_title, m_desc in modules:
        p2.append(f"BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 {y2} Td (\\(o\\) {m_title}) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( {m_desc}) Tj ET")
        y2 -= 10
    p2.append("Q")

    # SECTION 6: Empirical Testing & Validation Results (Table)
    y2 -= 4
    p2.append("q")
    p2.append(f"0.0 0.106 0.58 rg 36 {y2} 523.28 1.5 re f")
    p2.append(f"BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 {y2 + 5} Td (6. Empirical Testing & Validation Results \\(Automated Test Suite: test_gatekeeper.py\\)) Tj ET")
    
    # Table Header Box
    y_table = y2 - 17
    row_h = 13.5
    p2.append(f"0.0 0.106 0.58 rg 36 {y_table} 523.28 {row_h} re f")
    p2.append(f"BT /F2 7 Tf 1 1 1 rg 40 {y_table + 4} Td (Test ID) Tj 78 {y_table + 4} Td (Scenario Description) Tj 225 {y_table + 4} Td (Input Parameters) Tj 355 {y_table + 4} Td (Expected Verdict) Tj 455 {y_table + 4} Td (Actual Test Result) Tj ET")
    
    tests = [
        ("T-01", "Database schema initialization", "SQLite schema & seed data", "5 Seeded Agents", "Passed (5 loaded)"),
        ("T-02", "Action 1: View flight fares", "AGT-MMT-001, Fare Query", "ALLOW", "Passed (EXECUTED)"),
        ("T-03", "Action 2: Booking <= Rs. 8,000", "AGT-MMT-001, Rs. 4,800 fare", "ALLOW", "Passed (EXECUTED)"),
        ("T-04", "Action 2: Booking > Rs. 8,000", "AGT-MMT-001, Rs. 9,500 fare", "ASK CUSTOMER", "Passed (PENDING)"),
        ("T-05", "Action 3: Flight change request", "AGT-MMT-001, Rs. 1,200 fee", "ASK CUSTOMER", "Passed (PENDING)"),
        ("T-06", "Action 4: Refund request", "AGT-MMT-001, Rs. 4,800 refund", "ASK CUSTOMER", "Passed (PENDING)"),
        ("T-07", "Revoked agent lockdown", "AGT-ROG-005, Fare Query", "BLOCK", "Passed (Access Denied)"),
        ("T-08", "Dynamic Kill-Switch & Timestamps", "Revoke AGT-EXP-002", "Timestamp & BLOCK", "Passed (Timestamp logged)"),
        ("T-09", "Human-in-the-Loop approval", "Approve pending REQ-6E", "Status -> APPROVED", "Passed (State updated)"),
        ("T-10", "Permanent Audit Log integrity", "Query all audit_log rows", "Immutable Ledger", "Passed (All events logged)")
    ]
    
    y_curr = y_table - row_h
    for idx, (t_id, t_desc, t_param, t_exp, t_res) in enumerate(tests):
        bg = "0.96 0.97 0.99" if idx % 2 == 0 else "1.0 1.0 1.0"
        p2.append(f"{bg} rg 36 {y_curr} 523.28 {row_h} re f")
        p2.append(f"0.88 0.9 0.92 RG 0.4 w 36 {y_curr} 523.28 {row_h} re S")
        p2.append(f"BT /F2 6.5 Tf 0.1 0.15 0.2 rg 40 {y_curr + 4} Td ({t_id}) Tj ET")
        p2.append(f"BT /F1 6.5 Tf 0.2 0.2 0.2 rg 78 {y_curr + 4} Td ({t_desc}) Tj ET")
        p2.append(f"BT /F1 6.5 Tf 0.3 0.3 0.3 rg 225 {y_curr + 4} Td ({t_param}) Tj ET")
        p2.append(f"BT /F2 6.5 Tf 0.0 0.106 0.58 rg 355 {y_curr + 4} Td ({t_exp}) Tj ET")
        p2.append(f"BT /F2 6.5 Tf 0.06 0.6 0.3 rg 455 {y_curr + 4} Td ({t_res}) Tj ET")
        y_curr -= row_h
    p2.append("Q")

    # SECTION 7: Strategic MBA Takeaways & Conclusion
    y3 = y_curr - 8
    p2.append("q")
    p2.append(f"0.0 0.106 0.58 rg 36 {y3} 523.28 1.5 re f")
    p2.append(f"BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 {y3 + 5} Td (7. Strategic MBA Takeaways & Conclusion) Tj ET")
    
    takeaways = [
        ("Risk-Calibrated Automation:", "Full automation introduces severe dispute liability; zero automation eliminates AI utility. The Rs. 8,000 threshold balances frictionless commerce with financial safety."),
        ("Zero-Trust Architecture:", "Airlines cannot grant open API access to external agents. Every transaction must be validated against real-time agent lifecycle state, explicit scopes, and transaction limits."),
        ("Non-Repudiation & Auditability:", "Permanent SQLite audit trails record AI intent vs. human customer authorization, ensuring full legal defensibility under Indian DPDP and consumer protection laws.")
    ]
    y3 -= 12
    for tk_title, tk_desc in takeaways:
        p2.append(f"BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 {y3} Td (\\(o\\) {tk_title}) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( {tk_desc}) Tj ET")
        y3 -= 10
    p2.append("Q")

    # Page 2 Footer
    p2.append("q")
    p2.append("0.8 0.82 0.85 RG 0.5 w 36 38 523.28 0 re S")
    p2.append("BT /F1 7.5 Tf 0.45 0.5 0.55 rg 36 28 Td (IndiGo Airlines \\(6E Guard\\) - MBA Assignment Documentation | Candidate Enrolment ID: PGD202564221) Tj ET")
    p2.append("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 520 28 Td (Page 2 of 2) Tj ET")
    p2.append("Q")

    # Assemble content streams
    s1 = "\n".join(p1).encode("latin1")
    s2 = "\n".join(p2).encode("latin1")
    objects[4] = f"<< /Length {len(s1)} >>\nstream\n".encode("latin1") + s1 + b"\nendstream"
    objects[5] = f"<< /Length {len(s2)} >>\nstream\n".encode("latin1") + s2 + b"\nendstream"

    # Encode all objects as binary
    body = bytearray()
    body.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []

    for i, obj in enumerate(objects, 1):
        offsets.append(len(body))
        body.extend(f"{i} 0 obj\n".encode("latin1"))
        if isinstance(obj, str):
            body.extend(obj.encode("latin1"))
        else:
            body.extend(obj)
        body.extend(b"\nendobj\n")

    # Cross-reference table
    xref_offset = len(body)
    body.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin1"))
    for off in offsets:
        body.extend(f"{off:010d} 00000 n \n".encode("latin1"))

    # Trailer
    body.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin1"))

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "REPORT.pdf")
    with open(out_path, "wb") as f:
        f.write(body)

    print(f"Successfully generated {out_path} ({len(body)} bytes, exactly 2 A4 pages).")

if __name__ == "__main__":
    build_pdf()
