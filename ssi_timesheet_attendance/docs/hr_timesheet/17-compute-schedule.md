# Create Schedules — Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **Requires:** `ssi_timesheet/hr_timesheet/01-create`
>
> **Extends:** ssi_timesheet — model `hr.timesheet`

## Pre-Condition

- **Record:** Status is **Draft** or **On Progress**. **Working Schedule**, **Date
  Start**, and **Date End** must be filled — they are required to compute the schedule
  intervals.
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record (status **Draft** or **On Progress**).
3. On the **Attendance Schedules** tab, click **Create Schedules**
   (`action_compute_schedule`).
4. Click **OK** on the confirmation dialog ("Compute Schedules. Are you sure?").

## Post-Condition

- Existing `hr.timesheet_attendance_schedule` lines for this timesheet are removed and
  regenerated from **Working Schedule**'s attendance intervals between **Date Start**
  and **Date End**, excluding public holidays.
- Each attendance record already recorded on the **Attendance** tab is re-linked to the
  matching schedule slot for the same date, and each schedule slot's real
  attendance/deviation figures (Real Date Start/End, Early Start, Late Start, Finish
  Early, Finish Late) are recalculated from those attendance records.
- This step can be repeated at any time while the record is **Draft** or **On
  Progress**; running it again discards and regenerates all **Attendance Schedules**
  lines.
