# Cancel Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — Validator_
>
> **State:** `draft` | `confirm` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Work log — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to cancel.
3. On the **Work Log** tab, click the line to open it.
4. Click the **Cancel** button.
5. In the wizard that appears, select the **Reason**.
6. Click **Confirm**.
7. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the work log.
