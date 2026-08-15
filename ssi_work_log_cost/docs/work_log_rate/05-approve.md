# Approve Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `ready`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses a single level, approved by group
  _Work Log Rate — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Ready to Start**
  automatically — there is no separate Set Ready button. With the shipped _Standard_
  `approval.template` (single level), approving always fulfills the approval and the
  record goes straight to **Ready to Start**.
- If the document number is still **/**, it is assigned automatically from the sequence
  configured by the matching `sequence.template`.
