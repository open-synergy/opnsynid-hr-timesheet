# Create Timesheet

> **Module:** ssi_timesheet_attendance
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains these fields:

- **Schedule Source** _(required)_: Where the Attendance Schedule of this timesheet is
  generated from (see `ssi_timesheet_attendance/hr_timesheet/17-compute-schedule`):
  **Working Schedule** reads the attendance intervals of the working schedule;
  **Pattern** resolves the rules of an Attendance Schedule Pattern. When
  `ssi_timesheet_attendance_shift` is installed, **Shift Roster** is also offered.
  Automatically filled from **Employee**'s own Schedule Source, which starts from the
  company default. Editable only while the record is **Draft**.
- **Working Schedule** _(required for the Working Schedule and Pattern sources)_: The
  `resource.calendar` of this timesheet. Automatically filled from **Employee**'s
  default working calendar, if any — fill in manually if the employee has none
  configured. Editable only while the record is **Draft**.
- **Schedule Pattern** _(required for the Pattern source)_: The Attendance Schedule
  Pattern used when **Schedule Source** is **Pattern**; hidden for other sources.
  Automatically filled from **Employee**'s own Schedule Pattern. Editable only while the
  record is **Draft**.
