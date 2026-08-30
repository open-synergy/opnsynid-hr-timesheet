# Create Attendance Location

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_location`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Locations
>
> **Actor:** user in group _Attendance Location_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Location_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Locations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Location** _(required)_: Enter a short name identifying the place (for example
     "Kantor Pusat").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
   - **Latitude** _(required)_: Enter the latitude of the location's center point, in
     decimal degrees, between -90 and 90.
   - **Longitude** _(required)_: Enter the longitude of the location's center point, in
     decimal degrees, between -180 and 180.
   - **Radius (meter)** _(required)_: Enter the tolerance radius around the center
     point, in **meters**. Defaults to **100**.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**. If no matching `sequence.template` is configured, nothing changes and **Code**
   must be filled in manually.
5. Optionally fill in **Note**.
6. Click **Save**.

## Post-Condition

- A new attendance location record is created, active by default.
- Latitude and longitude that are both exactly 0, or outside their valid range, are
  rejected with an error and the record is not saved.
- A radius that is zero or negative is rejected with an error and the record is not
  saved.
