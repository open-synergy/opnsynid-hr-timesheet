# Agent Instructions — opnsynid-hr-timesheet

This file is intended for **AI assistants** (GitHub Copilot, Claude, Cursor, ChatGPT,
and similar tools) working inside this repository.

This repository provides Odoo modules for HR timesheet, attendance, work log, overtime,
and leave (holiday) management for PT. Simetri Sinergi Indonesia (SSI) / OpenSynergy
Indonesia, targeting Odoo 14.0.

---

## Modules in This Repository

| Module                                                    | Description                                                       |
| --------------------------------------------------------- | ----------------------------------------------------------------- |
| `ssi_holiday_state_change_constrain`                      | Employee Holiday + State Change Constrain Integration             |
| `ssi_hr_holiday`                                          | Leave Management                                                  |
| `ssi_hr_holiday_documenso_signing`                        | HR Holiday - Documenso Signing Integration                        |
| `ssi_hr_holiday_operating_unit`                           | Leave + Operating Unit                                            |
| `ssi_hr_leave_allocation_request_batch`                   | Leave Allocation Request Batch                                    |
| `ssi_hr_leave_allocation_request_batch_documenso_signing` | HR Leave Allocation Request Batch - Documenso Signing Integration |
| `ssi_hr_leave_allocation_request_batch_operating_unit`    | Leave Allocation Request Batch + Operating Unit                   |
| `ssi_hr_leave_request_batch`                              | Leave Request Batch                                               |
| `ssi_hr_leave_request_batch_documenso_signing`            | HR Leave Request Batch - Documenso Signing Integration            |
| `ssi_hr_leave_request_batch_operating_unit`               | Leave Request Batch + Operating Unit                              |
| `ssi_hr_overtime`                                         | Overtime Management                                               |
| `ssi_hr_overtime_account`                                 | Overtime Account                                                  |
| `ssi_hr_overtime_batch`                                   | Human Resource Overtime Batch                                     |
| `ssi_hr_overtime_batch_operating_unit`                    | Overtime Batch + Operating Unit                                   |
| `ssi_hr_overtime_documenso_signing`                       | HR Overtime - Documenso Signing Integration                       |
| `ssi_hr_overtime_operating_unit`                          | Overtime Management + Operating Unit                              |
| `ssi_hr_overtime_state_change_constrain`                  | Overtime State Change Constrain                                   |
| `ssi_timesheet`                                           | Timesheets                                                        |
| `ssi_timesheet_attendance`                                | Timesheet Attendance                                              |
| `ssi_timesheet_attendance_operating_unit`                 | Timesheet + Attendance + Operating Unit                           |
| `ssi_timesheet_attendance_shift`                          | Timesheet Attendance Shift                                        |
| `ssi_timesheet_attendance_work_log`                       | Timesheet + Attendance + Work Log                                 |
| `ssi_timesheet_documenso_signing`                         | Timesheet - Documenso Signing Integration                         |
| `ssi_timesheet_operating_unit`                            | Timesheet + Operating Unit                                        |
| `ssi_timesheet_state_change_constrain`                    | Timesheet State Change Constrain                                  |
| `ssi_work_log_cost`                                       | Work Log Cost                                                     |
| `ssi_work_log_expense`                                    | Work Log Expense                                                  |
| `ssi_work_log_expense_work_log`                           | Worklog Expense - Work Log Integration                            |
| `ssi_work_log_mixin`                                      | Work Log Mixin                                                    |
| `ssi_work_log_state_change_constrain`                     | Work Log State Change Constrain                                   |
| `test_ssi_work_log_mixin`                                 | Test Module - Work Log Mixin                                      |

---

## User Guide (Work Instructions)

Each module has a `docs/` directory containing **Work Instructions (IK)** — step-by-step
operational documentation for using the feature from the user's perspective.

### How to Answer User Questions About Feature Usage

