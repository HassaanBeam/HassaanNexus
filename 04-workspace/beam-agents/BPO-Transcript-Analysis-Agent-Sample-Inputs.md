# BPO Transcript Analysis Agent - Sample Input Data

**Agent ID:** `a1b9bee3-1e15-4c11-a6d5-739d8a4f01ea`
**Workspace ID:** `400f6086-88e0-43b8-9020-aaa1c0bb2ad0`
**Generated:** 2026-01-07

---

## Agent Overview

The BPO Transcript Analysis Agent processes customer service call transcripts to:
1. Extract key information (customer details, order number)
2. Look up order details in Airtable database
3. Analyze for negative sentiment and compliance issues
4. Flag problematic conversations and alert internal teams

### Workflow Diagram

```
Entry Node
    │
    ▼
Extract Key Info from Transcript
    │
    ▼
Retrieve Airtable Records (by Order Number)
    │
    ├── [No Orders Found] ──────► Exit Node
    │
    ▼
Analyze Transcript for Flags
    │
    ├── [Not Flagged] ──────► Exit Node
    │
    ▼
[Flagged] ──► Send Email to Customer
                    │
                    ▼
              Post Slack Notification
```

---

## Required Input Format

The agent expects a task query containing a call transcript. The transcript should include:
- Customer name and contact information
- Order number (required for Airtable lookup)
- Conversation between agent and customer

---

## Scenario 1 – Happy Path (Order Found, Not Flagged)

**Description:** Standard customer inquiry about order status. Positive interaction with no issues detected.

### How to Use
1. Navigate to the agent in Beam.ai
2. Click "Create Task"
3. Paste the transcript below in the task query field
4. Submit the task

### Sample Input (Task Query)

```
Analyze the following customer service call transcript for our BPO quality assurance process:

---
CALL TRANSCRIPT
Date: January 5, 2026
Duration: 4 minutes 23 seconds
Agent: Sarah Mitchell
Customer: John Anderson
Order Number: ORD-2026-00142

[00:00:00] Agent: Thank you for calling TechGear Support. My name is Sarah, how may I assist you today?

[00:00:08] Customer: Hi Sarah. I'm calling about my order ORD-2026-00142. I placed it three days ago and wanted to check on the shipping status.

[00:00:18] Agent: I'd be happy to help you with that, John. Let me pull up your order now. I can see your order for the wireless headphones was processed and shipped yesterday via express delivery.

[00:00:35] Customer: Oh that's great news! Do you have a tracking number?

[00:00:40] Agent: Yes, absolutely. Your tracking number is 1Z999AA10123456784. You should receive delivery by Thursday.

[00:00:52] Customer: Perfect, thank you so much for your help!

[00:00:56] Agent: You're welcome! Is there anything else I can help you with today?

[00:01:02] Customer: No, that's all I needed. Have a great day!

[00:01:06] Agent: Thank you for choosing TechGear. Have a wonderful day, John!
---

Customer Email: john.anderson@email.com
```

### Expected Behavior

| Step | Expected Outcome |
|------|------------------|
| 1. Extract Key Info | `order_number: ORD-2026-00142`, `customer_name: John Anderson`, `customer_email: john.anderson@email.com` |
| 2. Airtable Lookup | Order found with matching details |
| 3. Flag Analysis | `flag_status: not_flagged`, `flag_reason: null` |
| 4. Routing | Takes "Not Flagged" path → Exit Node |
| 5. Final Status | COMPLETED - No email or Slack notification sent |

### Expected Output

```json
{
  "flag_status": "not_flagged",
  "flag_reason": null,
  "extracted_data": {
    "order_number": "ORD-2026-00142",
    "customer_name": "John Anderson",
    "customer_email": "john.anderson@email.com",
    "call_sentiment": "positive"
  }
}
```

---

## Scenario 2 – Flagged (Negative Sentiment - Angry Customer)

**Description:** Customer expresses frustration and dissatisfaction. Transcript flagged for negative sentiment requiring review.

### How to Use
1. Navigate to the agent in Beam.ai
2. Click "Create Task"
3. Paste the transcript below in the task query field
4. Submit the task

### Sample Input (Task Query)

