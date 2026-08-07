# Restart Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — Validator_
>
> **State:** `cancel` | `reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it for
  states **Cancelled** and **Rejected**).
- **Access:** User is in group _Work log — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to restart.
3. On the **Work Log** tab, click the line to open it.
4. Click the **Restart** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- When restarting from **Cancelled**, the **Reason** recorded by `10-cancel` is cleared.
