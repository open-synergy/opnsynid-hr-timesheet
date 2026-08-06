# Cancel Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — Validator_
>
> **State:** `draft` | `confirm` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Overtime — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the overtime.
- **Attendances** is cleared.
