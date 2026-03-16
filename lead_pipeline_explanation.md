# Neo ERP Lead Pipeline Overview

Based on the source code in `neo_erp_app`, your company uses a highly customized Lead pipeline centered around the **NT Lead** DocType, specifically designed to bridge Marketing and Sales seamlessly.

Here is a step-by-step breakdown of how the pipeline works:

## 1. Ingestion & Lead Pool (Marketing)
Leads primarily enter the system via the **Lead Pool API** (`lead_pool_api.py`).
- **Sources**: Webhooks via n8n from Meta, LinkedIn, Google Ads, or manually entered.
- **Deduplication**: The API automatically prevents duplicates by checking the `platform` and `platform_lead_id` against the `NT Lead Sync Log`.
- **Initial State**: New leads are created as `NT Lead` with their `lead_pool_status` set to **"Pool"**.
- Marketing can view the overall pipeline via the Lead Pool Summary dashboard.

## 2. Quality Scoring & Categorization (`nt_lead.py`)
Upon creation and on every update, the system automatically calculates a **Quality Score (0-100)**:
- **Budget / Expected Value**: +20 points
- **High-Quality Source** (Referral, Website, Existing Customer): +15 points
- **B2B with GSTIN**: +15 points (or +8 if just B2B without GSTIN)
- **Complete Contact Info** (Email & Mobile): +15 points
- **Pipeline Progress** (Contacted, Qualified, etc.): Up to +15 points
- **Product Interest / Address provided**: +10 points each

Based on this score, the lead is categorized:
- **Hot**: Score >= 70 (configurable in Sales Settings)
- **Warm**: Score >= 40
- **Cold**: Score < 40

## 3. Marketing to Sales Handoff
Leads don't go to Sales immediately. The Marketing Head manually or bulk pushes qualified leads from the Pool using the `send_to_sales` action.
- This changes the `lead_pool_status` to **"Sent to Sales"**.
- System notifications and real-time alerts are instantly fired to **Sales Heads** alerting them of new vetted leads.

## 4. Sales Assignment (`events.py`)
Once handed off to Sales, leads are assigned to Sales Executives via the `auto_assign_lead` strategy:
- **Hot Leads**: Automatically routed to the **Top Performer** (salesperson with the most conversions last month).
- **Warm Leads**: Distributed via **Round Robin** (assigned to the "Least Loaded" eligible sales rep).
- **Cold Leads**: Typically wait for manual assignment.

When assigned, the `lead_owner` is set, changing `lead_pool_status` to **"Assigned"**, and the specific sales executive gets notified.

## 5. Nurturing & Quoting
Sales reps work the lead through various statuses (`New` -> `Contacted` -> `Qualified` -> `Proposal Sent` -> `Negotiation`).
- A unique feature is the `create_quotation` method: Sales can generate an **NT Quotation** directly for the Lead *without* having to convert them to a customer yet.

## 6. Conversion to Customer
If the deal is won, the lead is converted into an **NT Customer** (`convert_to_customer`).
- Contacts, company name, GSTIN, and ownership details are seamlessly copied over.
- The Lead's status changes to **Won** and is linked to the new Customer record.

## 7. Ongoing Maintenance
A scheduler (`mql_scheduler.py`) automatically runs on the 1st and 15th of every month. It extracts MQL (Marketing Qualified Leads) data, compiling a summary of Hot/Warm/Cold leads and sends an automated detailed email report to the Marketing Heads for review.
