# Edit Work Log Expense Type

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Work Log Expense Types
>
> **Actor:** user in group _Work Log Expense Type_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Find and open the record to edit.
3. Change **Name**, **Code**, **Active**, **Account**, **Journal**, or **Note** as
   needed.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/** (see `06-reset-code`). Only applies while **Code** is **/**;
   if no matching `sequence.template` is configured, nothing changes and **Code** must
   be filled in manually.
5. On the **Allowed Analytics** tab, add, change, or remove **Allowed Analytic Groups**
   and **Allowed Analytic Accounts** as needed.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values. Existing work log expenses that already
  reference this type keep their own **Account**/**Journal**/**Analytic Account** values
  — this change only affects the defaults applied to new records going forward.
