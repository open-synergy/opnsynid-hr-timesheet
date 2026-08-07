# Cancel Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** user in group _Leave Allocation Request Batch — Validator_
>
> **State:** `draft` | `confirm` | `done` | `reject` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **Done**, or **Rejected**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave Allocation Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the batch.
- If any `hr.leave_allocation` documents were already created for this batch (see
  `05-approve`, listed in the **Leave Allocation Request** tab), each one is **deleted**
  (not cancelled) as part of cancelling the batch. Cancelling from **Draft**, **Waiting
  for Approval**, or **Rejected** has no such effect, since the **Leave Allocation
  Request** tab is still empty at that point (documents are only created once the batch
  reaches **Done** — see `05-approve`).

> **Note:** deleting each linked `hr.leave_allocation` document only succeeds while that
> document is still in its own **Draft** status with document number **/** (its state
> right after being created by `05-approve`, since this batch does not advance it any
> further — see the note there). If a linked `hr.leave_allocation` document was manually
> confirmed, approved, or otherwise advanced after being created, cancelling this batch
> fails instead of deleting it, and the batch stays in its state from before this Cancel
> attempt.
