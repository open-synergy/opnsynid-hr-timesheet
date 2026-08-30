# Edit Attendance Location

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_location`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Locations
>
> **Actor:** user in group _Attendance Location_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Location_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Locations** menu.
2. Find and open the record to edit.
3. Change **Location**, **Code**, **Latitude**, **Longitude**, **Radius (meter)**,
   **Active**, or **Note** as needed.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/** (see `06-reset-code`). Only applies while **Code** is **/**;
   if no matching `sequence.template` is configured, nothing changes and **Code** must
   be filled in manually.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
- Latitude and longitude that are both exactly 0, or outside their valid range, are
  rejected with an error and the change is not saved.
- A radius that is zero or negative is rejected with an error and the change is not
  saved.
