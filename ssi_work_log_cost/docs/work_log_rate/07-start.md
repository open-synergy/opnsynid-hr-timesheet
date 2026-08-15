# Start Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** user in group _Work Log Rate — User_
>
> **State:** `ready` → `open`
>
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Ready to Start**.
- **Config:** An active `policy.template` for this model grants `open_ok` for state
  `ready` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Work Log Rate — User_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Open the record to start.
3. Click the **Start** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **In Progress**.
