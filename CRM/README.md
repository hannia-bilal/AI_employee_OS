# AI CRM & Customer Management

This folder contains the CRM module for the AI Employee OS project. It provides a lightweight, extensible foundation for managing leads, tracking sales progress, recording customer activity, and generating customer summaries.

## Overview

The CRM package is designed to support the following business workflows:

- Lead management
- Sales pipeline tracking
- Activity timeline management
- Customer summary generation

## Implemented Modules

### 1. Lead Management
Located in [CRM/src/modules/lead_management](CRM/src/modules/lead_management)

Handles the creation, retrieval, updating, and listing of leads. Each lead stores:

- Name
- Email
- Company
- Phone
- Source
- Pipeline stage
- Notes

### 2. Sales Pipeline
Located in [CRM/src/modules/sales_pipeline](CRM/src/modules/sales_pipeline)

Tracks deals associated with leads and supports pipeline-stage updates such as:

- new
- qualified
- proposal
- won
- lost

### 3. Activity Timeline
Located in [CRM/src/modules/activity_timeline](CRM/src/modules/activity_timeline)

Stores timeline activities for each lead, such as:

- Calls
- Meetings
- Notes
- Follow-ups

### 4. Customer Summaries
Located in [CRM/src/modules/customer_summaries](CRM/src/modules/customer_summaries)

Generates simple customer summaries based on recent activities and lead context.

## Project Structure

```text
CRM/
├── README.md
└── src/
    └── modules/
        ├── activity_timeline/
        ├── customer_summaries/
        ├── lead_management/
        └── sales_pipeline/
```

## Integration

The CRM modules are connected to the backend CRM tools in [backend/tools/crm_tool.py](backend/tools/crm_tool.py), allowing the assistant to:

- Create leads
- Find existing customers
- Update CRM fields such as pipeline stage and notes

## Development Notes

The current implementation uses in-memory storage for demo and development purposes. It is ready for future expansion with:

- Database persistence
- API endpoints
- UI dashboard integration
- Advanced analytics and reporting

## Verification

The CRM modules are verified through automated tests in [tests/test_crm_modules.py](tests/test_crm_modules.py).

## Contribution

This CRM work was implemented as part of the AI Employee OS project and is intended to be expanded into a full customer relationship management experience.


## Done By
- **Faez Ahmed** - Responsible for CRM Module

