# Edit Attendance Shift

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shifts
>
> **Actor:** user in group _Attendance Shift_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shifts** menu.
2. Find and open the record to edit.
3. Change the required fields, for example **Work From**, **Duration (Hours)**, **Early
   Check In Tolerance**, or **Late Check Out Tolerance**.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- **Work To** and **Cross Day** are recomputed from the updated **Work From** and
  **Duration (Hours)**.
