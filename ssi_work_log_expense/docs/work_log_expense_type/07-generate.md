# Generate Work Log Expense

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

- **Record:** The **Work Log Expense Type** record to generate from exists, with
  **Account** and **Journal** configured on it.
- **Data:** One or more `hr.work_log` records exist, in status **Done**, not yet linked
  to another work log expense, dated within the range to be entered, and matching the
  type's **Allowed Analytic Groups**/**Allowed Analytic Accounts** (or the **Analytic
  Account** entered in the wizard, if any).
- **Access:** User is in group _Work Log Expense Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Work Log Expense Types**
   menu.
2. Open the type record to generate work log expenses from.
3. Click the **Generate** button in the header.
4. In the wizard that appears, fill in the fields:
   - **Analytic Account**: Optionally narrow the work logs to be pulled in to a single
     analytic account. Leave empty to use the type's **Allowed Analytic Groups**/
     **Allowed Analytic Accounts**.
   - **Date Start** _(required)_: The first date of the work log range to be pulled in.
   - **Date End** _(required)_: The last date of the work log range to be pulled in.
   - **Date** _(required)_: The date to set on every generated work log expense.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog ("Are you sure?").

## Post-Condition

- One new **Work Log Expense** record is created in **Draft** status for each distinct
  **Employee** who has at least one matching `hr.work_log` record, with **Type**,
  **Account**, and **Journal** copied from this type, and **Date Start**/**Date End**/
  **Date** copied from the wizard.
- Each generated record is already populated: its **Details** tab is filled with the
  matching work logs (equivalent to running **Populate**, see
  `ssi_work_log_expense/work_log_expense/01-create`), and **Amount Total** is
  recalculated accordingly.
- If no employee has a matching `hr.work_log` record, nothing is created and no message
  is shown.
- The document number of each generated record stays **/** until it transitions to
  **Done** (see `ssi_work_log_expense/work_log_expense/05-approve`).
