# Confirm Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** user in group _Leave Allocation Request Batch — User_
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
  single sequential level approved by group _Leave Allocation Request Batch —
  Validator_).
- **Access:** User is in group _Leave Allocation Request Batch — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for the batch, one for each approver level defined by the
  _Standard_ `approval.template` (single level, group _Leave Allocation Request Batch —
  Validator_).
- The **Leave Allocation Request** tab still stays empty — confirming the batch does
  **not** create any `hr.leave_allocation` document yet. The derived documents are only
  created once every approval level has approved and the batch reaches **Done** (see
  `05-approve`).
- Once every approval level has approved, the batch transitions to **Done**
  automatically — there is no separate Finish/Done button. The document number is also
  assigned automatically at this point (unless already manually assigned — see
  `13-reset-number`).
