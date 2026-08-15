# Restart Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** user in group _Work Log Rate — Validator_
>
> **State:** `cancel` | `reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it for
  states **Cancelled** and **Rejected**).
- **Access:** User is in group _Work Log Rate — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  (`04-confirm`) starts the approval process from the beginning.
