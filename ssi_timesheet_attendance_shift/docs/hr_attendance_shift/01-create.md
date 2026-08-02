# Create Attendance Shift

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shifts
>
> **Actor:** user in group _Attendance Shift_

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shifts** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label for the shift (for example "Night
     Shift").
   - **Code** _(required)_: Enter a unique code, or fill in "/" to assign one
     automatically.
   - **Work From** _(required)_: Enter the hour of day, between 0 and 23.99, at which
     the shift starts.
   - **Duration (Hours)** _(required)_: Enter the length of the shift in hours, greater
     than 0 and at most 24.
   - **Work To**: Automatically filled from **Work From** and **Duration (Hours)**.
     Read-only.
   - **Cross Day**: Automatically filled from **Work From** and **Duration (Hours)**.
     Read-only.
   - **Early Check In Tolerance**: Defaults to 2.0 hours. Change if needed.
   - **Late Check Out Tolerance**: Defaults to 3.0 hours. Change if needed.
4. Click **Save**.

## Post-Condition

- A new attendance shift record is created.
- **Work To** shows the wrap-around of **Work From** plus **Duration (Hours)** over 24
  hours.
- **Cross Day** is checked when **Work From** plus **Duration (Hours)** goes past
  midnight.
