# Delete Leave Allocation Request Batch

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
- **Record:** Document number is still **/** (not yet generated).
- **Access:** User is in group _Leave Allocation Request Batch — User_, and is the
  record's **Responsible** (record rule), or holds a broader data-ownership group.

## Flow

1. Open the **Human Resource > Timesheets > Leave Allocation Request Batch** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
