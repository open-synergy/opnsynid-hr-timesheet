# Confirm Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
>
> **Actor:** user in group _Leave — User_
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
  single sequential level approved by group _Leave — Validator_).
- **Data:** If **Leave Type** has **Need Allocation** checked, an available **# Leave
  Allocation** with enough **Available Days** must be linked (see `01-create`) —
  otherwise this step fails with a validation error.
- **Access:** User is in group _Leave — User_.

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- **# Timesheet**, **Duration**, and **# Leave Allocation** are recomputed automatically
  (same effect as described in `01-create`).
- Approval records are created for each approver level defined by the _Standard_
  `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically — there is no separate Finish/Done button, and no dedicated IK
  for this transition. The document number is also assigned automatically at this point
  (unless already manually assigned — see `13-reset-number`).
- If the leave was linked to a **# Leave Allocation**, that allocation's **Used Days**
  and **Available Days** are recomputed, and may reach **0**, triggering the
  allocation's automatic transition to **Done** (see
  `ssi_hr_holiday/docs/hr_leave_allocation/09-auto-done.md`).
