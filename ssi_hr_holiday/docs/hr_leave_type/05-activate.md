# Activate Leave Type

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Leave Type
>
> **Actor:** user in group _Leave Type_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Leave Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Leave Type** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again on new **Leave** or **Leave Allocation** records.
