# Confirm Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (see the _Standard_ `approval.template`, which defines a
  single level approved by group _Work log — Validator_).
- **Access:** User is in group _Work log — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to confirm.
3. On the **Work Log** tab, click the line to open it.
4. Click the **Confirm** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the _Standard_
  `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically — there is no separate Finish/Done button, and no dedicated IK
  for this transition.
