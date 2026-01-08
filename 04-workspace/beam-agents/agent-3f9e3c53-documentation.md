# 🤖 Email Automation Agent

## Properties
- **Agent Template**: Email Automation Agent
- **Feasibility**: 🟡 Needs Review
- **Priority**: 2 - Medium
- **Status Platform**: Draft
- **Vertical/Teams**: [To be determined]
- **What it does**: [Auto-generated - please review and update]
- **Owner**: [To be assigned]
- **Internal Notes**: [Add context here]

---

▶ Email Automation Agent
### Email Automation Agent

**Description**

This agent automates send the entire personalized feedback to tenant channel.

the body of the email needs o be html to ensure line breaks and formatting. using gmail and airtable integrations. through a 7-step workflow.

---

### Trigger

[Describe what initiates this agent - manual trigger, webhook, schedule, etc.]

---

### Workflow

1. **Send Email** - Send the entire personalized feedback to tenant channel.

The body of the email needs o be HTML to ensure line breaks and formatting
2. **Tenant Response Generator** - Generate tailored responses for each tenant based on their specific inquiry, and tenant profile
3. **Tenant Profile Aggregator** - Aggregate all information related to a specific tenant or property unit from multiple communications and create a unified tenant profile/issue summary. This would involve combining the information from airtable and the extracted info from the documents
4. **Send Email** - Send email to internal team member for manually handle this usecaase as the details of the customer are not found in the database.

Make sure the body of the email also contiains available core details of the customer as well.

The body of the email should be in HTML format so that line breaks and formatting can be preserved
5. **Retrieve Airtable Records** - Fetch further details of the candidate from Airtable database.
6. **Create Airtable Records** - Create communication log in Airtable
7. **Communication Analysis Tool** - Analyze incoming communication to identify tenant information, communication type, priority level, and extract structured data from unstructured text
8. **Start** - Agent workflow begins

---

### Data Inputs

- **body**: HTML or markdown content of the email
- **email_address**: Comma-separated recipient email addresses
- **subject**: Subject line of the email
- **tenant_profile**: A unified tenant profile or issue summary that aggregates all information related to a specific tenant or property unit.
- **communication_type**: Identified communication type
- **priority_level**: Determined priority level
- **tenant_info**: Extracted tenant information
- **records**: [
  {
    "Communication ID": "[Generate unique identifier in format COM-XXX where XXX is a sequential number]",
    "Tenant ID": "[Insert the Tenant ID from Tenant Master Information table that matches this communication's tenant]",
    "Timestamp": "[Insert the date and time when the communication was received in ISO 8601 format: YYYY-MM-DDTHH:mm:ss]",
    "Communication Type": "[Select ONE from: Maintenance Request, Inquiry, Complaint, Contract Renewal, Invoice, Bill, General]",
    "Issue Category": "[Select ONE from: Plumbing, Electrical, HVAC, Appliance, Structural, Payment, Contract, Parking, Noise, Other]",
    "Channel": "[Select ONE from: Email, Phone, Portal, In-person]",
    "Subject": "[Insert the subject line or brief title of the communication]",
    "Issue Description": "[Insert the full detailed description of the issue, request, or inquiry as provided by the tenant in their communication]",
    "Attachment Info": "[Insert comma-separated list of attachment filenames if any were included, e.g., 'photo_001.jpg, invoice.pdf'. Leave blank if no attachments]",
    "Priority Level": "[Select ONE from: Urgent, Normal, Low based on the severity and time-sensitivity of the issue]",
    "Status": "[Select ONE from: Open, In Progress, Resolved, Closed based on current state of the communication]",
    "Response Sent": "In Progress",
    "Assigned To": "[Insert the name of the person, team, or contractor responsible for handling this communication, e.g., 'Sato Kenji', 'Tokyo HVAC Solutions', 'Accounting Department']",
    "Cost Amount": [Insert the cost amount in EUR as a number without currency symbol if there are costs associated with this communication, e.g., 15000. Leave blank if no costs. Do not make this a string. leave as integer],
    "Notes": "[Insert internal notes, updates, or comments about how this communication was handled, current status, or any follow-up actions needed]"
  }
]
- **initial_data**: All necessary fields for processing

---

### Expected Outputs

- **message_id**: -
- **message**: -
- **email_address**: -
- **label_ids**: -
- **thread_id**: -
- **tenant_profile**: A unified tenant profile or issue summary that aggregates all information related to a specific tenant or property unit.
- **records**: -
- **id**: -
- **Last Contact Date**: -
- **Risk Level**: -
- **Tenant Since Duration**: -
- **Account Manager**: -
- **Preferred Language**: -
- **Payment Status**: -
- **Tenant Type**: -
- **Contact Phone**: -
- **Contact Email**: -
- **Lease End Date**: -
- **Lease Start Date**: -
- **Property Location**: -
- **Unit Number**: -
- **Tenant Name**: -
- **Tenant ID**: -
- **fields**: -
- **createdTime**: -
- **Issue Description**: -
- **Communication Type**: -
- **Timestamp**: -
- **Issue Category**: -
- **Priority Level**: -
- **Channel**: -
- **Subject**: -
- **Status**: -
- **Response Sent**: -
- **Communication ID**: -
- **communication_type**: Identified communication type
- **priority_level**: Determined priority level
- **tenant_info**: Extracted tenant information

