# Create Work Log Expense Type

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Expense Types
>
> **Actor:** user in group _Work Log Expense Type_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label for the type (for example
     "Transportation").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
   - **Account** _(required)_: The accrual account credited when a work log expense of
     this type is populated. Also used as the default **Account** on new work log
     expense records of this type.
   - **Journal** _(required)_: The accounting journal used for the accounting entry
     created when a work log expense of this type is approved.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**. If no matching `sequence.template` is configured, nothing changes and **Code**
   must be filled in manually.
5. On the **Allowed Analytics** tab, fill in **Allowed Analytic Groups** and/or
   **Allowed Analytic Accounts** to restrict which analytic accounts a work log expense
   of this type may populate work logs from. Leave both empty to allow any analytic
   account.
6. Optionally fill in **Note**.
7. Click **Save**.

## Post-Condition

- A new work log expense type record is created, active by default.
- The record becomes selectable as **Type** on a work log expense (see
  `ssi_work_log_expense/work_log_expense/01-create`).
