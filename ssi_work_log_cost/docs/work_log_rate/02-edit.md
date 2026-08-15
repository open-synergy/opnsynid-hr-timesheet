# Edit Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** user in group _Work Log Rate — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Work Log Rate — User_, and either is the record's
  **Employee** (record rule), or holds a broader data-ownership group (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Date**, **Date Start**, or **Date End** as needed — the same
   constraints described in `01-create` apply.
4. On the **General Rates** tab, add, change, or remove lines as needed — the same
   fields described in `01-create` apply.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
