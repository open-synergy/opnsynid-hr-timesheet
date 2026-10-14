# Edit Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `02-edit`

## Additional Fields

- **Schedule Source**, **Working Schedule** _(required for the Working Schedule and
  Pattern sources)_, and **Schedule Pattern** _(required for the Pattern source)_:
  Editable only while the record is **Draft** (same restriction as the base **Edit**
  action). Change them to recompute a different Attendance Schedule the next time
  `ssi_timesheet_attendance/hr_timesheet/17-compute-schedule` is used.
