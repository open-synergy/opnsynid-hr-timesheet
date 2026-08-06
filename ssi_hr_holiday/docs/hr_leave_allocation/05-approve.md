# Approve Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `open`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses sequential approval with a single
  level, approved by group _Leave Allocation — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **In Progress** automatically
  — there is no separate Open/Start button. With the shipped _Standard_
  `approval.template` (single level), approving always fulfills the approval and the
  document goes straight to **In Progress**.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
