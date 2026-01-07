# Property Eligibility Checker

## Summary

| | |
|---|---|
| **Workspace Name** | Insurance Demo |
| **Industry** | Insurance / Property Coverage |
| **Use Case** | Property Coverage Eligibility Verification |
| **Agent Link** | https://app.beam.ai/12172090-4128-4dbb-ace2-0d60af617cb4/3aa08542-6f71-43e6-9120-72d78015e7ab |

---

## Agent Setup Instructions

1. **Pre-Requisites:**
   - Active Gmail account with API access enabled
   - Google Sheets workspace with Property Master Dataset
   - Beam AI workspace with Gmail and Google Sheets integrations enabled
   - Property Master spreadsheet configured with required columns (Property_ID, Property_Address, Owner_Name, Property_Type, Coverage_Limit, Inspection_Status)
   - Underwriting Approved spreadsheet for logging results

2. Navigate to Beam AI dashboard → Agents section

3. Click **Create** on "Property Eligibility Checker"

4. Click **Create → Continue**

▶ **Agent Settings:**

- **Trigger for Workflow:**
  - Service: Gmail Email Trigger
  - Configure: Inbox to monitor for incoming eligibility requests
  - Email format: Must contain Property_ID and property details

- **Configure Frequency:**
  - On-demand (triggered by incoming email) OR
  - Manual trigger for testing

