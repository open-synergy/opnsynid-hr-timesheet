# Confirm Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — User_
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
  single sequential level approved by group _Overtime — Validator_).
- **Access:** User is in group _Overtime — User_.

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- The **Attendances** tab is populated: every `hr.timesheet_attendance` record for the
  same **Employee** and **Date** is linked to this overtime, and those attendance
  records' own **Overtimes** field is recomputed to reference this record in turn (same
  underlying relation, so it also updates automatically whenever a matching attendance's
  **Check In**/**Check Out** changes — see `ssi_timesheet_attendance` documentation).
- **Realized Hours** is recomputed from the newly linked **Attendances**: for each
  linked attendance, the overlap between **Date Start**/**Date End** and that
  attendance's **Check In**/**Check Out** is added up.
- Approval records are created for each approver level defined by the _Standard_
  `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically — there is no separate Finish/Done button, and no dedicated IK
  for this transition. The document number is also assigned automatically at this point
  (unless already manually assigned — see `13-reset-number`).
