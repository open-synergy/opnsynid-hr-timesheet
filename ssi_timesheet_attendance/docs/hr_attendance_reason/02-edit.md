# Edit Attendance Reason

> **Module:** ssi_timesheet_attendance
>
> **Model:** `hr.attendance_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Reasons
>
> **Actor:** user in group _Attendance Reason_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Access:** User is in group _Attendance Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Reasons** menu.
2. Find and open the record to edit.
3. Change **Reason**, **Code**, **Active**, or **Note** as needed.
4. In the header, click **Generate Code** to assign a code from the sequence configured
   by an active `sequence.template` for this model — for example after resetting
   **Code** back to **/** (see `06-reset-code`). Only applies while **Code** is **/**;
   if no matching `sequence.template` is configured, nothing changes and **Code** must
   be filled in manually.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
