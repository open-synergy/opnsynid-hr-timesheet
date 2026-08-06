# Deactivate Attendance Reason

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Reasons
>
> **Actor:** user in group _Attendance Reason_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Reasons** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as **Reason In** / **Reason Out** on new
  timesheet attendance records.
- Timesheet attendance records that already reference this reason can still be viewed.
