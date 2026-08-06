# Delete Leave

> **Module:** ssi_hr_holiday
>
> **Model:** `hr.leave`
>
> **Menu:** Human Resource > Timesheets > Leaves
>
> **Actor:** user in group _Leave — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Leave — User_, and is the record's **Responsible** or
  **Employee** (record rule), or holds a broader data-ownership group.

## Flow

1. Open the **Human Resource > Timesheets > Leaves** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
