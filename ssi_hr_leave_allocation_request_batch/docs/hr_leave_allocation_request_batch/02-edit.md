# Edit Leave Allocation Request Batch

> **Module:** ssi_hr_leave_allocation_request_batch
>
> **Model:** `hr.leave_allocation_request_batch`
>
> **Menu:** Human Resource > Timesheets > Leave Allocation Request Batch
>
> **Actor:** user in group _Leave Allocation Request Batch — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Leave Allocation Request Batch — User_, and is the
  record's **Responsible** (record rule), or holds a broader data-ownership group
  (_Company_, _Company and All Child Companies_, or _All_).

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Find and open the record to edit.
3. Change **Type**, **Number Of Days**, **Employee(s)**, **Date Start**, **Date End**,
   **Can be Extended**, or **Date Extended** as needed — the same constraints described
   in `01-create` apply.
4. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- The **Leave Allocation Request** tab remains unaffected by this edit — it is only
  populated once the batch's approval completes and it reaches **Done** (see
  `05-approve`).
