# Create Overtime Type

> **Module:** ssi_hr_overtime
>
> **Model:** `hr.overtime_type`
>
> **Menu:** Human Resource > Configuration > Timesheets > Overtime Types
>
> **Actor:** user in group _Overtime Type_

## Pre-Condition

- **Access:** User is in group _Overtime Type_.

## Flow

1. Open the **Human Resource > Configuration > Timesheets > Overtime Types** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Type** _(required)_: Enter a short label for the overtime type (for example
     "Weekday Overtime").
   - **Apply Limit Per Days**: Enable to cap the total planned hours employees can
     request under this type on a single day.
   - **Limit Per Days**: When **Apply Limit Per Days** is enabled, enter the maximum
     total **Planned Hours** allowed per employee per day for overtimes of this type
     (see `ssi_hr_overtime/docs/hr_overtime/01-create.md`).
4. Click **Save**.

## Post-Condition

- A new overtime type record is created.
