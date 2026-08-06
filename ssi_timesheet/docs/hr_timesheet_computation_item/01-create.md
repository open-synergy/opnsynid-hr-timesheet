# Create Timesheet Computation Item

> **Module:** ssi_timesheet
>
> **Model:** `hr.timesheet_computation_item`
>
> **Menu:** Human Resource > Configuration > Timesheets > Timesheet Computation Items
>
> **Actor:** user in group _Timesheet Computation Item_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Timesheet Computation Item_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Timesheet Computation
   Items** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label for the computation item (for example
     "Overtime Allowance").
   - **Code** _(required)_: Enter a unique code, or leave the default **/** to assign
     one automatically.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**. If no matching `sequence.template` is configured, the field stays **/** and
   **Code** must be filled in manually before saving with a non-**/** value.
5. On the **Computation** tab, edit the **Python Code** field. It starts pre-filled with
   a comment template describing the available variables (`env`, `document`, `result`).
   Replace it with the logic that evaluates whether this item applies, assigning a
   boolean to `result`.
6. Click **Save**.

## Post-Condition

- A new timesheet computation item record is created.
