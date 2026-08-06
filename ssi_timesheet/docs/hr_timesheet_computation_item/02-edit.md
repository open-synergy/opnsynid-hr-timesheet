# Edit Timesheet Computation Item

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet_computation_item`
>
> **Menu:** Human Resource > Configuration > Timesheets > Timesheet Computation Items
>
> **Actor:** user in group _Timesheet Computation Item_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Timesheet Computation Item_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Timesheet Computation
   Items** menu.
2. Find and open the record to edit.
3. Change the **Name**, **Code**, or the **Python Code** on the **Computation** tab as
   needed.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/**. Only applies while **Code** is **/**; if no matching
   `sequence.template` is configured, nothing changes and **Code** must be filled in
   manually.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
