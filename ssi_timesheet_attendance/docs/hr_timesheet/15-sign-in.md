# Sign In — Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **Requires:** `ssi_timesheet/hr_timesheet/07-start`
>
> **Extends:** ssi_timesheet — model `hr.timesheet`

## Pre-Condition

- **Record:** Status is **On Progress**. The **Sign In** button is only visible while
  the timesheet is On Progress and the employee's **Attendance Status** is **Sign Out**.
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record to sign in for (status **On Progress**).
3. On the **Attendance** tab, click **Sign In** (`action_sign_in`).

## Post-Condition

- A new `hr.timesheet_attendance` record is created for the employee, with **Check In**
  set to the current date and time and **Date** set to today (see
  `ssi_timesheet_attendance/hr_timesheet_attendance/01-create`). No **Reason In** is set
  by this button — it can be filled in afterward by editing the new row directly on the
  **Attendance** tab, or via `ssi_timesheet_attendance/hr_timesheet_attendance/02-edit`.
- **Attendance Status** changes to **Sign In**; the **Sign In** button becomes hidden
  and **Sign Out** becomes visible.
- **Latest Attendance** is updated to point to the new record.
- Sign In is also available without opening this menu, from the attendance widget in the
  top bar (calls the same action through the employee's active timesheet).
