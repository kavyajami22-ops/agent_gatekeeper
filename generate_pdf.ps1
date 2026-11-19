# PowerShell Zero-Dependency PDF Generator for REPORT.pdf
$outPath = Join-Path $PSScriptRoot "REPORT.pdf"

$objects = [System.Collections.ArrayList]::new()

function Add-Obj($content) {
    [void]$objects.Add($content)
    return $objects.Count
}

# 1. Catalog
Add-Obj "<< /Type /Catalog /Pages 2 0 R >>"
# 2. Pages
Add-Obj "<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>"
# 3. Page 1
Add-Obj "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 5 0 R /Resources 7 0 R >>"
# 4. Page 2
Add-Obj "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 6 0 R /Resources 7 0 R >>"
# 5. Content Stream Page 1 Placeholder
Add-Obj ""
# 6. Content Stream Page 2 Placeholder
Add-Obj ""
# 7. Resources
Add-Obj "<< /Font << /F1 8 0 R /F2 9 0 R /F3 10 0 R >> /ProcSet [/PDF /Text /ImageC] >>"
# 8. Font F1
Add-Obj "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
# 9. Font F2
Add-Obj "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
# 10. Font F3
Add-Obj "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"

# PAGE 1 STREAM
$p1 = [System.Collections.ArrayList]::new()
[void]$p1.Add("q")
[void]$p1.Add("0.0 0.106 0.58 rg 36 740 523.28 72 re f")
[void]$p1.Add("1.0 0.82 0.4 rg 48 748 215 17 re f")
[void]$p1.Add("BT /F2 8.5 Tf 0.0 0.106 0.58 rg 56 753.5 Td (Candidate Enrolment ID: PGD202564221) Tj ET")
[void]$p1.Add("0.15 0.3 0.7 rg 270 748 185 17 re f")
[void]$p1.Add("BT /F1 8 Tf 1 1 1 rg 278 753.5 Td (Simulation Mode: Educational Sandbox) Tj ET")
[void]$p1.Add("BT /F2 15 Tf 1 1 1 rg 48 788 Td (IndiGo Airlines - Agent Gatekeeper \(6E Guard\)) Tj ET")
[void]$p1.Add("BT /F1 8.5 Tf 0.9 0.95 1 rg 48 774 Td (MBA Project Report | Emerging Tech & Autonomous AI Agent Governance System) Tj ET")
[void]$p1.Add("Q")

# SECTION 1
[void]$p1.Add("q")
[void]$p1.Add("0.0 0.106 0.58 rg 36 718 523.28 1.5 re f")
[void]$p1.Add("BT /F2 11 Tf 0.0 0.106 0.58 rg 36 724 Td (1. Executive Summary & Business Problem) Tj ET")

$y = 704
[void]$p1.Add("BT /F1 8 Tf 0.15 0.18 0.22 rg 36 $y Td (As consumer travel booking transitions from manual web searches to autonomous AI agents \(e.g., MakeMyTrip bots, Expedia concierges,) Tj ET")
$y -= 11
[void]$p1.Add("BT /F1 8 Tf 0.15 0.18 0.22 rg 36 $y Td (and Google Gemini personal assistants\), commercial airlines face an unprecedented governance challenge. Autonomous agents can search,) Tj ET")
$y -= 11
[void]$p1.Add("BT /F1 8 Tf 0.15 0.18 0.22 rg 36 $y Td (book, modify, and cancel flights on behalf of passengers. While frictionless, this introduces critical operational and commercial risks:) Tj ET")

$y -= 14
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Financial Risk & Hallucination Exposure:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Agents may misinterpret intent or hallucinate booking criteria, causing unexpected charges.) Tj ET")
$y -= 11
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Operational & Itinerary Disruption:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Arbitrary schedule changes disrupt itineraries, risk missed connections, and incur airline fees.) Tj ET")
$y -= 11
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Irreversible Inventory Depletion:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Cancellations and refunds release airline seat inventory and trigger payouts, demanding strict oversight.) Tj ET")

