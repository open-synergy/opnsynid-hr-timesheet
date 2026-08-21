# Create Overtime

> **Module:** ssi_hr_overtime_state_change_constrain
>
> **Extends:** ssi_hr_overtime — model `hr.overtime`, aksi `01-create`

## Modified Flow

- Anchor: on the base Flow, after the form is opened for a new record, the form now also
  shows a **Status Checks** tab. It lists the check items pulled from the **Status Check
  Template** that matches this record (selected automatically when the record is created
  — see Additional Post-Condition).

## Additional Post-Condition

- **Status Check Template** is automatically filled with the first matching
  `status.check.template` configured for `hr.overtime`, if any, and the **Status
  Checks** tab is populated with that template's items. **State Change Constrain
  Template** is then automatically filled with the matching
  `state.change.constrain.template` linked to that **Status Check Template**, if any.
  Which template applies (or whether none does) is configuration-driven, not fixed by
  this module.
