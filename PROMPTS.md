# AI Interaction Log & Prompt Traceability Report

**Course:** MBA in Technology Management / Executive Business Analytics  
**Candidate Enrolment ID:** `PGD202564221`  
**Project Title:** IndiGo Airlines — Agent Gatekeeper (6E Guard)  
**Document Purpose:** Academic Integrity, Generative AI Traceability, and Human-in-the-Loop Audit Trail  

---

## 1. Overview & Methodology

This document logs the actual interaction, iterative prompt sequence, and human oversight applied during the design, development, testing, and documentation of the **IndiGo Agent Gatekeeper** assignment. 

The AI coding assistant was utilized as a technical co-pilot to translate business governance requirements into clean software architecture, database schemas, and documentation. All high-level business rules, domain constraints, academic identifiers, threshold boundaries, and testing validations were driven, reviewed, and verified by the student.

---

## 2. Chronological Log of Actual Prompts Used

### Stage 1: Initial System Architecture & Implementation Planning
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

### Stage 3: Implementation Execution & Environment Boundary
* **User Approval & Proceed Prompt:**
```text
proceed again
```
* **User Environment Constraint (Intervention during package installation):**
```text
i have only python with me installed
```

---

### Stage 4: Written Academic Documentation (REPORT.md & RULES.md)
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

### Stage 6: Prompt Traceability Creation (PROMPTS.md)
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

### Stage 7: Git Repository Inspection
```text
Check whether Git is initialized in my existing agent_gatekeeper project folder.

Do not make any changes yet. Tell me:
1. Whether Git is installed.
2. Whether this folder is already a Git repository.
3. Whether a GitHub remote repository is connected.
4. How many commits currently exist.

Do not create commits or push anything yet.
```

---

### Stage 8: Demonstration Walkthrough Enhancement (README.md)
```text
Review the existing README.md and improve it by adding a clear section titled "How to Run the Project and Demonstrate the Six Test Cases".

Include simple Windows instructions for launching the application using run.bat, explain the four main tabs, and list the six required test scenarios with their expected ALLOW, ASK CUSTOMER, or BLOCK outcomes.

Do not change application logic or existing test results. Save only the updated README.md.
```

---

### Stage 9: Master Governance Decision Table Enhancement (RULES.md)
```text
Review the existing RULES.md file. Improve its presentation by adding a clear decision table covering these six test scenarios:

1. Registered active agent viewing flight fares — ALLOW.
2. Unknown or unregistered agent — BLOCK.
3. Booking amount above ₹8,000 — ASK CUSTOMER.
4. Booking amount at or below ₹8,000, with valid permission — ALLOW.
5. Revoked agent making any request — BLOCK.
6. Any flight change or refund request — ASK CUSTOMER.

Also explain that revocation overrides all other permissions and that customer approval is required before a pending action is treated as approved.

Keep the rules consistent with the actual application logic. Do not modify application code. Save only RULES.md.
```

---

## 3. Manual Review and Changes

A core principle of academic integrity in co-piloted software development is **active human verification** and **deliberate manual correction** rather than blind acceptance of AI outputs.

### 1. Genuine Manual Test: Verification of the ₹9,500 Threshold Boundary
* **The Manual Check:** In **Tab 1: Live Agent Simulator**, I personally configured a simulated booking using an active commercial agent (*Personal Gemini Travel Agent - AGT-GEM-003*) for **Mumbai (BOM) $\rightarrow$ Goa (GOI) on Flight 6E-802** with a transaction value of **₹9,500**, which specifically exceeds the pre-approved ₹8,000 limit.
* **The Review & Verification:**
  * I personally verified that the Gatekeeper did **not** automatically execute the transaction.
  * The system correctly produced the amber **`VERDICT: ASK CUSTOMER`** decision card, explicitly citing the threshold violation.
  * I navigated to **Tab 2: Customer Confirmation Inbox**, confirmed the request was held in `PENDING_CUSTOMER` status, manually clicked **`Approve Action`**, and confirmed the simulated state updated to `APPROVED` in the SQLite audit log.

### 2. Manual Corrections and Architectural Changes Enforced by the Student
Throughout the project lifecycle, I reviewed the AI assistant's proposals and actively intervened to correct and change direction:
* **Threshold & Policy Correction (Stage 2):** When the AI assistant initially proposed an arbitrary ₹5,000 threshold and flexible cancellation rules, I intervened before any code was written and mandated:
  1. Setting the pre-approved baseline to **₹8,000**.
  2. Mandating that **every** flight change and refund request strictly require human confirmation.
  3. Requiring prominent, configurable display of my candidate enrolment number **`PGD202564221`**.
  4. Enforcing an educational simulation boundary to ensure no real transactions could ever be triggered.
* **Environment Architecture Correction (Stage 3):** When the AI assistant attempted to execute package installations outside the standard environment, I intervened and specified: *"i have only python with me installed"*. This manual correction altered the technical direction, resulting in a zero-dependency architecture with `server.py` and `run.bat` that runs on base Python standard library without external dependencies.
* **Format & Scope Constraints (Stages 4 & 5):** I manually imposed strict length boundaries (maximum 2 pages for the project report and 1 page for the rules sheet), and prohibited the installation of third-party PDF compilation libraries to maintain environment integrity.

---

## 4. Academic Integrity Statement

I confirm that:
1. The prompts recorded in this document represent the actual, unaltered prompt history exchanged with the AI assistant during this project.
2. All business governance rules, risk thresholds, airline actions, and policy criteria were determined, reviewed, and verified by me.
3. The functional application was manually inspected, tested, and validated by me prior to submission.

**Student Name / Enrolment ID:** `PGD202564221`  
**Date:** November 19, 2026
