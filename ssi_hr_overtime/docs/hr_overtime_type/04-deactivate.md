# Deactivate Overtime Type

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Overtime Types
>
> **Actor:** user in group _Overtime Type_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Overtime Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Overtime Types** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as the **Overtime Type** on a new overtime (see
  `ssi_hr_overtime/docs/hr_overtime/01-create.md`).