# Notice Box
$y -= 4
$box_h = 32
$box_y = $y - $box_h + 8
[void]$p1.Add("0.95 0.96 0.98 rg 36 $box_y 523.28 $box_h re f")
[void]$p1.Add("0.8 0.84 0.88 RG 0.75 w 36 $box_y 523.28 $box_h re S")
$ny1 = $y - 4
$ny2 = $y - 15
[void]$p1.Add("BT /F2 7.5 Tf 0.6 0.2 0.0 rg 44 $ny1 Td (EDUCATIONAL SIMULATION NOTICE:) Tj /F1 7.5 Tf 0.25 0.25 0.25 rg ( This project is an educational simulation developed strictly for academic evaluation.) Tj ET")
[void]$p1.Add("BT /F1 7.5 Tf 0.25 0.25 0.25 rg 44 $ny2 Td (It operates in a local sandboxed environment. No real airline reservation systems \(PSS/GDS\), live inventory, or banking gateways are touched.) Tj ET")
[void]$p1.Add("Q")

# SECTION 2
$y -= 46
[void]$p1.Add("q")
[void]$p1.Add("0.0 0.106 0.58 rg 36 $y 523.28 1.5 re f")
$sy = $y + 6
[void]$p1.Add("BT /F2 11 Tf 0.0 0.106 0.58 rg 36 $sy Td (2. Project Objectives) Tj ET")

$y -= 13
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Tri-State Deterministic Governance:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Classify all inbound AI agent requests into ALLOW, ASK CUSTOMER, or BLOCK.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Pre-Approved Spending Controls:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Automate low-risk transactions while holding bookings above an initial limit of Rs. 8,000.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Mandatory Human-in-the-Loop:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Enforce explicit passenger confirmation on all flight changes and refund requests.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Agent Governance & Kill-Switch:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Provide one-click administrative revocation of compromised agents with permanent timestamps.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (\(o\) Regulatory Auditability:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Maintain an immutable, permanent SQLite audit log guaranteeing non-repudiation and compliance.) Tj ET")
[void]$p1.Add("Q")

# SECTION 3
$y -= 4
[void]$p1.Add("q")
[void]$p1.Add("0.0 0.106 0.58 rg 36 $y 523.28 1.5 re f")
$sy3 = $y + 6
[void]$p1.Add("BT /F2 11 Tf 0.0 0.106 0.58 rg 36 $sy3 Td (3. How the Gatekeeper Works \(Four-Stage Policy Evaluation Flow\)) Tj ET")

$y -= 13
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (Step 1 - Identity & Status Verification:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Gatekeeper checks agent directory. If status is REVOKED or SUSPENDED, request is instantly BLOCKED.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (Step 2 - Permission Scope Verification:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Verifies agent has active scope for the action \(View Fares, Book, Change, Refund\). If missing, request is BLOCKED.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (Step 3 - Risk Matrix & Threshold Evaluation:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Fares: ALLOW \(read-only\). Bookings <= Rs. 8,000: ALLOW. Bookings > Rs. 8,000: ASK CUSTOMER. Changes & Refunds: strictly ASK CUSTOMER.) Tj ET")
$y -= 11.5
[void]$p1.Add("BT /F2 8 Tf 0.0 0.106 0.58 rg 46 $y Td (Step 4 - Customer Confirmation & Audit:) Tj /F1 8 Tf 0.2 0.2 0.2 rg ( Pending requests enter passenger inbox. Approval/Rejection updates simulated state and appends immutable audit log.) Tj ET")
[void]$p1.Add("Q")

# Page 1 Footer
[void]$p1.Add("q")
[void]$p1.Add("0.8 0.82 0.85 RG 0.5 w 36 38 523.28 0 re S")
[void]$p1.Add("BT /F1 7.5 Tf 0.45 0.5 0.55 rg 36 28 Td (IndiGo Airlines \(6E Guard\) - MBA Assignment Documentation | Candidate Enrolment ID: PGD202564221) Tj ET")
[void]$p1.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 520 28 Td (Page 1 of 2) Tj ET")
[void]$p1.Add("Q")

# PAGE 2 STREAM
$p2 = [System.Collections.ArrayList]::new()
[void]$p2.Add("q")
[void]$p2.Add("BT /F2 8.5 Tf 0.0 0.106 0.58 rg 36 808 Td (IndiGo Airlines - Agent Gatekeeper \(6E Guard\) | Technical & Empirical Report) Tj ET")
[void]$p2.Add("BT /F2 8.5 Tf 0.6 0.3 0.0 rg 420 808 Td (Candidate Enrolment ID: PGD202564221) Tj ET")
[void]$p2.Add("0.8 0.82 0.85 RG 0.5 w 36 802 523.28 0 re S")
[void]$p2.Add("Q")

# SECTION 4
$y2 = 786
[void]$p2.Add("q")
[void]$p2.Add("0.0 0.106 0.58 rg 36 $y2 523.28 1.5 re f")
$sy4 = $y2 + 5
[void]$p2.Add("BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 $sy4 Td (4. Technology Stack & Architecture) Tj ET")

$y2 -= 12
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Programming Language:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Python 3.11 with clean modular separation \(core/config.py, core/database.py, core/gatekeeper.py\).) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Persistent Database:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( SQLite \(sqlite3 built-in\), ACID relational persistence, permanent registered_at & revoked_at timestamps.) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Zero-Dependency Server:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Built-in Python http.server \(server.py\) serving responsive HTML5/CSS/JS dashboard at http://localhost:8501.) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Streamlit Interface:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Streamlit dashboard \(app.py\) with Plotly analytics for environments with optional packages installed.) Tj ET")
[void]$p2.Add("Q")

# SECTION 5
$y2 -= 4
[void]$p2.Add("q")
[void]$p2.Add("0.0 0.106 0.58 rg 36 $y2 523.28 1.5 re f")
$sy5 = $y2 + 5
[void]$p2.Add("BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 $sy5 Td (5. Key Functional Modules \(The 4 Dashboard Tabs\)) Tj ET")

$y2 -= 12
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Tab 1 - Live Agent Simulator:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Dispatch simulated requests across all 4 actions; observe real-time ALLOW, ASK, or BLOCK verdict cards.) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Tab 2 - Confirmation Inbox:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Human-in-the-loop passenger inbox where held actions are reviewed and confirmed with Approve/Reject buttons.) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Tab 3 - Governance & Kill-Switch:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Onboard new customer AI agents, configure action scopes, and invoke the one-click emergency revocation switch.) Tj ET")
$y2 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y2 Td (\(o\) Tab 4 - Audit Log & Analytics:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Searchable immutable transaction ledger with decision distribution chart and one-click CSV compliance export.) Tj ET")
[void]$p2.Add("Q")

