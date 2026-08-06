# Delete Timesheet Attendance

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.timesheet_attendance`
>
> **Menu:** Human Resource > Timesheets > Attendances
>
> **Actor:** user in group _Timesheet Attendance_
>
> **Requires:** `01-create`

## Pre-Condition

- **Access:** User is in group _Timesheet Attendance_.

## Flow

1. Open the **Human Resource > Timesheets > Attendances** menu.
2. Select one or more records to delete (check the checkbox).
3. Click **Action** > **Delete**.
4. Click **OK** to confirm.

## Post-Condition

- The selected records are permanently removed from the system.
- Records are also removed automatically, without this flow, when their parent timesheet
  is deleted.