```
Analyze the following customer service call transcript for our BPO quality assurance process:

---
CALL TRANSCRIPT
Date: January 6, 2026
Duration: 8 minutes 47 seconds
Agent: Michael Torres
Customer: Rebecca Williams
Order Number: ORD-2026-00089

[00:00:00] Agent: Thank you for calling TechGear Support. My name is Michael, how may I assist you today?

[00:00:07] Customer: Finally! I've been on hold for 45 minutes! This is absolutely ridiculous!

[00:00:14] Agent: I sincerely apologize for the long wait time, ma'am. How can I help you today?

[00:00:20] Customer: My order number is ORD-2026-00089. I ordered a laptop two weeks ago and it still hasn't arrived. This is completely unacceptable!

[00:00:32] Agent: I understand your frustration. Let me look into this for you right away.

[00:00:40] Customer: You people are the worst! I paid extra for expedited shipping and nothing! I want a full refund AND I'm going to leave bad reviews everywhere!

[00:00:55] Agent: I completely understand, Mrs. Williams. I can see your order was delayed due to a warehouse issue. I want to make this right for you.

[00:01:08] Customer: Make it right? It's too late for that! I needed this laptop for my daughter's school. Now she's missed a week of online classes because of your incompetence!

[00:01:22] Agent: I am truly sorry for the impact this has had. Let me arrange expedited overnight shipping at no additional cost and provide you with a 20% discount on your next order.

[00:01:38] Customer: I don't want a discount, I want my laptop! And I want to speak to a manager right now!

[00:01:46] Agent: Absolutely, I can connect you with a supervisor. Before I do, I want to confirm the overnight shipping upgrade has been processed. Your new delivery date is tomorrow by 10 AM.

[00:02:01] Customer: Fine. But this is the last time I'm ordering from your company.

[00:02:08] Agent: I understand, and again, I sincerely apologize. Let me transfer you to our customer experience manager now.
---

Customer Email: rebecca.williams@email.com
```

### Expected Behavior

| Step | Expected Outcome |
|------|------------------|
| 1. Extract Key Info | `order_number: ORD-2026-00089`, `customer_name: Rebecca Williams`, `customer_email: rebecca.williams@email.com` |
| 2. Airtable Lookup | Order found |
| 3. Flag Analysis | `flag_status: flagged`, `flag_reason: Negative sentiment detected - customer expressed frustration, threatened bad reviews, requested manager escalation` |
| 4. Routing | Takes "Flagged" path → Send Email + Slack |
| 5. Email Sent | To: rebecca.williams@email.com with acknowledgment of flagged conversation |
| 6. Slack Notification | Posted to #demo-notifications channel with customer details and review request |

### Expected Output

```json
{
  "flag_status": "flagged",
  "flag_reason": "Negative sentiment detected: Customer expressed significant frustration (45-minute hold time complaint, 'worst' company accusation, threat to leave bad reviews, manager escalation request). Situation involved service failure impacting customer's daughter's education.",
  "extracted_data": {
    "order_number": "ORD-2026-00089",
    "customer_name": "Rebecca Williams",
    "customer_email": "rebecca.williams@email.com",
    "call_sentiment": "negative",
    "escalation_requested": true,
    "service_recovery_offered": "overnight shipping + 20% discount"
  }
}
```

---

## Scenario 3 – Flagged (Compliance Issue - PII Handling)

**Description:** Agent mishandles customer personal information, triggering a compliance flag.

### How to Use
1. Navigate to the agent in Beam.ai
2. Click "Create Task"
3. Paste the transcript below in the task query field
4. Submit the task

### Sample Input (Task Query)

```
Analyze the following customer service call transcript for our BPO quality assurance process:

---
CALL TRANSCRIPT
Date: January 4, 2026
Duration: 6 minutes 12 seconds
Agent: David Chen
Customer: Margaret Thompson
Order Number: ORD-2026-00156

[00:00:00] Agent: TechGear Support, David speaking. How can I help?

[00:00:05] Customer: Hi, I need to update my credit card information for my subscription.

[00:00:11] Agent: Sure thing! Can you give me your full credit card number?

[00:00:17] Customer: It's 4532 7891 2345 6789.

[00:00:24] Agent: Got it. And what's the expiration date and the three-digit code on the back?

[00:00:30] Customer: 09/28 and the code is 847.

[00:00:35] Agent: Perfect, let me write that down... 4532 7891 2345 6789, expiring 09/28, CVV 847. Your order number?

[00:00:48] Customer: ORD-2026-00156.

[00:00:52] Agent: Thanks. I've updated everything. Your card is now on file.

[00:00:58] Customer: Great, thanks for your help.

[00:01:02] Agent: No problem. Anything else?

[00:01:05] Customer: No, that's all.

[00:01:08] Agent: Have a great day!
---

Customer Email: margaret.thompson@email.com
```

