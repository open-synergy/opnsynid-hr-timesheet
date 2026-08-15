# Delete Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** user in group _Work Log Expense — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Work Log Expense — User_, and either is the record's
  **Responsible** (`user_id`, record rule: `user_id = user.id`), or holds a broader
  data-ownership group evaluated against the record's **Employee** (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- Any `hr.work_log` records that were populated onto a deleted record automatically have
  their `# Expense` link cleared (`ondelete="set null"`), becoming available for
  population onto another work log expense again. The `work_log_expense_summary` lines
  on the deleted record are removed together with it (`ondelete="cascade"`).
