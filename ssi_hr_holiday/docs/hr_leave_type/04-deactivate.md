# Deactivate Leave Type

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Leave Type
>
> **Actor:** user in group _Leave Type_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Leave Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Leave Type** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected on new **Leave** or **Leave Allocation**
  records.
- **Leave** and **Leave Allocation** records that already reference this leave type can
  still be viewed.
