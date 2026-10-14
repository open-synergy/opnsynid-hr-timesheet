# Edit Attendance Schedule Pattern

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

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Schedule
   Patterns** menu.
2. Find and open the record to edit.
3. Change the fields, for example **Name**, or add, change, or remove lines in the
   **Pattern Lines** and **Special Dates** tabs.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Timesheets that already have a schedule keep it. The new rules apply the next time
  **Create Schedules** is run on a timesheet that is **Draft** or **On Progress**.
