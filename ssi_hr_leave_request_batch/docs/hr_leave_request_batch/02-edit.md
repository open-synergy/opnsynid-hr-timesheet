# Edit Leave Request Batch

> **Module:** ssi_hr_leave_request_batch
>
> **Model:** `hr.leave_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Request Batch
>
> **Actor:** user in group _Leave Request Batch — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Leave Request Batch — User_, and is the record's
  **Responsible** (record rule), or holds a broader data-ownership group (_Company_,
  _Company and All Child Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Leave Request Batch** menu.
2. Find and open the record to edit.
3. Change **Type**, **Employee(s)**, **Date Start**, or **Date End** as needed — the
   same constraints described in `01-create` apply.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- The **Leave Request** tab remains unaffected by this edit — it is only populated when
  the batch is confirmed (see `04-confirm`).
