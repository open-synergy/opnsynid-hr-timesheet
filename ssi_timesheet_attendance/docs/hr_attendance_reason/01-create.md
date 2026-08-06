# Create Attendance Reason

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Reasons
>
> **Actor:** user in group _Attendance Reason_
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Reasons** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Reason** _(required)_: Enter a short label describing the reason (for example
     "Business Trip").
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it eligible for
     automatic assignment via **Generate Code**.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model. Only applies while **Code** is still
   **/**. If no matching `sequence.template` is configured, nothing changes and **Code**
   must be filled in manually.
5. Optionally fill in **Note**.
6. Click **Save**.

## Post-Condition

- A new attendance reason record is created, active by default.
- The record becomes selectable as **Reason In** / **Reason Out** on a timesheet
  attendance record (see `ssi_timesheet_attendance/hr_timesheet_attendance/01-create`).
