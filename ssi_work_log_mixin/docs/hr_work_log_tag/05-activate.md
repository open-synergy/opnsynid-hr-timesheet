# Activate Work Log Tag

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log_tag`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Tags
>
> **Actor:** user in group _Work Log Tags_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Work Log Tags_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Tags** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The tags can be selected again as a **Tag** on a new work log.
