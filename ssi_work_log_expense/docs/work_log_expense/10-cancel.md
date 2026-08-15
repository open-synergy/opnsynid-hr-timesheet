# Cancel Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** user in group _Work Log Expense — Validator_
>
> **State:** `draft` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **Done**. The _Standard_ `policy.template` does
  **not** grant `cancel_ok` for status **Waiting for Approval** — a record must be
  rejected or approved first before it can be cancelled from that point onward.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Work Log Expense — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the work log expense.
- If the record was **Done**, its **Accounting Entry** (see `05-approve`) is cancelled
  and removed; the **# Accounting Entry** field on the **Accounting** tab is cleared.
