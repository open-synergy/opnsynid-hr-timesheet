# Restart Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** user in group _Leave Allocation — Validator_
>
> **State:** `cancel` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for state
  `cancel` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave Allocation — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- The **Reason** recorded by `10-cancel` is cleared.

> **Note:** the shipped _Standard_ `policy.template` grants `restart_ok` **only** for
> state **Cancelled** — there is no policy path back to **Draft** from **Rejected**
> (`06-reject`) or **Terminated** (`11-terminate`) for this model, even though the
> **Restart** button itself is rendered for any state (visibility is controlled entirely
> by `restart_ok`).
