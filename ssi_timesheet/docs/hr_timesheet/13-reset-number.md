# Reset Document Number — Timesheet

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — Validator_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `manual_number_ok` for
  state `draft` to the actor's group (see the _Standard Timesheet_ `policy.template`).
- **Config:** An active `sequence.template` exists for this model (see the _Standard
  Timesheet_ `sequence.template`).
- **Access:** User is in group _Timesheets — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button (or edit the number field in the title
   area and change it to **/**).
4. Click **OK** on the confirmation dialog (only when the button was used).

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **On Progress**
  (see `07-start`), according to the _Standard Timesheet_ `sequence.template`
  configuration.
