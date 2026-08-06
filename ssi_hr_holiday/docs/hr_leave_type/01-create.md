# Create Leave Type

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Leave Type
>
> **Actor:** user in group _Leave Type_

## Pre-Condition

- **Access:** User is in group _Leave Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Leave Type** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Leave Type** _(required)_: Enter a short label for the leave type (for example
     "Annual Leave" or "Sick Leave").
   - **Need Allocation**: Check if a leave request of this type must be covered by an
     available leave allocation (see
     `ssi_hr_holiday/docs/hr_leave_allocation/01-create.md`) before it can be confirmed.
     Leave unchecked if this type does not require an allocation.
   - **Apply Limit Per Request**: Check to cap the number of days that can be requested
     in a single leave request of this type.
   - **Limit Per Request**: Enter the maximum number of days allowed per request. Only
     enforced when **Apply Limit Per Request** is checked.
   - **Exclude Public Holiday**: A configuration toggle stored on the leave type. See
     the note below.
   - **Exclude Rest Day**: A configuration toggle stored on the leave type. See the note
     below.
4. Click **Save**.

## Post-Condition

- A new leave type record is created and available for selection on **Leaves** and
  **Leave Allocations**.

> **Note:** as implemented in this module, **Exclude Public Holiday** and **Exclude Rest
> Day** are stored but not read by `hr.leave`'s duration computation
> (`_compute_leave_duration`) — public holidays are always excluded from **Duration**
> regardless of this flag, and rest days are excluded only as a side effect of
> **Schedules** already containing working days only, not because of this flag. This was
> found while writing this IK and reported to the module maintainers rather than fixed
> here, since fixing it is a code change out of scope for this Work Instruction.