# SECTION 6: Table
$y2 -= 4
[void]$p2.Add("q")
[void]$p2.Add("0.0 0.106 0.58 rg 36 $y2 523.28 1.5 re f")
$sy6 = $y2 + 5
[void]$p2.Add("BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 $sy6 Td (6. Empirical Testing & Validation Results \(Automated Test Suite: test_gatekeeper.py\)) Tj ET")

$y_table = $y2 - 18
$row_h = 16.5
[void]$p2.Add("0.0 0.106 0.58 rg 36 $y_table 523.28 $row_h re f")
$ty = $y_table + 5
[void]$p2.Add("BT /F2 7.5 Tf 1 1 1 rg 42 $ty Td (Scenario Name) Tj 205 $ty Td (Expected Decision) Tj 355 $ty Td (Actual Decision) Tj 480 $ty Td (Final Status) Tj ET")

$tests = @(
    @("1. Registered Agent with Read-Only Permission", "ALLOW (Fare) / BLOCK (Booking)", "ALLOW (Fare) / BLOCK (Booking)", "PASS"),
    @("2. Unknown or Unregistered Agent", "BLOCK", "BLOCK", "PASS"),
    @("3. Booking Amount Above Rs. 8,000 Threshold", "ASK CUSTOMER", "ASK CUSTOMER", "PASS"),
    @("4. Booking Amount At or Below Rs. 8,000", "ALLOW", "ALLOW", "PASS"),
    @("5. Revoked Agent Attempting Any Request", "BLOCK", "BLOCK", "PASS"),
    @("6. Custom: Mandatory Refund & Customer Sign-Off", "ASK CUSTOMER -> PENDING -> APPROVED", "ASK CUSTOMER -> PENDING -> APPROVED", "PASS")
)

$y_curr = $y_table - $row_h
$idx = 0
foreach ($t in $tests) {
    $bg = if ($idx % 2 -eq 0) { "0.96 0.97 0.99" } else { "1.0 1.0 1.0" }
    [void]$p2.Add("$bg rg 36 $y_curr 523.28 $row_h re f")
    [void]$p2.Add("0.88 0.9 0.92 RG 0.4 w 36 $y_curr 523.28 $row_h re S")
    $rty = $y_curr + 5
    $t0 = $t[0]; $t1 = $t[1]; $t2 = $t[2]; $t3 = $t[3]
    [void]$p2.Add("BT /F2 6.5 Tf 0.1 0.15 0.2 rg 42 $rty Td ($t0) Tj ET")
    [void]$p2.Add("BT /F1 6.5 Tf 0.2 0.2 0.2 rg 205 $rty Td ($t1) Tj ET")
    [void]$p2.Add("BT /F1 6.5 Tf 0.0 0.106 0.58 rg 355 $rty Td ($t2) Tj ET")
    [void]$p2.Add("BT /F2 7 Tf 0.06 0.6 0.3 rg 485 $rty Td ($t3) Tj ET")
    $y_curr -= $row_h
    $idx++
}
[void]$p2.Add("Q")

