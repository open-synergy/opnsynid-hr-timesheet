# Create Work Log Expense

> **Module:** ssi_work_log_expense
>
> **Model:** `work_log_expense`
>
> **Menu:** Human Resource > Timesheets > Work Log Expenses
>
> **Actor:** user in group _Work Log Expense — User_
>
> **State:** `—` → `draft`
>
> **Inline Actions:** `action_populate` (Populate), `action_clear` (Clear)

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`) and `manual_number_ok` (state `draft`) to the relevant groups — see the
  _Standard_ `policy.template` shipped with this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module (single level, approved by group _Work
  Log Expense — Validator_).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** An active `work_log_expense_type` record exists, with **Account** and
  **Journal** configured on it (see `work_log_expense_type/01-create`).
- **Data:** One or more `hr.work_log` records exist for the employee, in status
  **Done**, not yet linked to another work log expense, and dated within the range to be
  entered.
- **Access:** User is in group _Work Log Expense — User_, and either is the record's
  **Responsible** (`user_id`, record rule: `user_id = user.id` — defaults to the current
  user but can be changed to another user while in Draft), or holds a broader
  data-ownership group evaluated against the record's **Employee** (_Direct
  Subordinate_, _All Subordinate_, _Company_, _Company and All Child Companies_, or
  _All_).

## Flow

1. Open the **Human Resource > Timesheets > Work Log Expenses** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Employee** _(required)_: Automatically filled from the current user's linked
     employee record, if any. Change if needed. **Manager**, **Job Position**, and
     **Department** are filled in automatically and cannot be edited directly.
   - **Type** _(required)_: Select the work log expense type. Selecting it automatically
     fills **Account** and **Journal** from the type, and clears **Analytic Account**.
   - **Analytic Account**: Optionally narrow the work logs to be populated to a single
     analytic account. Only accounts allowed by the selected **Type** can be chosen.
     Leave empty to allow any analytic account/group allowed by the **Type**.
   - **Date Start** _(required)_: The first date of the work log range to be pulled in.
   - **Date End** _(required)_: The last date of the work log range to be pulled in.
   - **Date** _(required)_: The expense document's date. Used by the _Standard_
     `sequence.template` to resolve the date-range segment of the document number.
4. On the **Details** tab, click **Populate** to pull in every `hr.work_log` record for
   the selected **Employee** that is in status **Done**, dated between **Date Start**
   and **Date End**, not yet linked to another work log expense, and matching the
   **Analytic Account**/**Type**'s allowed analytic accounts and groups. Populating also
   (re)builds the **Summary** tab and recalculates **Amount Total**. You may click
   **Populate** again after changing **Employee**, **Type**, **Analytic Account**,
   **Date Start**, or **Date End** — it first clears any existing lines before pulling
   in the new set. Click **Clear** to remove all lines (and the **Summary** tab) without
   populating new ones. Populating is required before **Confirm** (`04-confirm`)
   produces a non-zero **Amount Total**, since the accounting entry created on approval
   is generated from the **Summary** tab.
5. Click **Save**.

## Post-Condition

- A new work log expense record is created in **Draft** status.
- The document number stays **/** until the record transitions to **Done** (see
  `05-approve`), unless the actor has _Can Input Manual Document Number_ access (see
  `13-reset-number`).
