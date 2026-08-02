# Delete Attendance Shift Pattern

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift_pattern`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shift Patterns
>
> **Actor:** user in group _Attendance Shift_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.
- **Record:** The pattern is not referenced by any Attendance Shift Assignment —
  deleting a pattern still in use is rejected.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shift Patterns**
   menu.
2. Open the record to delete.
3. Click the **Action** menu and select **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The record is permanently removed from the system, together with its cycle day lines.
- The deleted pattern no longer appears in the Attendance Shift Patterns list.
