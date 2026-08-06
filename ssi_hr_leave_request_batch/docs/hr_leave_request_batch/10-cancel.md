# Cancel Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** user in group _Leave Request Batch — Validator_
>
> **State:** `draft` | `confirm` | `done` | `reject` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **Done**, or **Rejected**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the batch.
- If any `hr.leave` documents were already created for this batch (see `04-confirm`,
  listed in the **Leave Request** tab), each one is cancelled as well, following the
  effect described in `ssi_hr_holiday/docs/hr_leave/10-cancel.md`. Cancelling straight
  from **Draft** has no such effect, since the **Leave Request** tab is still empty at
  that point.
