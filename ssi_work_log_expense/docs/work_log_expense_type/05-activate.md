# Activate Work Log Expense Type

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Expense Types
>
> **Actor:** user in group _Work Log Expense Type_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as **Type** on new **Work Log Expense** records.
