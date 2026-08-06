# Activate Timesheet Computation Item

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet_computation_item`
>
> **Menu:** Human Resource > Configuration > Timesheets > Timesheet Computation Items
>
> **Actor:** user in group _Timesheet Computation Item_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Timesheet Computation Item_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Timesheet Computation
   Items** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as a line item on a timesheet, and will reappear in
  `hr.timesheet.computation_ids` the next time **Reload** is used on the timesheet.