1. Identify the feature being asked about.
2. Find the relevant Work Instruction from the index below.
3. **Read that file** before answering — do not fabricate steps from assumptions.
4. If a relevant extension module is installed (marked _additive_ below), also read its
   Work Instruction and **merge** it with the base IK.
5. Answer based on the content of the Work Instruction.

### Work Instruction Location Pattern

```
<module_name>/docs/<model_name>/<number>-<action>.md
```

---

## Work Instruction Index

### `ssi_timesheet` — Model: `hr.timesheet`

Menu: **Human Resource > Timesheets > Timesheets**

| File                                                     | Action                                    |
| -------------------------------------------------------- | ----------------------------------------- |
| `ssi_timesheet/docs/hr_timesheet/01-create.md`           | Create a new timesheet                    |
| `ssi_timesheet/docs/hr_timesheet/02-edit.md`             | Edit a timesheet                          |
| `ssi_timesheet/docs/hr_timesheet/03-delete.md`           | Delete a timesheet                        |
| `ssi_timesheet/docs/hr_timesheet/04-confirm.md`          | Confirm a timesheet (submit for approval) |
| `ssi_timesheet/docs/hr_timesheet/05-approve.md`          | Approve a timesheet                       |
| `ssi_timesheet/docs/hr_timesheet/06-reject.md`           | Reject a timesheet                        |
| `ssi_timesheet/docs/hr_timesheet/07-start.md`            | Start a timesheet                         |
| `ssi_timesheet/docs/hr_timesheet/10-cancel.md`           | Cancel a timesheet                        |
| `ssi_timesheet/docs/hr_timesheet/12-restart.md`          | Restart a cancelled/rejected timesheet    |
| `ssi_timesheet/docs/hr_timesheet/13-reset-number.md`     | Reset a timesheet's document number       |
| `ssi_timesheet/docs/hr_timesheet/14-restart-approval.md` | Restart a timesheet's approval process    |

### `ssi_timesheet` — Model: `hr.timesheet_computation_item`

Menu: **Human Resource > Configuration > Timesheets > Timesheet Computation Items**

| File                                                                | Action                                  |
| ------------------------------------------------------------------- | --------------------------------------- |
| `ssi_timesheet/docs/hr_timesheet_computation_item/01-create.md`     | Create a new timesheet computation item |
| `ssi_timesheet/docs/hr_timesheet_computation_item/02-edit.md`       | Edit a timesheet computation item       |
| `ssi_timesheet/docs/hr_timesheet_computation_item/03-delete.md`     | Delete a timesheet computation item     |
| `ssi_timesheet/docs/hr_timesheet_computation_item/04-deactivate.md` | Deactivate a timesheet computation item |
| `ssi_timesheet/docs/hr_timesheet_computation_item/05-activate.md`   | Activate a timesheet computation item   |
| `ssi_timesheet/docs/hr_timesheet_computation_item/06-reset-code.md` | Reset the code of one or more items     |

### `ssi_hr_overtime` — Model: `hr.overtime`

Menu: **Human Resource > Timesheets > Overtimes**

| File                                                      | Action                                    |
| --------------------------------------------------------- | ----------------------------------------- |
| `ssi_hr_overtime/docs/hr_overtime/01-create.md`           | Create a new overtime                     |
| `ssi_hr_overtime/docs/hr_overtime/02-edit.md`             | Edit an overtime                          |
| `ssi_hr_overtime/docs/hr_overtime/03-delete.md`           | Delete an overtime                        |
| `ssi_hr_overtime/docs/hr_overtime/04-confirm.md`          | Confirm an overtime (submit for approval) |
| `ssi_hr_overtime/docs/hr_overtime/05-approve.md`          | Approve an overtime                       |
| `ssi_hr_overtime/docs/hr_overtime/06-reject.md`           | Reject an overtime                        |
| `ssi_hr_overtime/docs/hr_overtime/10-cancel.md`           | Cancel an overtime                        |
| `ssi_hr_overtime/docs/hr_overtime/12-restart.md`          | Restart a cancelled/rejected overtime     |
| `ssi_hr_overtime/docs/hr_overtime/13-reset-number.md`     | Reset an overtime's document number       |
| `ssi_hr_overtime/docs/hr_overtime/14-restart-approval.md` | Restart an overtime's approval process    |

