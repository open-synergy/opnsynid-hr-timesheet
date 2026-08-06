# Approve Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
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
  **pending**. The _Standard_ `approval.template` uses sequential approval with a single
  level, approved by group _Leave — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** automatically — there
  is no separate Finish/Done button. With the shipped _Standard_ `approval.template`
  (single level), approving always fulfills the approval and the document goes straight
  to **Done**.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- Once **Done**, the linked **# Leave Allocation** (if any) has its **Used Days** and
  **Available Days** recomputed, which may trigger that allocation's automatic
  transition to **Done** (see
  `ssi_hr_holiday/docs/hr_leave_allocation/09-auto-done.md`).
