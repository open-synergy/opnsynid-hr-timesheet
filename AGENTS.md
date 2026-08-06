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

---

## Module Development Guidelines

For code conventions, file structure, naming, security, views, and other SSI standard
patterns, follow the SSI Odoo development guidelines.
