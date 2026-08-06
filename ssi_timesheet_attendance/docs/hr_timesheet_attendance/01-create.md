# Create Timesheet Attendance

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet_attendance`
>
> **Menu:** Human Resource > Timesheets > Attendances
>
> **Actor:** user in group _Timesheet Attendance_

## Pre-Condition

- **Record:** An `hr.timesheet` for the current user's employee, covering **Date**,
  exists with status **On Progress**. The record cannot be saved otherwise — **Sheet**
  is resolved automatically from **Date** and the employee, and saving fails with an
  error if no matching open timesheet is found.
- **Access:** User is in group _Timesheet Attendance_.

## Flow

1. Open the **Human Resource > Timesheets > Attendances** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Date** _(required)_: Enter the calendar date this attendance belongs to. Must
     fall within the date range of an **On Progress** timesheet for the current user's
     employee.
   - **Check In** _(required)_: Automatically filled with the current date and time.
     Change if needed.
   - **Reason In**: Select a reason for the check-in. Optional.
   - **Check Out**: Enter the check-out date and time, if already known. Leave empty to
     fill in later (see `02-edit`).
   - **Reason Out**: Select a reason for the check-out. Optional; only meaningful once
     **Check Out** is filled.
4. Click **Save**.

## Post-Condition

- A new attendance record is created.
- **Sheet**, **Attendance Schedule**, **Valid Check In**, **Valid Check Out**, **Total
  Hour**, and **Total Valid Hour** are computed automatically from **Date**, **Check
  In**, and **Check Out**.
- Status becomes **Open** if only one of **Check In** / **Check Out** is filled, or
  **Present** once both are filled.
- The matching timesheet's daily summary is recalculated automatically.
- This record is more commonly created automatically via the **Sign In** / **Sign Out**
  action on the timesheet (see `ssi_timesheet_attendance/hr_timesheet/15-sign-in.md` and
  `ssi_timesheet_attendance/hr_timesheet/16-sign-out.md`), or via the attendance widget
  in the top bar, without opening this menu. This flow is for entering or correcting an
  attendance record directly.
