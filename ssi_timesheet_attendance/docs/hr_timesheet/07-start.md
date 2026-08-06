# Start Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `07-start`

## Additional Post-Condition

- The **Attendance** and **Attendance Schedules** tabs become usable: **Sign In** /
  **Sign Out** (see `ssi_timesheet_attendance/hr_timesheet/15-sign-in` and
  `16-sign-out`) and **Create Schedules** (see
  `ssi_timesheet_attendance/hr_timesheet/17-compute-schedule`) become available while
  the record stays **On Progress**.
