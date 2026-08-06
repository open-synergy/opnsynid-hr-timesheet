# Reject Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
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
  level, approved by group _Overtime Batch — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
- Every `hr.overtime` document created for this batch (see `04-confirm`, listed in the
  **Overtime(s)** tab) is rejected as well — each one is transitioned via its own
  **Reject** action, following the effect described in
  `ssi_hr_overtime/docs/hr_overtime/06-reject.md`.
