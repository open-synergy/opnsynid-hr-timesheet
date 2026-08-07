# Edit Work Log

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
  (record rule), or holds a broader data-ownership group (_Direct Subordinate_, _All
  Subordinate_, _Company_, _Company and All Child Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the timesheet that owns the work log to edit.
3. On the **Work Log** tab, click the line to edit.
4. Change **Description**, **Date**, **Analytic Account**, **Duration**, or **Tags** as
   needed.
5. Click **Save & Close**.
6. Click **Save** on the timesheet form.

## Post-Condition

- The record is updated with the new values.
