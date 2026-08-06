# Cancel Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
>
> **Actor:** user in group _Overtime Batch — Validator_
>
> **State:** `draft` | `confirm` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Overtime Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the batch.
- If any `hr.overtime` documents were already created for this batch (see `04-confirm`,
  listed in the **Overtime(s)** tab), each one is cancelled as well, following the
  effect described in `ssi_hr_overtime/docs/hr_overtime/10-cancel.md` (its own
  **Attendances** cleared). Cancelling straight from **Draft** has no such effect, since
  the **Overtime(s)** tab is still empty at that point.
