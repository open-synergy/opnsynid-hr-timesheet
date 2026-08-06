# Confirm Timesheet

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **State:** `open` → `confirm`
>
> **Requires:** `07-start`

## Pre-Condition

- **Record:** Status is **On Progress**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `open` to the actor's group (see the _Standard Timesheet_ `policy.template`).
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (see the _Standard - Timesheet_ `approval.template`, which
  defines a single sequential level approved by group _Timesheets — Validator_).
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- The **Computations** tab is reloaded and recomputed automatically (same effect as the
  **Reload** and **Compute** buttons described in `01-create`).
- Approval records are created for each approver level defined by the _Standard -
  Timesheet_ `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically — there is no separate Finish/Done button, and no dedicated IK
  for this transition.
