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
- **Check In Latitude**, **Check In Longitude**, **Check In Accuracy**, **Check Out
  Latitude**, **Check Out Longitude**, and **Check Out Accuracy** are recorded data:
  they are readonly and cannot be changed from this form. They are only ever written by
  the attendance mobile app over the REST API.
- **Check In Location** and **Check Out Location** are recomputed automatically whenever
  the matching coordinate pair changes (e.g. **Check Out Latitude**/**Check Out
  Longitude** filled in by a later Sign Out), following the same rule as `01-create`. If
  the company setting **Require Registered Attendance Location** is enabled and a
  filled-in coordinate resolves to no location, saving fails with an error instead.
