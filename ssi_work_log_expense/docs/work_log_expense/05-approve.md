# Approve Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** approver on the pending approval level
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses a single level, approved by group
  _Work Log Expense — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** automatically — there
  is no separate Done button. With the shipped _Standard_ `approval.template` (single
  level), approving always fulfills the approval and the record goes straight to
  **Done**.
- If the document number is still **/**, it is assigned automatically from the sequence
  configured by the matching `sequence.template` — this is the point where the document
  number is first issued for this model.
- An **Accounting Entry** (`account.move`) is created and posted: one debit line on the
  work log expense's **Account** for **Amount Total**, and one credit line per
  **Summary** row on that row's **Account**, each carrying its **Analytic Account** and
  **Product**. The move is shown in the **# Accounting Entry** field on the
  **Accounting** tab.
