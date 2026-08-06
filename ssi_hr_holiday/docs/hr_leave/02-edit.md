# Edit Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
>
> **Actor:** user in group _Leave — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Leave — User_, and is the record's **Responsible** or
  **Employee** (record rule), or holds a broader data-ownership group (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Leave Type**, **Date Start**, **Date End**, or **Number of
   Days** as needed.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- **# Timesheet**, **Duration**, and **# Leave Allocation** are recomputed the same way
  as described in `01-create`.
