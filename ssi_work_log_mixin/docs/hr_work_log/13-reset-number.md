# Reset Document Number — Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — Validator_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `manual_number_ok` for
  state `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `sequence.template` exists for this model (see the _Standard_
  `sequence.template`).
- **Access:** User is in group _Work log — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log.
3. On the **Work Log** tab, click the line to open it.
4. Click the **Reset Document Number** button (or edit the number field in the title
   area and change it to **/**).
5. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **Done** (see
  `05-approve`), according to the _Standard_ `sequence.template` configuration.
