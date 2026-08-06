# Delete Attendance Reason

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Reasons
>
> **Actor:** user in group _Attendance Reason_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** **Created By System** is not set. Records created automatically by the
  system (the default check-in / check-out reasons shipped with this module) can only be
  deleted by a user in the _ERP Manager_ (`base.group_erp_manager`) group.
- **Access:** User is in group _Attendance Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Reasons** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