### Expected Behavior

| Step | Expected Outcome |
|------|------------------|
| 1. Extract Key Info | `order_number: ORD-2026-00156`, `customer_name: Margaret Thompson`, `customer_email: margaret.thompson@email.com` |
| 2. Airtable Lookup | Order found |
| 3. Flag Analysis | `flag_status: flagged`, `flag_reason: COMPLIANCE VIOLATION - Agent verbally repeated full credit card number, expiration, and CVV on recorded call. PCI-DSS violation.` |
| 4. Routing | Takes "Flagged" path → Send Email + Slack |
| 5. Slack Notification | URGENT notification to #demo-notifications with compliance violation details |

### Expected Output

```json
{
  "flag_status": "flagged",
  "flag_reason": "COMPLIANCE VIOLATION - PCI-DSS breach detected: Agent requested and verbally repeated full credit card number (4532 7891 2345 6789), expiration date (09/28), and CVV (847) on a recorded call. This constitutes a serious security and compliance violation requiring immediate review.",
  "extracted_data": {
    "order_number": "ORD-2026-00156",
    "customer_name": "Margaret Thompson",
    "customer_email": "margaret.thompson@email.com",
    "compliance_issue": "PCI-DSS_violation",
    "severity": "critical"
  }
}
```

---

## Scenario 4 – No Orders Found (Order Number Not in Database)

**Description:** Customer provides order number that doesn't exist in Airtable database. Agent exits without flag analysis.

### How to Use
1. Navigate to the agent in Beam.ai
2. Click "Create Task"
3. Paste the transcript below in the task query field
4. Submit the task

### Sample Input (Task Query)

```
Analyze the following customer service call transcript for our BPO quality assurance process:

---
CALL TRANSCRIPT
Date: January 7, 2026
Duration: 3 minutes 05 seconds
Agent: Emily Rodriguez
Customer: James Wilson
Order Number: ORD-9999-INVALID

[00:00:00] Agent: Thank you for calling TechGear Support. My name is Emily, how may I assist you today?

[00:00:08] Customer: Hi, I'm calling about order ORD-9999-INVALID. I think there might be an issue with my shipment.

[00:00:18] Agent: Let me look that up for you. Could you spell out the order number again?

[00:00:24] Customer: O-R-D-9999-INVALID.

[00:00:32] Agent: I'm not finding that order in our system. Are you sure that's the correct order number? Do you have a confirmation email?

[00:00:42] Customer: Let me check... oh, I think I might have the wrong company. This might be from another store.

[00:00:52] Agent: No problem! Would you like me to help you verify if you have any orders with us?

[00:00:58] Customer: No, I think I made a mistake. Sorry to bother you!

[00:01:03] Agent: Not a bother at all. Have a great day!
---

Customer Email: james.wilson@email.com
```

### Expected Behavior

| Step | Expected Outcome |
|------|------------------|
| 1. Extract Key Info | `order_number: ORD-9999-INVALID`, `customer_name: James Wilson`, `customer_email: james.wilson@email.com` |
| 2. Airtable Lookup | No records found matching order number |
| 3. Routing | Takes "No Orders Found" path → Exit Node |
| 4. Final Status | COMPLETED - No flag analysis performed, no notifications sent |

### Expected Output

```json
{
  "status": "no_order_found",
  "extracted_data": {
    "order_number": "ORD-9999-INVALID",
    "customer_name": "James Wilson",
    "customer_email": "james.wilson@email.com"
  },
  "reason": "Order number not found in Airtable database. No flag analysis performed."
}
```

---

## Scenario 5 – Edge Case (Mixed Sentiment - Resolved Complaint)

**Description:** Customer starts angry but ends satisfied. Tests edge case handling for sentiment analysis.

### How to Use
1. Navigate to the agent in Beam.ai
2. Click "Create Task"
3. Paste the transcript below in the task query field
4. Submit the task

### Sample Input (Task Query)

