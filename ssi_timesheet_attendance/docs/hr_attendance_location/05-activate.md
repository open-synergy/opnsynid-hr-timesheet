# Activate Attendance Location

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_location`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Locations
>
> **Actor:** user in group _Attendance Location_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Attendance Location_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Locations** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
