# Create Work Log

> **Module:** ssi_work_log_cost
>
> **Extends:** ssi_work_log_mixin — model `hr.work_log`, aksi `01-create`

## Additional Pre-Condition

- **Config:** An active `policy.template` for this model grants `show_cost_setting_ok`
  for state `draft` to the actor's group (see the _Standard_ `policy.template` shipped
  with this module) — the **Cost** tab described below is hidden otherwise. As shipped,
  this is granted to group _Work log — User_.
- **Data:** The allowed **Product** and **Pricelist** choices are restricted to those
  configured on the timesheet's **Document Type** (the `ir.model` record for
  `hr.timesheet`) — either a fixed list or a Python-evaluated list. This configuration
  is set up by a developer/administrator and is out of scope for this Work Instruction.

## Additional Fields

When this module is installed and the actor has `show_cost_setting_ok` access, a
**Cost** tab appears on the work log form with the following fields:

- **Usage**: Automatically filled from the **Document Type**'s **Default Worklog
  Usage**, if configured (triggered when **Document Type** changes). Change if needed —
  choices are limited to the usages allowed for the selected **Product**.
- **Account**: Automatically filled from the selected **Product** and **Usage** (using
  the product's accounting configuration for that usage). Change if needed. Optional —
  this module makes the field not required.
- **Quantity**: Defaults to the work log's own **Duration** (`amount`); recalculated
  automatically if **Duration** changes. Not directly editable on this tab.
- **UoM** _(required if **Product** is selected)_: Select the unit of measure for
  **Quantity**. Choices are limited to units in the selected **Product**'s UoM category.
- **Currency**: Defaults to the company's currency.
- **Pricelist**: Automatically filled with the first pricelist allowed for the selected
  **Currency** (and, once a **Product** is selected, further restricted to pricelists
  allowed by the **Document Type**). Change if needed.
- **Product**: Automatically filled with the first product allowed by the **Document
  Type**, once one becomes available. Change if needed — choices are limited to the
  products allowed by the **Document Type**.
- **Price Unit**: Automatically filled from **Product**, **Pricelist**, **Quantity**,
  and **UoM** (via the pricelist's price computation). Change if needed.
- **Tax(es)**: Automatically filled from the selected **Product** and **Usage** (using
  the product's tax configuration for that usage). Change if needed.

## Additional Post-Condition

- **Price Subtotal**, **Tax**, and **Price Total** are computed automatically from
  **Price Unit**, **Quantity**, and **Tax(es)** — there is nothing to fill in for these.
