# Deactivate Attendance Location

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_location`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Locations
>
> **Actor:** user in group _Attendance Location_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Location_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Locations** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
