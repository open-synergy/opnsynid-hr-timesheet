# Delete Leave Type

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Leave Type
>
> **Actor:** user in group _Leave Type_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Leave Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Leave Type** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system. Deletion fails with a
  database integrity error if the leave type is already referenced by an existing
  **Leave** or **Leave Allocation** record (both reference `hr.leave_type` with
  `ondelete="restrict"`) — deactivate the record instead (see `04-deactivate`).