- **Filter/Criteria:**
  - Emails containing "eligibility", "coverage request", or "Property ID"
  - Properties with valid Property_ID format (PROP###)

- **Gmail Integration:**
  - Connect Gmail account
  - Authorize send/receive permissions
  - Test connection with sample email

- **Google Sheets Integration:**
  - Connect Google account
  - Link Property Master Dataset spreadsheet
  - Link Underwriting Approved spreadsheet for logging
  - Configure read/write permissions

- **Advanced Settings:**
  - Eligible Inspection_Status values: "Passed" only
  - Auto-reply enabled: Yes
  - Log all verification results: Yes
  - Email template: Professional HTML format

---

# Branch: Property Eligibility Checker

**Description:**

The Property Eligibility Checker automates the end-to-end verification of property coverage eligibility requests. It receives customer emails, validates property details against a master database, applies underwriting criteria based on inspection status, and sends automated acceptance or rejection responses—all within seconds. This eliminates manual database lookups and ensures consistent, auditable eligibility decisions across all requests.

**Choose If:**
- You receive property coverage eligibility requests via email
- Your team manually checks property databases for each request
- You want consistent, rule-based eligibility decisions
- You need to process high volumes of eligibility requests quickly
- You want automatic email responses to customers
- You require audit trails for all eligibility decisions
- You need to track approved properties in a separate spreadsheet

---

## Graph & Step Details

### Graph

[Workflow diagram available in Beam AI graph editor]

### Step Details

1. **Step 1: Entry Node:** Workflow initialization. Triggered by incoming Gmail message. Validates email contains property information and prepares workflow context.

2. **Step 2: Property Underwriting Checker:** AI-powered extraction tool parses incoming email content. Identifies and extracts Property_ID, Property_Address, Owner_Name, Property_Type, and Coverage_Limit from unstructured email text. Handles various email formats and writing styles. Returns structured property data for verification.

3. **Step 3: Retrieve All Rows:** Queries Google Sheets API to retrieve complete Property Master Dataset. Fetches all rows including Property_ID, Property_Address, Owner_Name, Property_Type, Coverage_Limit, and Inspection_Status columns. Returns dataset for Property ID lookup.

4. **Step 4: Property ID Verification Tool:** Cross-references extracted sender_property_id against the underwriting_master_dataset. Performs exact match lookup on Property_ID column. Returns verification status: "Found" with full property record, or "Not Found" if Property_ID doesn't exist in database. Branches workflow based on result.

5. **Step 5: Claim Underwriting Analysis Tool:** For verified properties, evaluates Inspection_Status against eligibility criteria. Checks if status equals "Passed" (eligible) or "Failed"/"Pending" (not eligible). Analyzes property details against underwriting rules. Returns eligibility determination with supporting rationale. Branches to appropriate response path.

6. **Step 6: Reply to Email (Rejection - ID Not Found):** Sends rejection email when Property_ID not found in master database. Email explains property is not registered in the system and provides guidance on registration process. Uses professional HTML template. Threads reply to original email.

7. **Step 7: Reply to Email (Rejection - Not Eligible):** Sends rejection email when property exists but fails eligibility criteria (Inspection_Status ≠ "Passed"). Email explains specific criteria not met and offers opportunity for re-evaluation after inspection completion. Uses professional HTML template.

8. **Step 8: Underwriting Data Formatter:** For eligible properties, formats verification data for spreadsheet logging. Structures Property_ID, Verification_Status ("Verified"), and Eligibility_Criteria ("Passed") as comma-separated values for individual cell placement. Prepares data payload for Google Sheets update.

9. **Step 9: Update Sheet Cells:** Writes formatted verification data to Underwriting Approved spreadsheet. Appends new row with Property_ID, verification timestamp, status, and eligibility criteria. Creates audit trail for approved properties. Returns confirmation of successful update.

10. **Step 10: Reply to Email (Acceptance):** Sends acceptance email confirming property meets eligibility criteria. Email includes confirmation of coverage eligibility, next steps for policy activation, and contact information for questions. Uses professional HTML template. Completes workflow.

---

## Example Task Scenarios

### ▶ Scenario 1 – Valid Property with Passed Inspection (Approved)

**Description:**

This scenario demonstrates the agent evaluating a property that exists in the master database and has a "Passed" inspection status. The property meets all eligibility criteria and should be approved for coverage.

**How to use:**

1. Customer with registered property sends eligibility request email
2. Agent extracts Property ID: PROP001
3. Agent retrieves Property Master Dataset from Google Sheets
4. Property ID found in database ✓
5. Inspection_Status retrieved: "Passed" ✓
6. Eligibility analysis confirms all criteria met
7. Data formatted and logged to Underwriting Approved spreadsheet
8. Acceptance email sent to customer confirming eligibility
9. Customer receives response within seconds

**Data Input:**

- **Email From:** john.doe@email.com
- **Email Subject:** Coverage Request - PROP001
- **Email Body:** Property ID: PROP001, Address: 123 Main St, Springfield, IL, Owner: John Doe, Type: Single-Family Home, Coverage: $500,000
- **Master Dataset Record:** PROP001 | 123 Main St, Springfield, IL | John Doe | Single-Family Home | $500,000 | Passed

**Expected Output:**

- **property_verification_status:** Found
- **inspection_status:** Passed
- **eligibility_result:** Eligible
- **spreadsheet_update:** New row added to Underwriting Approved sheet with PROP001, Verified, Passed, timestamp
- **email_response:** Acceptance email sent confirming coverage eligibility
- **success:** true

**Expected Agent Behavior:**

- Successfully extracts Property ID from email
- Locates property in master database
- Identifies "Passed" inspection status
- Determines property is eligible
- Logs approval to tracking spreadsheet
- Sends professional acceptance email
- Completes workflow without errors

---

### ▶ Scenario 2 – Property ID Not Found in Database (Rejected)

**Description:**

This scenario demonstrates the agent handling a request for a property that doesn't exist in the master database. The Property ID is not registered, so the agent cannot verify eligibility and must reject the request.

**How to use:**

1. Customer sends eligibility request with unregistered Property ID
2. Agent extracts Property ID: PROP999
3. Agent retrieves Property Master Dataset
4. Property ID NOT found in database ✗
5. Workflow branches to rejection path (ID Not Found)
6. Rejection email sent explaining property is not registered
7. No spreadsheet update (property not approved)
8. Customer receives guidance on registration process

**Data Input:**

- **Email From:** new.customer@email.com
- **Email Subject:** New Coverage Request - PROP999
- **Email Body:** Property ID: PROP999, Address: 555 Unknown St, Chicago, IL, Owner: Jane Williams, Type: Townhouse, Coverage: $275,000
- **Master Dataset:** No matching record for PROP999

**Expected Output:**

- **property_verification_status:** Not Found
- **eligibility_result:** Not Applicable (verification failed)
- **spreadsheet_update:** None
- **email_response:** Rejection email explaining Property ID not found in system
- **success:** false (property not eligible)

**Expected Agent Behavior:**

- Correctly extracts Property ID from email
- Searches master database thoroughly
- Identifies Property ID doesn't exist
- Does NOT attempt eligibility analysis
- Does NOT update tracking spreadsheet
- Sends helpful rejection email with registration guidance
- Completes workflow on rejection path

---

### ▶ Scenario 3 – Property Exists but Inspection Failed (Rejected)

**Description:**

This scenario demonstrates the agent handling a registered property that fails eligibility due to "Failed" inspection status. The property exists but doesn't meet underwriting criteria.

**How to use:**

1. Customer with registered property (failed inspection) sends request
2. Agent extracts Property ID: PROP004
3. Agent retrieves Property Master Dataset
4. Property ID found in database ✓
5. Inspection_Status retrieved: "Failed" ✗
6. Eligibility analysis determines property not eligible
7. Rejection email sent explaining failed inspection
8. No spreadsheet update (property not approved)
9. Customer informed of reason and potential remediation

**Data Input:**

- **Email From:** sarah.johnson@email.com
- **Email Subject:** Eligibility Check - PROP004
- **Email Body:** Property ID: PROP004, Address: 101 Maple Dr, Seattle, WA, Owner: Sarah Johnson, Type: Commercial, Coverage: $450,000
- **Master Dataset Record:** PROP004 | 101 Maple Dr, Seattle, WA | Sarah Johnson | Commercial | $450,000 | Failed

**Expected Output:**

- **property_verification_status:** Found
- **inspection_status:** Failed
- **eligibility_result:** Not Eligible
- **spreadsheet_update:** None
- **email_response:** Rejection email explaining property failed inspection criteria
- **success:** false (property not eligible)

**Expected Agent Behavior:**

- Successfully extracts Property ID
- Locates property in master database
- Identifies "Failed" inspection status
- Determines property is NOT eligible
- Does NOT log to approved spreadsheet
- Sends clear rejection email explaining reason
- Offers guidance on re-inspection process

---

### ▶ Scenario 4 – Property with Pending Inspection (Rejected)

**Description:**

This scenario demonstrates handling a property with "Pending" inspection status. The property exists but cannot be approved until inspection is completed.

**How to use:**

1. Customer with property awaiting inspection sends request
2. Agent extracts Property ID: PROP002
3. Agent retrieves master dataset and locates property
4. Inspection_Status: "Pending" ✗
5. Eligibility analysis determines cannot approve yet
6. Rejection email sent explaining pending inspection
7. Customer advised to reapply after inspection completion

**Data Input:**

- **Email From:** alice.smith@email.com
- **Email Subject:** Coverage Verification - PROP002
- **Email Body:** Property ID: PROP002, Address: 456 Oak Ave, Denver, CO, Owner: Alice Smith, Type: Condo, Coverage: $350,000
- **Master Dataset Record:** PROP002 | 456 Oak Ave, Denver, CO | Alice Smith | Condo | $350,000 | Pending

**Expected Output:**

- **property_verification_status:** Found
- **inspection_status:** Pending
- **eligibility_result:** Not Eligible (pending inspection)
- **spreadsheet_update:** None
- **email_response:** Rejection email explaining inspection is pending
- **success:** false

**Expected Agent Behavior:**

- Extracts Property ID correctly
- Finds property in database
- Identifies "Pending" status
- Determines cannot approve until inspection complete
- Sends informative rejection email
- Advises customer on expected timeline

---

## How To Use

▶ **Trigger (Manual):**

1. Log in to Beam AI dashboard
2. Navigate to Agents → Property Eligibility Checker
3. Click **Create Task**
4. Enter required input:
   - **email_input:** Full email content with property details
   - **spreadsheet_url:** URL to Property Master Dataset
5. Click **Run**
6. Monitor task execution in dashboard
7. View results: verification status, eligibility decision, email sent confirmation
8. Check Google Sheets for logged approval (if applicable)

▶ **Trigger (Email - Automated):**

1. Configure Gmail trigger in Beam AI
2. Monitor inbox for emails containing eligibility keywords
3. Agent runs automatically when matching email received
4. Payload automatically extracted from email:
   ```json
   {
     "email_input": "{{email.body}}",
     "message_id": "{{email.id}}",
     "sender_email": "{{email.from}}"
   }
   ```
5. Response sent automatically to original sender

▶ **Postman (API Usage):**

```bash
POST https://api.beamstudio.ai/agent-tasks/3aa08542-6f71-43e6-9120-72d78015e7ab/webhook/{webhook-id}
Content-Type: application/json

{
  "email_input": "Property ID: PROP001\nAddress: 123 Main St\nOwner: John Doe",
  "spreadsheet_url": "https://docs.google.com/spreadsheets/d/xxx",
  "timestamp": "2026-01-06T10:00:00Z"
}
```

Response:
```json
{
  "taskId": "task-12345",
  "status": "queued",
  "message": "Eligibility check initiated"
}
```

▶ **Dashboard:**

- **Monitor execution:** https://app.beam.ai/12172090-4128-4dbb-ace2-0d60af617cb4/3aa08542-6f71-43e6-9120-72d78015e7ab/tasks
- **View task details:** Click on specific task ID
- **See full execution log** with each node's input/output
- **Download** verification results and email records
- **Audit trail:** All eligibility decisions logged with timestamps

---

*Documentation generated: 2026-01-06*
