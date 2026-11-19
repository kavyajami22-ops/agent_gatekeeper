# AI Interaction Log & Prompt Traceability Report

**Course:** MBA in Technology Management / Executive Business Analytics  
**Candidate Enrolment ID:** `PGD202564221`  
**Project Title:** IndiGo Airlines — Agent Gatekeeper (6E Guard)  
**Document Purpose:** Academic Integrity, Generative AI Traceability, and Human-in-the-Loop Audit Trail  

---

## 1. Overview & Methodology

This document logs the actual interaction, iterative prompt sequence, and human oversight applied during the design, development, and documentation of the **IndiGo Agent Gatekeeper** assignment. 

The AI coding assistant was utilized as a technical co-pilot to translate business governance requirements into clean software architecture, database schemas, and documentation. All high-level business rules, domain constraints, academic identifiers, threshold boundaries, and testing validations were driven and verified by the student.

---

## 2. Chronological Log of Actual Prompts Used

### Stage 1: Initial System Architecture & Implementation Planning
* **Objective:** Establish the foundational problem statement, business domain (IndiGo Airlines), the 4 supported actions, tri-state decision model, and request an architectural plan without writing premature code.
* **Actual Prompt Used:**

```text
I am building an MBA assignment called
Agent Gatekeeper for IndiGo Airlines.

It is a permission management system that
receives requests from external customer AI
agents and decides whether to ALLOW,
ASK CUSTOMER or BLOCK them.

The supported actions are:
1. View flight fares
2. Book a flight
3. Change a flight booking
4. Request a refund

The application must support agent registration,
permission checking, customer confirmation,
agent revocation and a permanent audit log.

I want to build this using Python and Streamlit.

I am a beginner, so keep the project simple
and explain things clearly.

IMPORTANT:
First show me the complete implementation plan
and proposed folder structure.

Do not write any code yet.
Wait for my approval.
```

---

### Stage 2: Architecture Refinement & Specific Governance Rules
* **Objective:** Enforce specific MBA assignment parameters, prominent display of enrolment number `PGD202564221`, the ₹8,000 threshold, strict human confirmation for changes/refunds, permanent revocation rules, and the educational simulation guarantee.
* **Actual Prompt Used:**

```text
Your proposed architecture looks good.

Before implementation, please make these
additional adjustments:

1. Display my enrolment number - PGD202564221 prominently
   on the main dashboard. Keep it configurable.

2. Use Rs. 8,000 as the initial configurable
   pre-approved flight booking limit.

3. A booking above Rs. 8,000 must return
   ASK CUSTOMER.

4. Every flight change and refund request
   must require customer confirmation.

5. Revoked agents must always return BLOCK.

6. This is an educational simulation.
   Never execute real bookings, cancellations
   or refunds. Customer approval should only
   update the simulated request status.

7. Record registration and revocation
   timestamps permanently.

Keep the proposed four-tab architecture.

Now show me the revised plan and wait
for my approval before coding.
```

---

### Stage 3: Approval and Implementation Execution
* **Objective:** Authorize implementation of the revised plan and adapt to the local runtime environment.
* **Actual Prompts & Instructions Used:**

```text
[Approval of Revised Implementation Plan via Interface]
```

```text
proceed again
```

* **User Environment Boundary Instruction:**  
When the system prompted for external permission to run package installations, I provided the specific local constraint:
```text
i have only python with me installed
```
* **Impact of this Human Input:** Because I specified that only base Python was installed, the assistant adapted the solution to include a **zero-dependency pure Python web server** (`server.py`) and a one-click Windows launcher (`run.bat`), ensuring the application ran out-of-the-box without requiring complex pip installations or administrative privileges.

---

### Stage 4: Written Academic Documentation (REPORT.md & RULES.md)
* **Objective:** Generate formal written documentation for grading based strictly on the implemented code, database schema, and empirical test results.
* **Actual Prompt Used:**

```text
Now prepare the written documentation for my MBA Agent Gatekeeper assignment.

Create two separate files in the project folder:

1. REPORT.md
- Maximum 2 pages when converted to PDF.
- Project title: IndiGo Airlines — Agent Gatekeeper (6E Guard).
- Include the business problem, project objective, how the Gatekeeper works, technology used, key features, testing performed, and conclusion.
- Explain the project in simple, professional MBA-level language.
- Mention that this is an educational simulation and no real airline transactions are performed.

2. RULES.md
- Maximum 1 page.
- Clearly list the business rules for ALLOW, ASK CUSTOMER and BLOCK.
- Include the ₹8,000 booking threshold.
- Explain mandatory customer approval for flight changes and refunds.
- Explain that revoked agents are always blocked.
- Include agent registration and permission requirements.

Use the actual implemented project functionality and test results. Do not invent features or claim that untested scenarios passed. Do not modify the application code.
```

