# Edit Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `02-edit`

## Additional Fields

- **Working Schedule** _(required)_: Editable only while the record is **Draft** (same
  restriction as the base **Edit** action). Change it to recompute a different
  Attendance Schedule the next time
  `ssi_timesheet_attendance/hr_timesheet/17-compute-schedule` is used.
