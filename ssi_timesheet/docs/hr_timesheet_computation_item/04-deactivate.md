# Deactivate Timesheet Computation Item

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet_computation_item`
>
> **Menu:** Human Resource > Configuration > Timesheets > Timesheet Computation Items
>
> **Actor:** user in group _Timesheet Computation Item_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Timesheet Computation Item_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Timesheet Computation
   Items** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as a line item on a timesheet.
- Timesheet computation lines that already reference this item can still be viewed, but
  will be dropped from `hr.timesheet.computation_ids` the next time **Reload** is used
  on the timesheet.
