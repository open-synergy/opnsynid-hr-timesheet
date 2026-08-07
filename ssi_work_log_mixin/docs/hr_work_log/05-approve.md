# Approve Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses a single level, approved by group
  _Work log — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to approve.
3. On the **Work Log** tab, click the line to open it.
4. Click the **Approve** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** automatically — there
  is no separate Finish/Done button. With the shipped _Standard_ `approval.template`
  (single level), approving always fulfills the approval and the document goes straight
  to **Done**.
- If the document number is still **/**, it is assigned automatically from the sequence
  configured by the matching `sequence.template`.
