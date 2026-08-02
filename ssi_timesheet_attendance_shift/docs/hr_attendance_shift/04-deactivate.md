# Deactivate Attendance Shift

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shifts
>
> **Actor:** user in group _Attendance Shift_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Shift_.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shifts** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected in new records that reference this shift.
- Records that already reference this shift can still be viewed.
