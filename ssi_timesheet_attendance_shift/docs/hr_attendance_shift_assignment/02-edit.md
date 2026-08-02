# Edit Attendance Shift Assignment

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift_assignment`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shift Assignments
>
> **Actor:** user in group _Attendance Shift_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shift
   Assignments** menu.
2. Find and open the record to edit.
3. Change the required fields, for example **Pattern**, **Cycle Offset (Days)**, **Date
   Start**, or **Date End**.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Saving a date range that overlaps another assignment of the same employee is rejected.
