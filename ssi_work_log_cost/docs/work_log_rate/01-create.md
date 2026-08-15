# Create Work Log Rate

> **Module:** ssi_work_log_cost
>
> **Model:** `work_log_rate`
>
> **Menu:** Human Resource > Timesheets > Work Log Rates
>
> **Actor:** user in group _Work Log Rate — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`) and `manual_number_ok` (state `draft`) to the relevant groups — see the
  _Standard_ `policy.template` shipped with this module.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template` shipped with this module (single level, approved by group _Work
  Log Rate — Validator_).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module.
- **Data:** At least one `product.product` and `product.pricelist` exist to be used as
  general rate lines.
- **Access:** User is in group _Work Log Rate — User_, and either the **Employee** to
  select is themselves (record rule: `employee_id = user.employee_id`), or the user
  holds a broader data-ownership group (_Direct Subordinate_, _All Subordinate_,
  _Company_, _Company and All Child Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Work Log Rates** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Employee** _(required)_: Select the employee this rate applies to.
   - **Date** _(required)_: The rate document's date. Used by the _Standard_
     `sequence.template` to resolve the date-range segment of the document number.
   - **Date Start** _(required)_: The first date this rate is valid for the employee.
   - **Date End**: The last date this rate is valid for the employee. Leave empty for a
     rate that stays valid indefinitely (no end date).
4. On the **General Rates** tab, click **Add a line**. Repeat the following steps as
   many times as needed:
   - **Product** _(required)_: Select the product this general rate line applies to.
   - **Pricelist** _(required)_: Select the pricelist that determines the unit price for
     this product.
5. Click **Save**.

## Post-Condition

- A new work log rate record is created in **Draft** status.
- The document number stays **/** until the record transitions to **Ready to Start**
  (see `05-approve`), unless the actor has _Can Input Manual Document Number_ access
  (see `13-reset-number`).
