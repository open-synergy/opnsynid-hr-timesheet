# Approve Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Data:** For every employee listed in **Employee(s)** that does not already have a
  linked `hr.leave_allocation` document in this batch, the employee must not already
  have another active `hr.leave_allocation` (status other than
  **Cancelled**/**Rejected**) whose date range overlaps this batch's **Date
  Start**/**Date End** — see `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md`. If
  this condition is not met for even one employee, approving fails for the whole batch
  (see Post-Condition below).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses sequential approval with a single
  level, approved by group _Leave Allocation Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending; the rest of this section does not apply yet.
- If all approval levels are fulfilled, status changes to **Done** automatically — there
  is no separate Finish/Done button. With the shipped _Standard_ `approval.template`
  (single level), approving always fulfills the approval and the batch goes straight to
  **Done**. Reaching **Done** triggers the derived-document creation described below.
- For each employee listed in **Employee(s)** that does not already have a linked
  `hr.leave_allocation` document in this batch (**Leave Allocation Request** tab), a new
  `hr.leave_allocation` document is created (**Date Start**/**Date End** = this batch's
  **Date Start**/**Date End**, **Type** = this batch's **Type**, **Number of Days** =
  this batch's **Number Of Days**, **Can be Extended**/**Date Extended** = this batch's
  own values, **Batch** = this record) and appears in the **Leave Allocation Request**
  tab. Its **Department**, **Manager**, and **Job Position** are computed automatically
  — the same effect as the onchange triggered when creating an `hr.leave_allocation`
  document manually (see `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md`).
- Unlike the batch itself, each newly created `hr.leave_allocation` document is **not**
  automatically confirmed or approved — it is left in its own **Draft** status.
  Advancing it through its own workflow (see
  `ssi_hr_holiday/docs/hr_leave_allocation/04-confirm.md` onward) is a separate, manual
  step outside this batch.
- If any employee in **Employee(s)** already has another active `hr.leave_allocation`
  overlapping this batch's date range (see Pre-Condition), approving raises an error and
  the whole action fails — the batch does not reach **Done** and no
  `hr.leave_allocation` document is created for any employee in this approval attempt.

> **Note:** **Employee(s)** is a required field on this model (see `01-create`), so a
> batch can never reach this step with an empty employee list.