---

### Key Integrations

- **Gmail**: Email operations
  - Functions: GmailAction_SendEmail
- **Airtable**: Database storage and query
  - Functions: AirtableAction_GetRecords, AirtableAction_RecordCreate

---

## Summary

**Workspace Name**: [Workspace name]
**Industry**: [Industry/vertical]
**Agent Link**: https://app.beam.ai/[workspace-id]/3f9e3c53-d193-4f35-9227-3d274628b019

---

## Agent Setup Instructions

1. **Pre-Requisite**: [List required accounts, API keys, integrations]
2. Navigate to Beam AI dashboard
3. Click **Create** on the "Email Automation Agent"
4. Click **Create → Continue**
5. **Agent Settings**:
   - Configure trigger mechanism
   - Set up required integrations
   - Test with sample data
6. **Agent is Setup** and ready to use

---

## Technical Implementation Details

### Agent Graph Structure
- **Agent ID**: 3f9e3c53-d193-4f35-9227-3d274628b019
- **Graph ID**: 3d8defdd-490a-4deb-93fa-ea11d8c47702
- **Status**: Draft
- **Total Nodes**: 8
- **Total Edges**: 0

### Node Breakdown
1. **Send Email**: Send the entire personalized feedback to tenant channel.

The body of the email needs o be HTML to ensure line breaks and formatting
   - Description: Send an email to one or more recipients.
   - Inputs: 8 parameters (3 required)
   - Outputs: message_id, message, email_address
2. **Tenant Response Generator**: Generate tailored responses for each tenant based on their specific inquiry, and tenant profile
   - Description: The Tenant Response Generator is designed to create personalized responses for each tenant based on their specific inquiry and tenant profile. It analyzes tenant profiles to understand their needs and concerns, ensuring that responses are tailored to the tenant's specific context and requirements. The tool synthesizes information from various sources to create comprehensive tenant profiles, maintaining data integrity and providing well-informed responses. It is crucial for enhancing tenant satisfaction and improving communication efficiency. The tool facilitates effective communication and resolution by providing accurate and relevant responses.
   - Inputs: 1 parameters (1 required)
   - Outputs: tenant_profile
3. **Tenant Profile Aggregator**: Aggregate all information related to a specific tenant or property unit from multiple communications and create a unified tenant profile/issue summary. This would involve combining the information from airtable and the extracted info from the documents
   - Description: The Tenant Profile Aggregator is a tool designed to aggregate all information related to a specific tenant or property unit from multiple communications. It combines data from Airtable and extracted information from documents to create a unified tenant profile or issue summary. The tool ensures data integrity and accuracy while synthesizing information from various sources. It provides a comprehensive overview of tenant information and issues, facilitating decision-making and further analysis. The tool is essential for creating detailed profiles that enable effective management and resolution.
   - Inputs: 3 parameters (3 required)
   - Outputs: tenant_profile
4. **Send Email**: Send email to internal team member for manually handle this usecaase as the details of the customer are not found in the database.

Make sure the body of the email also contiains available core details of the customer as well.

The body of the email should be in HTML format so that line breaks and formatting can be preserved
   - Description: Send an email to one or more recipients.
   - Inputs: 8 parameters (3 required)
   - Outputs: message, email_address, label_ids
5. **Retrieve Airtable Records**: Fetch further details of the candidate from Airtable database.
   - Description: Retrieves records from an Airtable table, with optional filtering by field values.
   - Inputs: 3 parameters (2 required)
   - Outputs: records, id, Last Contact Date
6. **Create Airtable Records**: Create communication log in Airtable
   - Description: Creates new record(s) in an Airtable table with specified field values.
   - Inputs: 3 parameters (3 required)
   - Outputs: fields, records, Issue Description
7. **Communication Analysis Tool**: Analyze incoming communication to identify tenant information, communication type, priority level, and extract structured data from unstructured text
   - Description: This tool analyzes incoming communications to extract structured data. It identifies tenant information, communication type, and priority level from unstructured text. The tool ensures that all relevant information is captured accurately. It maintains data integrity and provides clear and concise output. The tool is crucial for decision-making and further analysis in the agent graph.
   - Inputs: 1 parameters (1 required)
   - Outputs: communication_type, priority_level, tenant_info
8. **Unknown**: Entry Node

### Error Handling
- All nodes configured with error handling
- Review error paths and retry logic in Beam AI editor


---

*Documentation generated automatically on demo-documentation-generation-agent*
*Agent Graph ID: 3d8defdd-490a-4deb-93fa-ea11d8c47702*