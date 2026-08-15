# Reset Document Number — Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** user in group _Work Log Expense — Validator_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `manual_number_ok` for
  state `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `sequence.template` exists for this model (see the _Standard_
  `sequence.template`).
- **Access:** User is in group _Work Log Expense — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field in the title
   area and change it to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done** (see
  `05-approve`), according to the _Standard_ `sequence.template` configuration.
