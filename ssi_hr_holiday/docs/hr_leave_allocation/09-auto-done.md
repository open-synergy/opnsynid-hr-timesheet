# Auto Transition to Done — Leave Allocation

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave_allocation`
>
> **Menu:** Human Resource > Timesheets > Leave Allocations
>
> **Actor:** system (`base.automation`, no user action)
>
> **State:** `open` → `done`
>
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress**.
- **Record:** **Available Days** (`num_of_days_available`) is greater than **0** just
  before the triggering write (the automation's `filter_pre_domain`).

## Flow

This transition is **not** triggered by a user action — there is no button for it. It
runs automatically via the `base.automation` record `leave_allocation_done` whenever a
write on the allocation causes **Available Days** to become exactly **0** (the
automation's `filter_domain`). In practice this happens when the linked **Leaves**
(`leave_ids`) change in a way that recomputes **Used Days**, **Plannned Days**, or
**Available Days** — most commonly, a **Leave** that draws from this allocation reaches
status **Done** (see `ssi_hr_holiday/docs/hr_leave/04-confirm.md`, whose approval
completion sets the leave to **Done** automatically) and fully consumes the remaining
**Available Days**.

## Post-Condition

- Status changes to **Done**.
- No approval, policy, or sequence configuration is required for this transition — the
  server action it triggers (`leave_allocation_action_done`) calls `action_done()`
  directly, and the model's `done_ok` policy check is bypassed because
  `_automatically_insert_done_button` is set to `False` for this model.
