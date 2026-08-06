# Edit Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Overtime — User_, and is the record's **Responsible** or
  **Employee** (record rule), or holds a broader data-ownership group (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Overtime Type**, **Date**, **Date Start**, or **Date End** as
   needed — the same constraints described in `01-create` apply.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- **# Timesheet**, **Planned Hours**, and **Realized Hours** are recomputed
  automatically (same effect as described in `01-create`).
