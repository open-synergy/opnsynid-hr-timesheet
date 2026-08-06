# Reject Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `reject`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `reject_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  pending. The _Standard_ `approval.template` uses sequential approval with a single
  level, approved by group _Leave Request Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- Every `hr.leave` document listed in the **Leave Request** tab (see `04-confirm`) is
  rejected as well — each one is transitioned via its own **Reject** action, following
  the effect described in `ssi_hr_holiday/docs/hr_leave/06-reject.md`.
