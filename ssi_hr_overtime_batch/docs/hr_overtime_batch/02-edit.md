# Edit Overtime Batch

> **Module:** ssi_hr_overtime_batch
>
> **Model:** `hr.overtime_batch`
>
> **Menu:** Human Resource > Timesheets > Overtime Batch
>
> **Actor:** user in group _Overtime Batch — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Overtime Batch — User_, and is the record's
  **Responsible** (record rule), or holds a broader data-ownership group (_Company_,
  _Company and All Child Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Overtime Batch** menu.
2. Find and open the record to edit.
3. Change **Overtime Type**, **Employee(s)**, **Date Start**, or **Date End** as needed
   — the same constraints described in `01-create` apply.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- The **Overtime(s)** tab remains unaffected by this edit — it is only populated when
  the batch is confirmed (see `04-confirm`).
