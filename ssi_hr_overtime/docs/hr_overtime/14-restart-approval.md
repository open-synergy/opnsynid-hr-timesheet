# Restart Approval Process — Overtime

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime`
>
> **Menu:** Human Resource > Timesheets > Overtimes
>
> **Actor:** user in group _Overtime — Validator_
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `restart_approval_ok`
  for state `confirm` to the actor's group (see the _Standard_ `policy.template`). As
  shipped, this policy only evaluates to allowed while the record's **Approval
  Template** field is still empty — since Confirm (`04-confirm`) already assigns an
  approval template before the record reaches this state, the button is typically not
  clickable in practice with the default configuration. See the note below.
- **Access:** User is in group _Overtime — Validator_.

## Flow

1. Open the **Human Resource > Timesheets > Overtimes** menu.
2. Open the record to restart the approval process for.
3. Click the **Restart Approval Process** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- All existing approval records for this document are removed.
- New approval records are created from the record's current **Approval Template**,
  restarting the approval process from the first level.
- Status remains **Waiting for Approval**.

> **Note:** the shipped _Standard_ `policy.template` grants `restart_approval_ok` only
> when `approval_template_id` is **not yet** set. Because the `Confirm` action
> (`04-confirm`) always assigns `approval_template_id` before the record reaches state
> `confirm`, this policy is effectively never satisfied under the default configuration.
> This was found while writing this IK and reported to the module maintainers rather
> than fixed here, since fixing it is a code change out of scope for this Work
> Instruction.
