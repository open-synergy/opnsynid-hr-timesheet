# Edit Timesheet Attendance

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet_attendance`
>
> **Menu:** Human Resource > Timesheets > Attendances
>
> **Actor:** user in group _Timesheet Attendance_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Timesheet Attendance_.

## Flow

1. Open the **Human Resource > Timesheets > Attendances** menu.
2. Find and open the record to edit.
3. Change **Date**, **Check In**, **Reason In**, **Check Out**, or **Reason Out** as
   needed.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- **Sheet**, **Attendance Schedule**, **Valid Check In**, **Valid Check Out**, **Total
  Hour**, and **Total Valid Hour** are recomputed automatically.
- Status is recomputed to **Present** once both **Check In** and **Check Out** are
  filled, or back to **Open** if one of them is cleared.
- The matching timesheet's daily summary is recalculated automatically whenever
  **Date**, **Check In**, or **Check Out** changes.
