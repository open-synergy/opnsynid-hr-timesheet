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
3. Open the record to reactivate.
4. Click **Action** > **Unarchive**. The record is restored immediately — unlike
   Archive, Unarchive does not show a confirmation dialog.

## Post-Condition

- The record is restored and the **Archived** ribbon no longer appears.
- The record can be selected again in new records that reference this shift.