### `ssi_hr_overtime` — Model: `hr.overtime_type`

Menu: **Human Resource > Configuration > Timesheets > Overtime Types**

| File                                                     | Action                      |
| -------------------------------------------------------- | --------------------------- |
| `ssi_hr_overtime/docs/hr_overtime_type/01-create.md`     | Create a new overtime type  |
| `ssi_hr_overtime/docs/hr_overtime_type/02-edit.md`       | Edit an overtime type       |
| `ssi_hr_overtime/docs/hr_overtime_type/03-delete.md`     | Delete an overtime type     |
| `ssi_hr_overtime/docs/hr_overtime_type/04-deactivate.md` | Deactivate an overtime type |
| `ssi_hr_overtime/docs/hr_overtime_type/05-activate.md`   | Activate an overtime type   |

### `ssi_hr_overtime_batch` — Model: `hr.overtime_batch`

Menu: **Human Resource > Timesheets > Overtime Batch**

| File                                                                  | Action                                                                           |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/01-create.md`           | Create a new overtime batch                                                      |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/02-edit.md`             | Edit an overtime batch                                                           |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/03-delete.md`           | Delete an overtime batch                                                         |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/04-confirm.md`          | Confirm an overtime batch (creates & confirms the derived overtimes)             |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/05-approve.md`          | Approve an overtime batch (approves the derived overtimes too)                   |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/06-reject.md`           | Reject an overtime batch (rejects the derived overtimes too)                     |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/10-cancel.md`           | Cancel an overtime batch (cancels the derived overtimes too)                     |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/12-restart.md`          | Restart a cancelled/rejected overtime batch (restarts the derived overtimes too) |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/13-reset-number.md`     | Reset an overtime batch's document number                                        |
| `ssi_hr_overtime_batch/docs/hr_overtime_batch/14-restart-approval.md` | Restart an overtime batch's approval process                                     |

### `ssi_hr_holiday` — Model: `hr.leave`

Menu: **Human Resource > Timesheets > Leaves**

| File                                                  | Action                                |
| ----------------------------------------------------- | ------------------------------------- |
| `ssi_hr_holiday/docs/hr_leave/01-create.md`           | Create a new leave                    |
| `ssi_hr_holiday/docs/hr_leave/02-edit.md`             | Edit a leave                          |
| `ssi_hr_holiday/docs/hr_leave/03-delete.md`           | Delete a leave                        |
| `ssi_hr_holiday/docs/hr_leave/04-confirm.md`          | Confirm a leave (submit for approval) |
| `ssi_hr_holiday/docs/hr_leave/05-approve.md`          | Approve a leave                       |
| `ssi_hr_holiday/docs/hr_leave/06-reject.md`           | Reject a leave                        |
| `ssi_hr_holiday/docs/hr_leave/10-cancel.md`           | Cancel a leave                        |
| `ssi_hr_holiday/docs/hr_leave/12-restart.md`          | Restart a cancelled/rejected leave    |
| `ssi_hr_holiday/docs/hr_leave/13-reset-number.md`     | Reset a leave's document number       |
| `ssi_hr_holiday/docs/hr_leave/14-restart-approval.md` | Restart a leave's approval process    |

### `ssi_hr_holiday` — Model: `hr.leave_allocation`

Menu: **Human Resource > Timesheets > Leave Allocations**

| File                                                             | Action                                           |
| ---------------------------------------------------------------- | ------------------------------------------------ |
| `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md`           | Create a new leave allocation                    |
| `ssi_hr_holiday/docs/hr_leave_allocation/02-edit.md`             | Edit a leave allocation                          |
| `ssi_hr_holiday/docs/hr_leave_allocation/03-delete.md`           | Delete a leave allocation                        |
| `ssi_hr_holiday/docs/hr_leave_allocation/04-confirm.md`          | Confirm a leave allocation (submit for approval) |
| `ssi_hr_holiday/docs/hr_leave_allocation/05-approve.md`          | Approve a leave allocation                       |
| `ssi_hr_holiday/docs/hr_leave_allocation/06-reject.md`           | Reject a leave allocation                        |
| `ssi_hr_holiday/docs/hr_leave_allocation/09-auto-done.md`        | Automatic transition to Done when days run out   |
| `ssi_hr_holiday/docs/hr_leave_allocation/10-cancel.md`           | Cancel a leave allocation                        |
| `ssi_hr_holiday/docs/hr_leave_allocation/11-terminate.md`        | Terminate a leave allocation                     |
| `ssi_hr_holiday/docs/hr_leave_allocation/12-restart.md`          | Restart a cancelled leave allocation             |
| `ssi_hr_holiday/docs/hr_leave_allocation/13-reset-number.md`     | Reset a leave allocation's document number       |
| `ssi_hr_holiday/docs/hr_leave_allocation/14-restart-approval.md` | Restart a leave allocation's approval process    |

### `ssi_hr_holiday` — Model: `hr.leave_type`

Menu: **Human Resource > Configuration > Timesheets > Leave Type**

| File                                                 | Action                  |
| ---------------------------------------------------- | ----------------------- |
| `ssi_hr_holiday/docs/hr_leave_type/01-create.md`     | Create a new leave type |
| `ssi_hr_holiday/docs/hr_leave_type/02-edit.md`       | Edit a leave type       |
| `ssi_hr_holiday/docs/hr_leave_type/03-delete.md`     | Delete a leave type     |
| `ssi_hr_holiday/docs/hr_leave_type/04-deactivate.md` | Deactivate a leave type |
| `ssi_hr_holiday/docs/hr_leave_type/05-activate.md`   | Activate a leave type   |

### `ssi_hr_leave_allocation_request_batch` — Model: `hr.leave_allocation_request_batch`

Menu: **Human Resource > Timesheets > Leave Allocation Request Batch**

| File                                                                                                  | Action                                                                                             |
| ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/01-create.md`           | Create a new leave allocation request batch                                                        |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/02-edit.md`             | Edit a leave allocation request batch                                                              |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/03-delete.md`           | Delete a leave allocation request batch                                                            |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/04-confirm.md`          | Confirm a leave allocation request batch (submit for approval)                                     |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/05-approve.md`          | Approve a leave allocation request batch (creates & leaves the derived leave allocations in Draft) |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/06-reject.md`           | Reject a leave allocation request batch                                                            |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/10-cancel.md`           | Cancel a leave allocation request batch (deletes the derived leave allocations, if any)            |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/12-restart.md`          | Restart a cancelled leave allocation request batch                                                 |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/13-reset-number.md`     | Reset a leave allocation request batch's document number                                           |
| `ssi_hr_leave_allocation_request_batch/docs/hr_leave_allocation_request_batch/14-restart-approval.md` | Restart a leave allocation request batch's approval process                                        |

