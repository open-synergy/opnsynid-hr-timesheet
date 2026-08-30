# Reset Code — Attendance Location

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_location`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Locations
>
> **Actor:** user in group _Attendance Location_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** One or more records exist.
- **Access:** User is in group _Attendance Location_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Locations** menu.
2. Select one or more records whose code will be reset (check the checkbox).
3. Click the **Reset code** button that appears above the list.
4. Click **OK** on the confirmation dialog ("Reset code. Are you sure?").

## Post-Condition

- **Code** of the selected records returns to **/**.
- The records become eligible for automatic code assignment the next time **Generate
  Code** is used (see `01-create` and `02-edit`), or the field can be filled in
  manually.
