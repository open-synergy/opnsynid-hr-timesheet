# Delete Attendance Schedule Pattern

> **Module:** `ssi_timesheet_attendance`
>
> **Model:** `hr.attendance_schedule_pattern`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Schedule Patterns
>
> **Actor:** user in group _Attendance Schedule Pattern_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Attendance Schedule Pattern_.
- **Record:** The pattern is not referenced by any Attendance Schedule line of a
  timesheet — deleting a pattern still in use is rejected.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Schedule
   Patterns** menu.
2. Open the record to delete.
3. Click the **Action** menu and select **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system, together with its lines and special
  dates.
- The deleted pattern no longer appears in the Attendance Schedule Patterns list.
