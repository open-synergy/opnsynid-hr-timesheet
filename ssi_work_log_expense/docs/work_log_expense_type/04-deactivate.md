# Deactivate Work Log Expense Type

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Expense Types
>
> **Actor:** user in group _Work Log Expense Type_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated records cannot be selected as **Type** on new **Work Log Expense**
  records.
- **Work Log Expense** records that already reference this type can still be viewed.
