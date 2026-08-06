# Activate Overtime Type

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Overtime Types
>
> **Actor:** user in group _Overtime Type_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Overtime Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Overtime Types** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as the **Overtime Type** on a new overtime.
