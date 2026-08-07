# Delete Work Log

> **Module:** ssi_work_log_mixin
>
> **Model:** `hr.work_log`
>
> **Menu:** Human Resource > Timesheets > Timesheets (open a timesheet, then use its
> **Work Log** tab)
>
> **Actor:** user in group _Work log — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Work log — User_, and is the record's **Employee**
  (record rule), or holds a broader data-ownership group.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to delete.
3. On the **Work Log** tab, select the line to delete and click the row's delete
   (trash) icon.
4. Click **Save** on the timesheet form.

## Post-Condition

- The work log record is permanently removed from the system.
- The timesheet's **Total Work Log** is recalculated automatically.
