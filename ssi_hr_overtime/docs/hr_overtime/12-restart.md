# Restart Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — Validator_
>
> **State:** `cancel` | `reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it for
  states **Cancelled** and **Rejected**).
- **Access:** User is in group _Overtime — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- When restarting from **Cancelled**, the **Reason** recorded by `10-cancel` is cleared.
