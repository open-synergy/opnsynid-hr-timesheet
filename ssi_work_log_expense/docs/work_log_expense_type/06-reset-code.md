# Reset Code — Work Log Expense Type

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

- **Record:** One or more records exist.
- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Select one or more records whose code will be reset (check the checkbox).
3. Click the **Reset code** button that appears above the list.
4. Click **OK** on the confirmation dialog ("Reset code. Are you sure?").

## Post-Condition

- **Code** of the selected records returns to **/**.
- The records become eligible for automatic code assignment the next time **Generate
  Code** is used (see `01-create` and `02-edit`), or the field can be filled in
  manually.
