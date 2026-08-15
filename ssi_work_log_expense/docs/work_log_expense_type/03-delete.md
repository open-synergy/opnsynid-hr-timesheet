# Delete Work Log Expense Type

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Expense Types
>
> **Actor:** user in group _Work Log Expense Type_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system. Deletion fails with a
  database integrity error if the type is already referenced by an existing **Work Log
  Expense** record (`type_id` uses `ondelete="restrict"`) — deactivate the record
  instead (see `04-deactivate`).
