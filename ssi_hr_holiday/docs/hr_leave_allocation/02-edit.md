# Edit Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** user in group _Leave Allocation — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Leave Allocation — User_, and is the record's
  **Responsible** or **Employee** (record rule), or holds a broader data-ownership group
  (_Direct Subordinate_, _All Subordinate_, _Company_, _Company and All Child
  Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Find and open the record to edit.
3. Change **Leave Type**, **Employee**, **Date Start**, **Date End**, **Number of
   Days**, **Can be Extended**, or **Date Extended** as needed.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
