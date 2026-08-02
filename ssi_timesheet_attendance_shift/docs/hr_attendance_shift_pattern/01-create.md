# Create Attendance Shift Pattern

> **Module:** ssi_timesheet_attendance_shift
>
> **Model:** `hr.attendance_shift_pattern`
>
> **Menu:** Human Resource > Configurations > Attendance > Attendance Shift Patterns
>
> **Actor:** user in group _Attendance Shift_

## Pre-Condition

- **Access:** User is in group _Attendance Shift_.
- **Record:** At least one Attendance Shift exists, if a cycle day should point at a
  shift instead of being a day off.

## Flow

1. Open the **Human Resource > Configurations > Attendance > Attendance Shift Patterns**
   menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label for the pattern (for example "Three Crew
     Rotation").
   - **Code** _(required)_: Enter a unique code, or fill in "/" to assign one
     automatically.
   - **Cycle Length (Days)** _(required)_: Enter the number of days in one full
     rotation. Defaults to 7.
   - **Cycle Anchor Date** _(required)_: Enter the global reference date day-in-cycle 1
     is resolved from.
4. Open the **Cycle Days** tab.
5. For each day-in-cycle from 1 up to **Cycle Length (Days)**, add a line:
   - **Day Index** _(required)_: Enter the position of this day within the cycle,
     between 1 and **Cycle Length (Days)**.
   - **Shift**: Select the shift that applies on that day-in-cycle. Leave empty for a
     day off.
6. Click **Save**.

## Post-Condition

- A new attendance shift pattern record is created together with its cycle day lines.
- A cycle day line with **Shift** left empty represents a day off.
