# Start Timesheet

> **Module:** ssi_work_log_mixin
>
> **Extends:** ssi_timesheet — model `hr.timesheet`, aksi `07-start`

## Additional Post-Condition

- The **Work Log** tab's **Work Log(s)** list becomes usable: work logs can be added
  from it (see `ssi_work_log_mixin/docs/hr_work_log/01-create.md`) while the timesheet
  stays **On Progress**. The tab itself is visible from creation onward, but a work log
  cannot be saved until the timesheet reaches this status — its **Timesheet** field is
  resolved by matching **Employee** and **Date** against an **On Progress** timesheet,
  and saving fails otherwise.