# SECTION 7
$y3 = $y_curr - 12
[void]$p2.Add("q")
[void]$p2.Add("0.0 0.106 0.58 rg 36 $y3 523.28 1.5 re f")
$sy7 = $y3 + 5
[void]$p2.Add("BT /F2 10.5 Tf 0.0 0.106 0.58 rg 36 $sy7 Td (7. Strategic MBA Takeaways & Conclusion) Tj ET")

$y3 -= 12
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y3 Td (\(o\) Risk-Calibrated Automation:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Full automation introduces dispute liability; zero automation eliminates AI utility. Rs. 8,000 balances both.) Tj ET")
$y3 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y3 Td (\(o\) Zero-Trust Architecture:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Airlines cannot grant open API access to external agents. Every transaction must be validated against real-time status.) Tj ET")
$y3 -= 10
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 46 $y3 Td (\(o\) Non-Repudiation & Auditability:) Tj /F1 7.5 Tf 0.2 0.2 0.2 rg ( Permanent SQLite audit trails record AI intent vs. human authorization, ensuring legal defensibility under DPDP.) Tj ET")
[void]$p2.Add("Q")

# Page 2 Footer
[void]$p2.Add("q")
[void]$p2.Add("0.8 0.82 0.85 RG 0.5 w 36 38 523.28 0 re S")
[void]$p2.Add("BT /F1 7.5 Tf 0.45 0.5 0.55 rg 36 28 Td (IndiGo Airlines \(6E Guard\) - MBA Assignment Documentation | Candidate Enrolment ID: PGD202564221) Tj ET")
[void]$p2.Add("BT /F2 7.5 Tf 0.0 0.106 0.58 rg 520 28 Td (Page 2 of 2) Tj ET")
[void]$p2.Add("Q")

# Content streams assembly
$enc = [System.Text.Encoding]::GetEncoding("ISO-8859-1")
$s1_text = ($p1 -join "`n")
$s1_bytes = $enc.GetBytes($s1_text)
$objects[4] = "<< /Length $($s1_bytes.Length) >>`nstream`n$s1_text`nendstream"

$s2_text = ($p2 -join "`n")
$s2_bytes = $enc.GetBytes($s2_text)
$objects[5] = "<< /Length $($s2_bytes.Length) >>`nstream`n$s2_text`nendstream"

# Build raw binary PDF
$ms = [System.IO.MemoryStream]::new()
$headerBytes = $enc.GetBytes("%PDF-1.4`n%`xE2`xE3`xCF`xD3`n")
$ms.Write($headerBytes, 0, $headerBytes.Length)

$offsets = [System.Collections.ArrayList]::new()
for ($i = 0; $i -lt $objects.Count; $i++) {
    [void]$offsets.Add($ms.Position)
    $objHeader = $enc.GetBytes("$($i + 1) 0 obj`n")
    $ms.Write($objHeader, 0, $objHeader.Length)
    
    $objBody = $enc.GetBytes($objects[$i])
    $ms.Write($objBody, 0, $objBody.Length)
    
    $objEnd = $enc.GetBytes("`nendobj`n")
    $ms.Write($objEnd, 0, $objEnd.Length)
}

$xrefPos = $ms.Position
$xrefHeader = $enc.GetBytes("xref`n0 $($objects.Count + 1)`n0000000000 65535 f `n")
$ms.Write($xrefHeader, 0, $xrefHeader.Length)

foreach ($off in $offsets) {
    $line = "{0:D10} 00000 n `n" -f $off
    $lineBytes = $enc.GetBytes($line)
    $ms.Write($lineBytes, 0, $lineBytes.Length)
}

$trailer = $enc.GetBytes("trailer`n<< /Size $($objects.Count + 1) /Root 1 0 R >>`nstartxref`n$xrefPos`n%%EOF`n")
$ms.Write($trailer, 0, $trailer.Length)

[System.IO.File]::WriteAllBytes($outPath, $ms.ToArray())
Write-Output "Successfully updated $outPath ($($ms.Length) bytes, exactly 2 A4 pages)."
