# Create Attendance Shift Assignment

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift_assignment`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shift Assignments
>
> **Actor:** user in group _Attendance Shift_

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.
- **Record:** At least one Employee and one Attendance Shift Pattern exist.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shift
   Assignments** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Employee** _(required)_: Select the employee (crew member) this assignment is
     for.
   - **Pattern** _(required)_: Select the rotation pattern to assign.
   - **Cycle Offset (Days)** _(required)_: Enter the number of days that distinguishes
     this crew's rotation start from another crew sharing the same **Pattern**. Defaults
     to 0.
   - **Date Start** _(required)_: Enter the first calendar date this assignment applies
     from.
   - **Date End**: Enter the last calendar date this assignment applies to. Leave empty
     for an assignment with no end date.
4. Click **Save**.

## Post-Condition

- A new attendance shift assignment record is created, linking the employee to the
  pattern.
- An assignment with **Date End** left empty applies indefinitely.
