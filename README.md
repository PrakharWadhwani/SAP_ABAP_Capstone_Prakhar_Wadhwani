# Z_VENDOR_INVOICE_REPORT — SAP ABAP Capstone Project

## Overview
Custom ALV Report for Vendor Invoice Analysis in SAP FI-AP module.

## Program Details
| Field         | Value                        |
|---------------|------------------------------|
| Program Name  | Z_VENDOR_INVOICE_REPORT      |
| Type          | Executable Program (Report)  |
| Module        | FI-AP (Accounts Payable)     |
| Author        | [YOUR NAME]                  |
| Roll No       | [YOUR ROLL NUMBER]           |
| Batch/Program | [YOUR BATCH/PROGRAM]         |

## Tables Used
| Table | Description                        |
|-------|------------------------------------|
| BSIK  | AP Open Items (Unpaid Invoices)    |
| BSAK  | AP Cleared Items (Paid Invoices)   |
| LFA1  | Vendor Master – General Data       |

## How to Upload to SAP SE38
1. Log in to your SAP System (use SAP Logon or SAP GUI).
2. Go to Transaction **SE38**.
3. Enter program name: `Z_VENDOR_INVOICE_REPORT`
4. Click **Create** → Select type **Executable Program**.
5. Paste the entire content of `Z_VENDOR_INVOICE_REPORT.abap`.
6. Click **Save** → Assign to a Package (e.g., `$TMP` for local).
7. Press **F8** to Activate, then **F8** to Execute.

## Selection Screen Parameters
| Parameter | Description                              |
|-----------|------------------------------------------|
| s_bukrs   | Company Code (Mandatory)                 |
| s_lifnr   | Vendor Number (Optional)                 |
| s_bldat   | Document Date Range (Optional)           |
| s_budat   | Posting Date Range (Optional)            |
| s_gjahr   | Fiscal Year Range (Optional)             |
| p_blart   | Document Type (Default: KR = Vendor Inv) |
| p_open    | Checkbox: Include Open Items             |
| p_clear   | Checkbox: Include Cleared Items          |
| p_vari    | ALV Display Variant (Optional)           |

## Submission Files
- `Z_VENDOR_INVOICE_REPORT.abap` — Main ABAP program source code
- `Project_Documentation.pdf`   — Project documentation (as per guidelines)
- `README.md`                   — This file

