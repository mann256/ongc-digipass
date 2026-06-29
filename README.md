# ONGC DigiPass

## Project Overview

**ONGC DigiPass** is a web-based Gate Pass Management System developed
for **ONGC Ltd. -- Security Services**. The application digitizes the
complete material gate pass lifecycle by replacing manual paper-based
passes with a secure workflow featuring approval, QR-code verification,
PDF generation, and reporting.

The system supports both **Non-Returnable** and **Returnable** gate
passes and maintains a complete audit trail of security movements.

------------------------------------------------------------------------

# Organization Details

  Field              Details
  ------------------ ---------------------------------------------
  Project Name       ONGC DigiPass
  Organization       Oil and Natural Gas Corporation Ltd. (ONGC)
  Department         Security Services
  Application Type   Web Application
  Architecture       Full Stack Web Application

## Mentors

-   Anip C. Halpati
-   Arun Kumar Gupta
-   Virendra Singh
-   Suraj Singh
-   Saurabh Gupta

------------------------------------------------------------------------

# Objectives

-   Digitize the gate pass process.
-   Eliminate manual paperwork.
-   Generate unique QR-based gate passes.
-   Maintain complete movement history.
-   Support returnable and non-returnable materials.
-   Improve security verification.
-   Generate downloadable PDF gate passes.
-   Export gate pass records to Excel.

------------------------------------------------------------------------

# Major Features

-   Secure Login
-   Role-based access
-   Gate Pass Creation
-   Gate Pass Editing
-   Gate Pass Approval
-   QR Code Generation
-   Security Verification
-   Returnable Gate Pass Workflow
-   Dynamic Material Entry
-   PDF Generation
-   Excel Export
-   Search & Filter
-   Audit Trail

------------------------------------------------------------------------

# Technology Stack

  Layer       Technology
  ----------- ------------------------------------
  Backend     Python
  Framework   Flask
  Database    PostgreSQL / SQLAlchemy
  Frontend    HTML, CSS, Bootstrap 5, JavaScript
  PDF         ReportLab
  QR Code     qrcode
  Excel       OpenPyXL

------------------------------------------------------------------------

# User Roles

## User

-   Create Gate Pass
-   Edit Gate Pass before approval
-   Print Gate Pass
-   View Gate Pass List

## Approving Authority

-   Approve Gate Pass
-   Reject Gate Pass

## Gate Security

-   Verify QR Code
-   Perform Check-Out
-   Perform Check-In
-   Enter Guard Details
-   Enter Remarks

------------------------------------------------------------------------

# Gate Pass Workflow

``` text
Login
   │
   ▼
Create Gate Pass
   │
   ▼
Add Material Details
   │
   ▼
Submit
   │
   ▼
Approval
   │
   ▼
QR Code Generated
   │
   ▼
Security Verification
   │
   ▼
Completed
```

------------------------------------------------------------------------

# Non-Returnable Workflow

``` text
APPROVED
    │
    ▼
Security Check-Out
    │
    ▼
IN_TRANSIT
    │
    ▼
Security Check-In
    │
    ▼
COMPLETED
```

Information captured: - Guard Name - Date & Time - Remarks

------------------------------------------------------------------------

# Returnable Workflow

``` text
APPROVED
    │
    ▼
First Check-Out
    │
    ▼
IN_TRANSIT
    │
    ▼
First Check-In
    │
    ▼
Second Check-Out
    │
    ▼
IN_TRANSIT
    │
    ▼
Second Check-In
    │
    ▼
COMPLETED
```

For each movement the system records: - Guard Name - Time Stamp -
Remarks

------------------------------------------------------------------------

# QR Code Verification

Each approved gate pass contains a QR code.

When scanned:

-   Opens the Security Verification page.
-   Displays complete gate pass details.
-   Shows material information.
-   Allows only authorized security personnel to authenticate.
-   Updates gate pass status.

------------------------------------------------------------------------

# Gate Pass Status Lifecycle

## Non-Returnable

``` text
PENDING
 ↓
APPROVED
 ↓
IN_TRANSIT
 ↓
COMPLETED
```

## Returnable

``` text
PENDING
 ↓
APPROVED
 ↓
IN_TRANSIT
 ↓
COMPLETED
```

Movement stages: 1. First Check-Out 2. First Check-In 3. Second
Check-Out 4. Second Check-In

------------------------------------------------------------------------

# Material Details

Each gate pass supports multiple material entries.

Each material stores: - Item Number - Material Description - Asset /
Serial Number - Census Number (Optional) - Quantity - Remarks

------------------------------------------------------------------------

# PDF Generation

The application generates a professional PDF containing:

-   ONGC Branding
-   QR Code
-   Gate Pass Details
-   Material Details
-   Approval Details
-   Security Details
-   Footer with generation timestamp

For returnable gate passes:

-   First Movement
-   Second Movement

are displayed separately.

------------------------------------------------------------------------

# Excel Report

The system exports the last 30 days of gate passes.

Columns include:

-   Gate Pass Number
-   Created By
-   Receiver Name
-   Returnable
-   Material Details
-   Asset / Serial Number
-   Quantity

------------------------------------------------------------------------

# Database Overview

## GatePass

Stores: - Gate Pass Number - Status - Vehicle Details - Receiver
Details - Returnable Flag - Approval Details - Security Details -
Movement Information

## GatePassItem

Stores: - Item Number - Material Description - Asset / Serial Number -
Census Number - Quantity - Remarks

------------------------------------------------------------------------

# Security Features

-   QR-based verification
-   Role-based authentication
-   Security credential validation
-   Timestamp logging
-   Guard identification
-   Audit history

------------------------------------------------------------------------

# Validation Rules

-   Mandatory gate pass information.
-   At least one material item.
-   Positive quantity.
-   Unique gate pass number.
-   Security authentication required.
-   Completed gate passes cannot be modified.

------------------------------------------------------------------------

# Future Enhancements

-   Notification center
-   Dashboard analytics
-   Email alerts
-   SMS notifications
-   Digital signatures
-   Barcode support
-   Mobile application
-   Approval history
-   Advanced reporting

------------------------------------------------------------------------

# Conclusion

ONGC DigiPass modernizes the gate pass process by integrating secure
authentication, QR-code verification, digital approvals, PDF generation,
Excel reporting, and comprehensive movement tracking into a single web
application. The system improves operational efficiency, enhances
security, and provides a scalable platform for managing material
movement within ONGC Security Services.
