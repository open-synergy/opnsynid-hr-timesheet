# Cancel Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** user in group _Leave Allocation — Validator_
>
> **State:** `draft` | `confirm` | `open` | `done` | `reject` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, **Done**,
  or **Rejected**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave Allocation — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the allocation.
- If any **Leaves** referencing this allocation are not already **Cancelled** or
  **Rejected**, cancellation fails — cancel or reject those leaves first.
