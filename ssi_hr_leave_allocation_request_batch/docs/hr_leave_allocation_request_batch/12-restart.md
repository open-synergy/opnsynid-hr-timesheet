# Restart Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** user in group _Leave Allocation Request Batch — Validator_
>
> **State:** `cancel` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it only
  for status **Cancelled**).
- **Access:** User is in group _Leave Allocation Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- The **Reason** recorded by `10-cancel` is cleared.
- All approval records for the batch are removed and the **Approval Template** is
  cleared. A later Confirm (`04-confirm`) starts the approval process from the
  beginning.
- The **Leave Allocation Request** tab stays empty — any `hr.leave_allocation` documents
  that existed for this batch were already removed when it was cancelled (see
  `10-cancel`).

> **Note:** the shipped _Standard_ `policy.template` grants `restart_ok` only for status
> **Cancelled** — not **Rejected**. A record in status **Rejected** has no button to
> return directly to **Draft**; it must first be cancelled (see `10-cancel`, which
> allows cancelling from status **Rejected**) before **Restart** becomes available.
