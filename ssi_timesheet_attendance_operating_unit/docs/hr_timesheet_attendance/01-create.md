# Create Timesheet Attendance

> **Module:** ssi_timesheet_attendance_operating_unit
>
> **Extends:** ssi_timesheet_attendance — model `hr.timesheet_attendance`, aksi
> `01-create`

## Additional Pre-Condition

- **Config:** Group `operating_unit.group_multi_operating_unit` is active — the
  **Operating Unit** field described below is only visible when this group is enabled.

## Additional Fields

When this module is installed, the create form gains one optional field:

- **Operating Unit**: The operating unit that owns this attendance record. Defaults to
  the current user's default operating unit. Automatically re-filled from the selected
  **Sheet**'s operating unit whenever **Sheet** changes. Visible only when group
  `operating_unit.group_multi_operating_unit` is active. The same field is also added
  (hidden by default) as an optional column in the **Attendances** list, and as a
  **Group By: Operating Unit** filter in the search view — both gated by the same group.

## Modified — Record Visibility

- A user granted the _Operating Unit_ data-ownership group for this model
  (`ssi_timesheet_operating_unit.hr_timesheet_ou_group`) only sees attendance records
  whose **Operating Unit** is one of the operating units assigned to them (record rule
  `hr_timesheet_attendance_rule_ou`). This is not a Flow step.
