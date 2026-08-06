# Create Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one required field:

- **Working Schedule** _(required)_: The `resource.calendar` used to compute this
  timesheet's Attendance Schedule (see
  `ssi_timesheet_attendance/hr_timesheet/17-compute-schedule`). Automatically filled
  from **Employee**'s default working calendar, if any — fill in manually if the
  employee has none configured. Editable only while the record is **Draft**.
