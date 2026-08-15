# Confirm Leave

> **Module:** ssi_holiday_state_change_constrain
>
> **Extends:** ssi_hr_holiday — model `hr.leave`, aksi `04-confirm`

## Modified Validation

- Confirm (and every other state transition) fails with a validation error **when** a
  **State Change Constrain Template** applies to this record (see `01-create`) and
  defines check items for the target state, **and** one or more of those items on the
  **Status Checks** tab are not yet ticked. Which template applies, and which items it
  requires per state, is configuration-driven, not fixed by this module.
