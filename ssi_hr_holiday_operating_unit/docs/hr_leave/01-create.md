# Create Leave

> **Module:** ssi_hr_holiday_operating_unit
>
> **Extends:** ssi_hr_holiday — model `hr.leave`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: The operating unit this leave belongs to. Defaults to the current
  user's default operating unit. Only visible to users in the _Multi Operating Unit_
  group (`operating_unit.group_multi_operating_unit`); hidden for single-operating-unit
  installations. The same field is also added (hidden by default) as an optional column
  in the **Leaves** list, and as a **Group By: Operating Unit** filter in the search
  view — both gated by the same group.

## Modified — Record Visibility

- A user granted the _Operating Unit_ data-ownership group for this model only sees
  leaves whose **Operating Unit** is one of the operating units assigned to them (record
  rule). This is not a Flow step.