```
Analyze the following customer service call transcript for our BPO quality assurance process:

---
CALL TRANSCRIPT
Date: January 6, 2026
Duration: 5 minutes 33 seconds
Agent: Jennifer Park
Customer: Robert Martinez
Order Number: ORD-2026-00178

[00:00:00] Agent: Thank you for calling TechGear Support. My name is Jennifer, how may I assist you today?

[00:00:07] Customer: I'm really upset right now. My order ORD-2026-00178 arrived damaged and nobody has been able to help me!

[00:00:18] Agent: I'm so sorry to hear that, Mr. Martinez. That must be very frustrating. Let me take care of this for you right now.

[00:00:28] Customer: I've already called twice before and nothing has happened!

[00:00:33] Agent: I completely understand, and I apologize for the previous experiences. I'm going to personally ensure this gets resolved today. First, let me arrange a replacement to ship out today with overnight delivery at no charge.

[00:00:50] Customer: Okay... that would help.

[00:00:54] Agent: I've also applied a $50 credit to your account as an apology for the inconvenience. Would you like me to arrange a pickup for the damaged item, or should I send a return label?

[00:01:10] Customer: A return label would be easier.

[00:01:14] Agent: Perfect. I'm sending that to your email now, along with confirmation of your replacement shipment and the $50 credit. Is there anything else I can help with?

[00:01:28] Customer: No, actually... thank you, Jennifer. You've been really helpful. I appreciate you actually solving this for me.

[00:01:38] Agent: It's my pleasure, Mr. Martinez. I'm sorry again for the trouble. Your replacement will arrive tomorrow by noon. Have a wonderful day!

[00:01:48] Customer: You too! Thanks again.
---

Customer Email: robert.martinez@email.com
```

### Expected Behavior

| Step | Expected Outcome |
|------|------------------|
| 1. Extract Key Info | `order_number: ORD-2026-00178`, `customer_name: Robert Martinez`, `customer_email: robert.martinez@email.com` |
| 2. Airtable Lookup | Order found |
| 3. Flag Analysis | `flag_status: not_flagged`, `flag_reason: null` (initial complaint resolved successfully) |
| 4. Routing | Takes "Not Flagged" path → Exit Node |
| 5. Final Status | COMPLETED - Resolved complaint, positive ending |

### Expected Output

```json
{
  "flag_status": "not_flagged",
  "flag_reason": null,
  "extracted_data": {
    "order_number": "ORD-2026-00178",
    "customer_name": "Robert Martinez",
    "customer_email": "robert.martinez@email.com",
    "call_sentiment": "mixed_resolved_positive",
    "initial_issue": "damaged_item",
    "resolution": "replacement + $50 credit",
    "customer_satisfied": true
  },
  "analysis_notes": "Initial negative sentiment due to damaged item and previous unresolved contacts. Agent successfully de-escalated and resolved with replacement, overnight shipping, and account credit. Customer expressed gratitude at end of call."
}
```

---

## Airtable Test Data Requirements

For these test scenarios to work, ensure the following records exist in your Airtable base:

**Base ID:** `appaJAfTi3RohG8AB`
**Table ID:** `tblCsCjuFe5qj5nbc`

| Order Number | Customer Name | Customer Email | Status |
|--------------|---------------|----------------|--------|
| ORD-2026-00142 | John Anderson | john.anderson@email.com | Shipped |
| ORD-2026-00089 | Rebecca Williams | rebecca.williams@email.com | Delayed |
| ORD-2026-00156 | Margaret Thompson | margaret.thompson@email.com | Active |
| ORD-2026-00178 | Robert Martinez | robert.martinez@email.com | Replacement |

---

## Integration Requirements

### Gmail Integration
- Connected Gmail account for sending customer notification emails
- Sender will appear as configured Gmail account

### Slack Integration
- Connected Slack workspace
- Channel: `demo-notifications` (must exist and bot must have access)

### Airtable Integration
- Connected Airtable account with access to base `appaJAfTi3RohG8AB`
- Read access to orders table

---

## Testing Checklist

- [ ] Scenario 1: Verify no notifications sent for happy path
- [ ] Scenario 2: Verify email and Slack notification sent for negative sentiment
- [ ] Scenario 3: Verify URGENT compliance violation notification
- [ ] Scenario 4: Verify graceful handling when order not found
- [ ] Scenario 5: Verify mixed sentiment correctly analyzed as resolved

---

**Document Version:** 1.0
**Last Updated:** 2026-01-07
