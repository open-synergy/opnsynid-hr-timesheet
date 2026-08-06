# Terminate Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** user in group _Leave Allocation — Validator_
>
> **State:** `done` → `terminate`
>
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **Done**.
- **Config:** An active `policy.template` for this model grants `terminate_ok` for state
  `done` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Leave Allocation — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocations** menu.
2. Open the record to terminate.
3. Click the **Terminate** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Terminated**.
- The selected **Reason** is recorded on the allocation.
- There is no policy path back to **Draft** from **Terminated** for this model — the
  shipped _Standard_ `policy.template` only grants `restart_ok` for state **Cancelled**
  (see `12-restart`).

> **Note:** a daily scheduled action (`ir_cron_terminate_allocation`) attempts the same
> effect automatically, without any user action, for any **In Progress** (`open`)
> allocation whose **Date Extended** has passed. As implemented, this scheduled job
> calls the same `action_terminate()` used by the button above, which re-checks the
> `terminate_ok` policy — and the shipped _Standard_ `policy.template` only grants
> `terminate_ok` for state **Done**, not **In Progress**. This appears to make the
> scheduled job fail with a policy error for its actual target records instead of
> terminating them. This was found while writing this IK and reported to the module
> maintainers rather than fixed here, since fixing it is a code change out of scope for
> this Work Instruction.
