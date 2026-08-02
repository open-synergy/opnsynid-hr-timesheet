# Activate Attendance Shift

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shifts
>
> **Actor:** user in group _Attendance Shift_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Attendance Shift_.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shifts** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again in new records that reference this shift.