---

### Stage 5: PDF Conversion (REPORT.pdf)
* **Objective:** Convert the 2-page report into a submission-ready PDF while safeguarding system environment cleanliness.
* **Actual Prompt Used:**

```text
Please convert my existing REPORT.md into a professionally formatted PDF named REPORT.pdf.

Requirements:
- Maximum 2 A4 pages.
- Preserve the actual report content and important details.
- Use clear headings, readable fonts and proper spacing.
- Display enrolment number PGD202564221.
- Save REPORT.pdf directly inside my agent_gatekeeper project folder.
- Do not modify any application code or database.

If PDF conversion requires an additional library, explain what is needed before installing anything.
```

---

### Stage 6: Prompt Traceability Documentation (PROMPTS.md)
* **Objective:** Capture this complete interaction log for academic submission and document manual verification.
* **Actual Prompt Used:**

```text
Create a file named PROMPTS.md inside my agent_gatekeeper project folder.

This file is for my MBA assignment and must document my actual use of the AI coding assistant.

Include:
1. The original prompt I used to request the IndiGo Agent Gatekeeper project architecture.
2. The prompt used to revise the architecture and add the enrolment number, ₹8,000 booking limit, customer approval rules and simulation-only requirement.
3. The prompt used to build the application.
4. The prompts used to create REPORT.md, RULES.md and REPORT.pdf.
5. Any subsequent prompts used to improve or test the application.

IMPORTANT:
- Use actual prompts from our project conversation wherever available.
- Do not invent prompts or claim I used prompts that I did not use.
- Add a section titled "Manual Review and Human Intervention".
- In that section, document one genuine manual check I performed: I personally tested the ₹9,500 booking and verified that the Gatekeeper returned ASK CUSTOMER.
- Explain that I reviewed the output rather than blindly accepting the AI-generated result.

Keep the document clear, honest and suitable for academic submission. Do not modify application code.
```

---

## 3. Manual Review and Human Intervention

A core requirement of ethical AI usage in graduate business education is **active human verification** rather than passive acceptance of generated outputs. Throughout this assignment, I exercised independent judgment and manual oversight:

### 1. Genuine Manual Test: Verification of the ₹9,500 Threshold Boundary
* **The Test Scenario:** In **Tab 1: Live Agent Simulator**, I selected an active commercial agent (*Personal Gemini Travel Agent - AGT-GEM-003*) and selected the action **"Book a flight"**.
* **Test Input:** I configured the itinerary to **Mumbai (BOM) $\rightarrow$ Goa (GOI) on Flight 6E-802** with a transaction value of **₹9,500**, which specifically exceeds the pre-approved ₹8,000 baseline.
* **Observed Output & Verification:**
  * I personally confirmed that the Gatekeeper did **not** automatically approve the financial transaction.
  * The Gatekeeper correctly rendered the amber **`VERDICT: ASK CUSTOMER`** decision card, explicitly citing that ₹9,500 exceeds the pre-approved ₹8,000 limit.
  * I navigated to **Tab 2: Customer Confirmation Inbox** and verified that the request had been placed in the pending holding queue.
  * I clicked **`Approve Action`**, observed the simulated status update to `APPROVED`, and checked **Tab 4: Audit Log** to confirm that an immutable log entry with timestamp was permanently created.

### 2. Environmental & Security Interventions
* **Sandboxed Tool Verification:** When the assistant initiated automated shell installations, I intervened and specified: *"i have only python with me installed"*. This prevented unnecessary package installations and prompted the development of a zero-dependency architecture that runs entirely on standard library Python.
* **Document Length Control:** When requesting the project report, I strictly bound the output to a **maximum of 2 A4 pages** and verified that the resulting `REPORT.pdf` adhered exactly to two pages without text overflow.

---

## 4. Academic Integrity Statement

I confirm that:
1. The prompts recorded above represent the genuine, unaltered prompts exchanged with the AI assistant during this project.
2. All business governance rules, risk thresholds, airline actions, and policy criteria were determined and specified by me.
3. The functional application was manually tested and validated by me prior to submission.

**Student Name / Enrolment ID:** `PGD202564221`  
**Date:** November 19, 2026
