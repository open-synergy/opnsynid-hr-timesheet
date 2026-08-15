# Edit Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** user in group _Work Log Expense — User_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_populate` (Populate), `action_clear` (Clear)

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Work Log Expense — User_, and either is the record's
  **Responsible** (`user_id`, record rule: `user_id = user.id`), or holds a broader
  data-ownership group evaluated against the record's **Employee** (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Type**, **Analytic Account**, **Date Start**, **Date End**, or
   **Date** as needed — the same constraints described in `01-create` apply.
4. On the **Details** tab, click **Populate** to refresh the lines after changing
   **Employee**, **Type**, **Analytic Account**, **Date Start**, or **Date End** — it
   first clears any existing lines (and the **Summary** tab), then pulls in the work
   logs matching the current field values, exactly as described in `01-create`. Click
   **Clear** to remove all lines without populating new ones.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
