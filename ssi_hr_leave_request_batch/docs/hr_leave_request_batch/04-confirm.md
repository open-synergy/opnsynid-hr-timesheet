# Confirm Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** user in group _Leave Request Batch — User_
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
  single sequential level approved by group _Leave Request Batch — Validator_).
- **Data:** See `01-create` for the per-employee prerequisites (matching timesheet, and
  leave allocation if the **Type** needs one) that the batch's employees must satisfy —
  a failure for any one of them fails confirming the whole batch.
- **Access:** User is in group _Leave Request Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- For each employee listed in **Employee(s)** that does not already have a linked
  `hr.leave` document in this batch, a new `hr.leave` document is created (**Date
  Start**/**Date End** = this batch's **Date Start**/**Date End**, **Type** = this
  batch's **Type**, **Batch** = this record) and appears in the **Leave Request** tab.
  Creating each of these documents is subject to `hr.leave`'s own creation prerequisites
  — see `ssi_hr_holiday/docs/hr_leave/01-create.md` — and fails the whole batch confirm
  if not met for any employee (e.g., no matching `hr.timesheet`, or insufficient leave
  allocation).
- Each newly created `hr.leave` document has its **Number of Days**, **Department**,
  **Manager**, and **Job Position** computed automatically — the same effect as the
  onchange triggered when creating an `hr.leave` document manually (see
  `ssi_hr_holiday/docs/hr_leave/01-create.md`).
- Every `hr.leave` document listed in the **Leave Request** tab (whether newly created
  by this confirm, or already linked from an earlier confirm on this same batch) is
  immediately confirmed as well — it transitions to **Waiting for Approval** on its own,
  with the same effects described in `ssi_hr_holiday/docs/hr_leave/04-confirm.md` (its
  own approval records created from the `hr.leave` _Standard_ `approval.template`).
- If **Employee(s)** is empty, the batch still transitions to **Waiting for Approval**,
  but no `hr.leave` documents are created.
- Approval records are created for the batch itself, for each approver level defined by
  the _Standard_ `approval.template` (single level, group _Leave Request Batch —
  Validator_).
- Once every approval level has approved (see `05-approve`), the batch transitions to
  **Done** automatically — there is no separate Finish/Done button. The document number
  is also assigned automatically at this point (unless already manually assigned — see
  `13-reset-number`).
