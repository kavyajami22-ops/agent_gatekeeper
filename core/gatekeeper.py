"""
Gatekeeper Policy & Permission Decision Engine for IndiGo Airlines (6E Guard)

Evaluates inbound requests from external customer AI agents against
zero-trust security policies and outputs one of three deterministic verdicts:
1. ALLOW: Automated simulated execution.
2. ASK CUSTOMER: Routed to customer approval queue.
3. BLOCK: Denied immediately (revoked credentials, missing scopes, or policy violations).
"""
import uuid
from typing import Dict, Any, Optional
from core.config import (
    DECISION_ALLOW,
    DECISION_ASK_CUSTOMER,
    DECISION_BLOCK,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_BOOKING,
    ACTION_REQUEST_REFUND,
    STATUS_EXECUTED,
    STATUS_PENDING_CUSTOMER,
    STATUS_BLOCKED,
    AGENT_STATUS_ACTIVE,
    AGENT_STATUS_REVOKED,
    AGENT_STATUS_SUSPENDED,
    DEFAULT_PRE_APPROVED_BOOKING_LIMIT,
)
from core.database import (
    get_agent,
    save_request,
    get_current_timestamp,
)

class GatekeeperEngine:
    """Core evaluation engine that implements IndiGo's AI Agent Governance rules."""

    def __init__(self, booking_threshold: float = DEFAULT_PRE_APPROVED_BOOKING_LIMIT):
        self.booking_threshold = booking_threshold

    def evaluate_request(
        self,
        agent_id: str,
        action: str,
        customer_id: str,
        pnr: str,
        flight_details: str,
        amount: float = 0.0,
        booking_threshold_override: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluates an inbound AI agent request and determines the policy verdict.
        Educational simulation guarantee: Never performs real financial transactions or airline cancellations.
        """
        threshold = (
            booking_threshold_override 
            if booking_threshold_override is not None 
            else self.booking_threshold
        )
        request_id = f"REQ-6E-{uuid.uuid4().hex[:8].upper()}"
        agent = get_agent(agent_id)

        # -------------------------------------------------------------
        # STEP 1: Verify Agent Existence
        # -------------------------------------------------------------
        if not agent:
            decision = DECISION_BLOCK
            status = STATUS_BLOCKED
            reason = f"Security Violation: Agent ID '{agent_id}' is not registered in the IndiGo Agent Directory."
            save_request(
                request_id=request_id,
                agent_id=agent_id,
                customer_id=customer_id,
                pnr=pnr,
                action=action,
                flight_details=flight_details,
                amount=amount,
                gatekeeper_decision=decision,
                status=status,
                reason=reason
            )
            return self._format_result(
                request_id=request_id,
                agent_id=agent_id,
                agent_name="Unknown Agent",
                action=action,
                decision=decision,
                status=status,
                reason=reason,
                amount=amount,
                flight_details=flight_details
            )

        agent_name = agent["name"]
        agent_status = agent["status"]

        # -------------------------------------------------------------
        # STEP 2: Strict Revocation Enforcement (Rule #5)
        # Revoked agents must ALWAYS return BLOCK for any action.
        # -------------------------------------------------------------
        if agent_status == AGENT_STATUS_REVOKED:
            decision = DECISION_BLOCK
            status = STATUS_BLOCKED
            revoked_time = agent.get("revoked_at") or "Unknown"
            reason = (
                f"Security Lockdown: Agent '{agent_name}' ({agent_id}) access was REVOKED on {revoked_time}. "
                f"All incoming requests are strictly BLOCKED."
            )
            save_request(
                request_id=request_id,
                agent_id=agent_id,
                customer_id=customer_id,
                pnr=pnr,
                action=action,
                flight_details=flight_details,
                amount=amount,
                gatekeeper_decision=decision,
                status=status,
                reason=reason
            )
            return self._format_result(
                request_id=request_id,
                agent_id=agent_id,
                agent_name=agent_name,
                action=action,
                decision=decision,
                status=status,
                reason=reason,
                amount=amount,
                flight_details=flight_details
            )

        if agent_status == AGENT_STATUS_SUSPENDED:
            decision = DECISION_BLOCK
            status = STATUS_BLOCKED
            reason = f"Access Denied: Agent '{agent_name}' ({agent_id}) is currently SUSPENDED by IndiGo Governance."
            save_request(
                request_id=request_id,
                agent_id=agent_id,
                customer_id=customer_id,
                pnr=pnr,
                action=action,
                flight_details=flight_details,
                amount=amount,
                gatekeeper_decision=decision,
                status=status,
                reason=reason
            )
            return self._format_result(
                request_id=request_id,
                agent_id=agent_id,
                agent_name=agent_name,
                action=action,
                decision=decision,
                status=status,
                reason=reason,
                amount=amount,
                flight_details=flight_details
            )

        # -------------------------------------------------------------
        # STEP 3: Action Scope Permission Verification
        # -------------------------------------------------------------
        has_scope = False
        if action == ACTION_VIEW_FARES and agent.get("can_view_fares", 0):
            has_scope = True
        elif action == ACTION_BOOK_FLIGHT and agent.get("can_book", 0):
            has_scope = True
        elif action == ACTION_CHANGE_BOOKING and agent.get("can_change_booking", 0):
            has_scope = True
        elif action == ACTION_REQUEST_REFUND and agent.get("can_request_refund", 0):
            has_scope = True

        if not has_scope:
            decision = DECISION_BLOCK
            status = STATUS_BLOCKED
            reason = f"Permission Denied: Agent '{agent_name}' lacks the '{action}' permission scope in its registered profile."
            save_request(
                request_id=request_id,
                agent_id=agent_id,
                customer_id=customer_id,
                pnr=pnr,
                action=action,
                flight_details=flight_details,
                amount=amount,
                gatekeeper_decision=decision,
                status=status,
                reason=reason
            )
            return self._format_result(
                request_id=request_id,
                agent_id=agent_id,
                agent_name=agent_name,
                action=action,
                decision=decision,
                status=status,
                reason=reason,
                amount=amount,
                flight_details=flight_details
            )

        # -------------------------------------------------------------
        # STEP 4: Risk Evaluation for the 4 Supported Actions
        # -------------------------------------------------------------

        # Action 1: View Flight Fares
        if action == ACTION_VIEW_FARES:
            decision = DECISION_ALLOW
            status = STATUS_EXECUTED
            reason = "Read-Only Query: Low-risk information retrieval. Auto-approved by Gatekeeper policy."

        # Action 2: Book a Flight
        elif action == ACTION_BOOK_FLIGHT:
            # Respect agent custom limit if set lower than global threshold
            agent_custom_limit = agent.get("custom_spending_limit") or threshold
            effective_limit = min(threshold, agent_custom_limit)

            if amount <= effective_limit:
                decision = DECISION_ALLOW
                status = STATUS_EXECUTED
                reason = (
                    f"Booking value of ₹{amount:,.2f} is within the pre-approved limit "
                    f"of ₹{effective_limit:,.2f}. Auto-authorized without human friction."
                )
            else:
                decision = DECISION_ASK_CUSTOMER
                status = STATUS_PENDING_CUSTOMER
                reason = (
                    f"Booking value of ₹{amount:,.2f} EXCEEDS the pre-approved limit "
                    f"of ₹{effective_limit:,.2f}. Sent to Customer Confirmation Portal for explicit approval."
                )

        # Action 3: Change Flight Booking (Rule #4: Mandatory Customer Confirmation)
        elif action == ACTION_CHANGE_BOOKING:
            decision = DECISION_ASK_CUSTOMER
            status = STATUS_PENDING_CUSTOMER
            reason = (
                "Policy Requirement: Every flight schedule modification requires passenger consent "
                "to confirm flight timings and potential fare difference/change fees."
            )

        # Action 4: Request a Refund (Rule #4: Mandatory Customer Confirmation)
        elif action == ACTION_REQUEST_REFUND:
            decision = DECISION_ASK_CUSTOMER
            status = STATUS_PENDING_CUSTOMER
            reason = (
                "Policy Requirement: Every refund request releases airline seat inventory and triggers payout. "
                "Mandatory passenger confirmation required to prevent unauthorized ticket cancellation."
            )

        else:
            decision = DECISION_BLOCK
            status = STATUS_BLOCKED
            reason = f"Unsupported Action: '{action}' is not an authorized IndiGo Gatekeeper operation."

        # Persist request & initial audit log
        save_request(
            request_id=request_id,
            agent_id=agent_id,
            customer_id=customer_id,
            pnr=pnr,
            action=action,
            flight_details=flight_details,
            amount=amount,
            gatekeeper_decision=decision,
            status=status,
            reason=reason
        )

        return self._format_result(
            request_id=request_id,
            agent_id=agent_id,
            agent_name=agent_name,
            action=action,
            decision=decision,
            status=status,
            reason=reason,
            amount=amount,
            flight_details=flight_details
        )

    def _format_result(
        self,
        request_id: str,
        agent_id: str,
        agent_name: str,
        action: str,
        decision: str,
        status: str,
        reason: str,
        amount: float,
        flight_details: str
    ) -> Dict[str, Any]:
        """Formats the Gatekeeper verdict object."""
        return {
            "request_id": request_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "action": action,
            "decision": decision,
            "status": status,
            "reason": reason,
            "amount": amount,
            "flight_details": flight_details,
            "timestamp": get_current_timestamp()
        }
