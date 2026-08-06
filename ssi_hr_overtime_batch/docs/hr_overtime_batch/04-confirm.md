# Confirm Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
>
> **Actor:** user in group _Overtime Batch — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (see the _Standard_ `approval.template`, which defines a
  single sequential level approved by group _Overtime Batch — Validator_).
- **Data:** See `01-create` for the per-employee prerequisites (matching timesheet, no
  overlapping overtime) that the batch's employees must satisfy — a failure for any one
  of them fails confirming the whole batch.
- **Access:** User is in group _Overtime Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- For each employee listed in **Employee(s)**, a new `hr.overtime` document is created
  (**Date** = the date of this batch's **Date Start**, **Date Start**/**Date End** =
  this batch's **Date Start**/**Date End**, **Overtime Type** = this batch's **Overtime
  Type**, **Batch** = this record) and appears in the **Overtime(s)** tab. Creating each
  of these documents is subject to `hr.overtime`'s own creation prerequisites — see
  `ssi_hr_overtime/docs/hr_overtime/01-create.md` — and fails the whole batch confirm if
  not met for any employee (e.g., no matching `hr.timesheet`, or an overlapping overtime
  already exists for that employee/date range).
- Each newly created `hr.overtime` document is immediately confirmed as well — it
  transitions to **Waiting for Approval** on its own, with the same effects described in
  `ssi_hr_overtime/docs/hr_overtime/04-confirm.md` (its **Attendances** tab populated,
  **Realized Hours** recomputed, and its own approval records created from the
  `hr.overtime` _Standard_ `approval.template`).
- If **Employee(s)** is empty, the batch still transitions to **Waiting for Approval**,
  but no `hr.overtime` documents are created.
- Approval records are created for the batch itself, for each approver level defined by
  the _Standard_ `approval.template` (single level, group _Overtime Batch — Validator_).
- Once every approval level has approved (see `05-approve`), the batch transitions to
  **Done** automatically — there is no separate Finish/Done button. The document number
  is also assigned automatically at this point (unless already manually assigned — see
  `13-reset-number`).
