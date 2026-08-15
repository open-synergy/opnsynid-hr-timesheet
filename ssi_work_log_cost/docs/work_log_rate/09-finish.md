# Finish Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** user in group _Work Log Rate — User_
>
> **State:** `open` → `done`
>
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Work Log Rate — User_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
