# Create Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch_operating_unit
>
> **Extends:** ssi_hr_leave_allocation_request_batch — model
> `hr.leave_allocation_request_batch`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one field:

- **Operating Unit**: The operating unit this leave allocation request batch belongs to.
  Defaults to the current user's default operating unit. Only visible to users in the
  _Multi Operating Unit_ group (`operating_unit.group_multi_operating_unit`); hidden for
  single-operating-unit installations. The same field is also added (hidden by default)
  as an optional column in the **Leave Allocation Request Batch** list, and as a **Group
  By: Operating Unit** filter in the search view — both gated by the same group.

## Modified — Record Visibility

- A user granted the _Operating Unit_ data-ownership group for this model only sees
  leave allocation request batches whose **Operating Unit** is one of the operating
  units assigned to them (record rule). This is not a Flow step.
