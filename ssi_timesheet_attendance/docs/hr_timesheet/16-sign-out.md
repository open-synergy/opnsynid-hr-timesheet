# Sign Out — Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **Requires:** `15-sign-in`
>
> **Extends:** ssi_timesheet — model `hr.timesheet`

## Pre-Condition

- **Record:** Status is **On Progress**. The **Sign Out** button is only visible while
  the timesheet is On Progress and the employee's **Attendance Status** is **Sign In**
  (i.e. a Sign In was already done and not yet closed).
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record to sign out from (status **On Progress**, employee currently signed
   in).
3. On the **Attendance** tab, click **Sign Out** (`action_sign_out`).

## Post-Condition

- In the usual case, the employee's latest (open) `hr.timesheet_attendance` record is
  updated: **Check Out** is set to the current date and time, with no **Reason Out**
  filled by this button.
- If the check-out date falls on a different date than the attendance's **Date** _and_
  the gap from the **Working Schedule**'s scheduled end exceeds the company's **Check
  Out Buffer** (`res.company`, Attendance settings — 0.0 hours if not configured), the
  sign-out is treated as an anomaly instead: a **new**, already-closed
  `hr.timesheet_attendance` record is created (**Check In** = **Check Out** = now), with
  **Reason In** / **Reason Out** defaulted from the company's **Check In Reason** /
  **Check Out Reason** (falling back to this module's default _[SYSTEM] Automatic check
  in/out due to inactivity_ reasons when the company fields are empty).
- Either way, the resulting entry can be corrected afterward by editing it directly on
  the **Attendance** tab, or via
  `ssi_timesheet_attendance/hr_timesheet_attendance/02-edit`.
- **Attendance Status** changes to **Sign Out**; the **Sign Out** button becomes hidden
  and **Sign In** becomes visible.
- Sign Out is also available without opening this menu, from the attendance widget in
  the top bar (calls the same action through the employee's active timesheet).
