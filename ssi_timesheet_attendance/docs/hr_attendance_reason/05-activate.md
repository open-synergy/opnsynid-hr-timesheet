# Activate Attendance Reason

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Reasons
>
> **Actor:** user in group _Attendance Reason_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Attendance Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Reasons** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The records can be selected again as **Reason In** / **Reason Out** on new timesheet
  attendance records.
