# Restart Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
>
> **Actor:** user in group _Overtime Batch — Validator_
>
> **State:** `cancel` | `reject` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`, which grants it for
  states **Cancelled** and **Rejected**).
- **Access:** User is in group _Overtime Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- When restarting from **Cancelled**, the **Reason** recorded by `10-cancel` is cleared.
- If any `hr.overtime` documents exist for this batch (see `04-confirm`, listed in the
  **Overtime(s)** tab), each one is restarted as well, following the effect described in
  `ssi_hr_overtime/docs/hr_overtime/12-restart.md`.
