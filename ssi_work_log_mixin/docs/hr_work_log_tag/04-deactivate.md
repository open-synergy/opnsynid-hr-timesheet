# Deactivate Work Log Tag

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log_tag`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Tags
>
> **Actor:** user in group _Work Log Tags_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Work Log Tags_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Tags** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated tags cannot be selected as a **Tag** on a new work log (see
  `docs/hr_work_log/01-create.md`).
