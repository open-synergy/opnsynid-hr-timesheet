# Create Timesheet

> **Module:** ssi_work_log_mixin
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `01-create`

## Additional Fields

When this module is installed, the form gains a **Work Log** tab with two inputs
(besides the **Work Log(s)** list itself — see
`ssi_work_log_mixin/docs/hr_timesheet/07-start.md`):

- **Estimation**: The planned total work hours for this timesheet. Optional. Used to
  compute **Remaining** and **Excess** against the sum of logged **Duration**.
- **Work Log Analytic Account**: An analytic account associated with this timesheet for
  work log purposes. Optional.

Both fields are editable at any time, regardless of the timesheet's status.