### `ssi_hr_leave_request_batch` — Model: `hr.leave_request_batch`

Menu: **Human Resource > Timesheets > Leave Request Batch**

| File                                                                            | Action                                                                    |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/01-create.md`           | Create a new leave request batch                                          |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/02-edit.md`             | Edit a leave request batch                                                |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/03-delete.md`           | Delete a leave request batch                                              |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/04-confirm.md`          | Confirm a leave request batch (creates & confirms the derived leaves)     |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/05-approve.md`          | Approve a leave request batch (approves the derived leaves too)           |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/06-reject.md`           | Reject a leave request batch (rejects the derived leaves too)             |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/10-cancel.md`           | Cancel a leave request batch (cancels the derived leaves too)             |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/12-restart.md`          | Restart a cancelled leave request batch (restarts the derived leaves too) |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/13-reset-number.md`     | Reset a leave request batch's document number                             |
| `ssi_hr_leave_request_batch/docs/hr_leave_request_batch/14-restart-approval.md` | Restart a leave request batch's approval process                          |

### `ssi_timesheet_attendance` — Model: `hr.timesheet` (extends `ssi_timesheet`)

Menu: **Human Resource > Timesheets > Timesheets**

| File                                                                | Action                                                               |
| ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `ssi_timesheet_attendance/docs/hr_timesheet/01-create.md`           | Additional field when creating a timesheet (Working Schedule)        |
| `ssi_timesheet_attendance/docs/hr_timesheet/02-edit.md`             | Additional field when editing a timesheet (Working Schedule)         |
| `ssi_timesheet_attendance/docs/hr_timesheet/07-start.md`            | Additional effect when starting a timesheet (attendance tabs unlock) |
| `ssi_timesheet_attendance/docs/hr_timesheet/15-sign-in.md`          | Sign in (record a check-in attendance)                               |
| `ssi_timesheet_attendance/docs/hr_timesheet/16-sign-out.md`         | Sign out (record a check-out attendance)                             |
| `ssi_timesheet_attendance/docs/hr_timesheet/17-compute-schedule.md` | Create Schedules (generate the attendance schedule)                  |

> Read together with `ssi_timesheet/docs/hr_timesheet/*` — these files are deltas
> (additional fields/effects) or new actions on top of the base `hr.timesheet` IK, only
> relevant when `ssi_timesheet_attendance` is installed.

### `ssi_timesheet_attendance` — Model: `hr.timesheet_attendance`

Menu: **Human Resource > Timesheets > Attendances**

| File                                                                 | Action                            |
| -------------------------------------------------------------------- | --------------------------------- |
| `ssi_timesheet_attendance/docs/hr_timesheet_attendance/01-create.md` | Create a new timesheet attendance |
| `ssi_timesheet_attendance/docs/hr_timesheet_attendance/02-edit.md`   | Edit a timesheet attendance       |
| `ssi_timesheet_attendance/docs/hr_timesheet_attendance/03-delete.md` | Delete a timesheet attendance     |

### `ssi_timesheet_attendance` — Model: `hr.attendance_reason`

Menu: **Human Resource > Configuration > Attendance > Attendance Reasons**

| File                                                                  | Action                                           |
| --------------------------------------------------------------------- | ------------------------------------------------ |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/01-create.md`     | Create a new attendance reason                   |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/02-edit.md`       | Edit an attendance reason                        |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/03-delete.md`     | Delete an attendance reason                      |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/04-deactivate.md` | Deactivate an attendance reason                  |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/05-activate.md`   | Activate an attendance reason                    |
| `ssi_timesheet_attendance/docs/hr_attendance_reason/06-reset-code.md` | Reset the code of one or more attendance reasons |

### `ssi_timesheet_attendance_shift` — Model: `hr.attendance_shift`

Menu: **Human Resource > Configurations > Attendance > Attendance Shifts**

| File                                                                       | Action                         |
| -------------------------------------------------------------------------- | ------------------------------ |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift/01-create.md`     | Create a new attendance shift  |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift/02-edit.md`       | Edit an attendance shift       |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift/03-delete.md`     | Delete an attendance shift     |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift/04-deactivate.md` | Deactivate an attendance shift |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift/05-activate.md`   | Activate an attendance shift   |

### `ssi_timesheet_attendance_shift` — Model: `hr.attendance_shift_pattern`

Menu: **Human Resource > Configurations > Attendance > Attendance Shift Patterns**

| File                                                                           | Action                                |
| ------------------------------------------------------------------------------ | ------------------------------------- |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_pattern/01-create.md` | Create a new attendance shift pattern |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_pattern/02-edit.md`   | Edit an attendance shift pattern      |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_pattern/03-delete.md` | Delete an attendance shift pattern    |

### `ssi_timesheet_attendance_shift` — Model: `hr.attendance_shift_assignment`

Menu: **Human Resource > Configurations > Attendance > Attendance Shift Assignments**

| File                                                                              | Action                                   |
| --------------------------------------------------------------------------------- | ---------------------------------------- |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_assignment/01-create.md` | Create a new attendance shift assignment |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_assignment/02-edit.md`   | Edit an attendance shift assignment      |
| `ssi_timesheet_attendance_shift/docs/hr_attendance_shift_assignment/03-delete.md` | Delete an attendance shift assignment    |

### `ssi_work_log_mixin` — Model: `hr.work_log`

Menu: **Human Resource > Timesheets > Timesheets** (open a timesheet, then use its
**Work Log** tab — see the note in `01-create.md`)

| File                                                         | Action                                   |
| ------------------------------------------------------------ | ---------------------------------------- |
| `ssi_work_log_mixin/docs/hr_work_log/01-create.md`           | Create a new work log                    |
| `ssi_work_log_mixin/docs/hr_work_log/02-edit.md`             | Edit a work log                          |
| `ssi_work_log_mixin/docs/hr_work_log/03-delete.md`           | Delete a work log                        |
| `ssi_work_log_mixin/docs/hr_work_log/04-confirm.md`          | Confirm a work log (submit for approval) |
| `ssi_work_log_mixin/docs/hr_work_log/05-approve.md`          | Approve a work log                       |
| `ssi_work_log_mixin/docs/hr_work_log/06-reject.md`           | Reject a work log                        |
| `ssi_work_log_mixin/docs/hr_work_log/10-cancel.md`           | Cancel a work log                        |
| `ssi_work_log_mixin/docs/hr_work_log/12-restart.md`          | Restart a cancelled/rejected work log    |
| `ssi_work_log_mixin/docs/hr_work_log/13-reset-number.md`     | Reset a work log's document number       |
| `ssi_work_log_mixin/docs/hr_work_log/14-restart-approval.md` | Restart a work log's approval process    |

> `hr.work_log` also has a standalone **Human Resource > Timesheets > Work Logs** menu
> (group _Work log — Viewer_) for browsing/reporting only — it cannot be used to create
> a new work log. See the note in `01-create.md`.

### `ssi_work_log_mixin` — Model: `hr.work_log_tag`

Menu: **Human Resource > Configuration > Timesheets > Work Log Tags**

| File                                                       | Action                    |
| ---------------------------------------------------------- | ------------------------- |
| `ssi_work_log_mixin/docs/hr_work_log_tag/01-create.md`     | Create a new work log tag |
| `ssi_work_log_mixin/docs/hr_work_log_tag/02-edit.md`       | Edit a work log tag       |
| `ssi_work_log_mixin/docs/hr_work_log_tag/03-delete.md`     | Delete a work log tag     |
| `ssi_work_log_mixin/docs/hr_work_log_tag/04-deactivate.md` | Deactivate a work log tag |
| `ssi_work_log_mixin/docs/hr_work_log_tag/05-activate.md`   | Activate a work log tag   |

### `ssi_work_log_mixin` — Model: `hr.timesheet` (extends `ssi_timesheet`)

Menu: **Human Resource > Timesheets > Timesheets**

| File                                                | Action                                                                              |
| --------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `ssi_work_log_mixin/docs/hr_timesheet/01-create.md` | Additional fields when creating a timesheet (Estimation, Work Log Analytic Account) |
| `ssi_work_log_mixin/docs/hr_timesheet/07-start.md`  | Additional effect when starting a timesheet (Work Log tab becomes usable)           |

> Read together with `ssi_timesheet/docs/hr_timesheet/*` — these files are deltas
> (additional fields/effects) on top of the base `hr.timesheet` IK, only relevant when
> `ssi_work_log_mixin` is installed.

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the SSI Odoo development guidelines.
