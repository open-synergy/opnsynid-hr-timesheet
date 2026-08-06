# Cancel Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
>
> **Actor:** user in group _Leave — Validator_
>
> **State:** `draft` | `confirm` | `done` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Done**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the leave.
- The code attempts to also reopen a linked **# Leave Allocation** that is in status
  **Done** back to **In Progress** as part of this step. See the note below.

> **Note:** as implemented, this reopen attempt calls the allocation's `action_open()`
> directly, without bypassing the `open_ok` policy check. The shipped `policy.template`
> named "Standard" never grants `open_ok` on `hr.leave_allocation` (see the note on
> `ssi_hr_holiday/docs/hr_leave_allocation/04-confirm.md`), so this appears to make
> cancelling a **Done** leave whose allocation is also **Done** fail with a policy error
> instead of completing the cancellation. This was found while writing this IK and
> reported to the module maintainers rather than fixed here, since fixing it is a code
> change out of scope for this Work Instruction.
