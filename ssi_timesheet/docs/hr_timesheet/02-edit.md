# Edit Timesheet

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_reload_timesheet_computation` (Reload),
> `action_compute_computation` (Compute)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Timesheets — User_, and is the record's **Responsible**
  or **Employee** (record rule), or holds a broader data-ownership group (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Date Start**, or **Date End** as needed.
4. On the **Computations** tab, click **Reload** to refresh the computation lines after
   changing **Employee** — items no longer registered on the new employee are removed
   and newly registered items are added. Click **Compute** afterward to re-evaluate
   **Amount** and **Final Amount**. Both steps also run automatically when the record is
   **Started** or **Confirmed**.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
