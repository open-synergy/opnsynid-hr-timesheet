# Approve Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
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
  level, approved by group _Leave Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** automatically — there
  is no separate Finish/Done button. With the shipped _Standard_ `approval.template`
  (single level), approving always fulfills the approval and the batch goes straight to
  **Done**.
- Every `hr.leave` document listed in the **Leave Request** tab (see `04-confirm`) is
  approved as well — each one is transitioned via its own **Approve** action, following
  the effect described in `ssi_hr_holiday/docs/hr_leave/05-approve.md` (with the
  `hr.leave` _Standard_ `approval.template` also being single level, each child leave
  goes straight to **Done** too).
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
