# Restart Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** user in group _Leave Request Batch — Validator_
>
> **State:** `cancel` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it only
  for status **Cancelled**).
- **Access:** User is in group _Leave Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- The **Reason** recorded by `10-cancel` is cleared.
- All approval records for the batch are removed and the **Approval Template** is
  cleared. A later Confirm (`04-confirm`) starts the approval process from the
  beginning.
- If any `hr.leave` documents exist for this batch (see `04-confirm`, listed in the
  **Leave Request** tab), each one is restarted as well, following the effect described
  in `ssi_hr_holiday/docs/hr_leave/12-restart.md`.

> **Note:** the shipped _Standard_ `policy.template` grants `restart_ok` only for status
> **Cancelled** — not **Rejected**. Unlike some other modules in this repository, a
> record in status **Rejected** has no button to return directly to **Draft**; it must
> first be cancelled (see `10-cancel`, which allows cancelling from status **Rejected**)
> before **Restart** becomes available.
