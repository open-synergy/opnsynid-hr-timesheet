# Create Schedules — Timesheet

> **Module:** `ssi_timesheet_attendance`
>
> **Model:** `hr.timesheet`
>
> **Menu:** Human Resource > Timesheets > Timesheets
>
> **Actor:** user in group _Timesheets — User_
>
> **Requires:** `ssi_timesheet/hr_timesheet/01-create`
>
> **Extends:** ssi_timesheet — model `hr.timesheet`

## Pre-Condition

- **Record:** Status is **Draft** or **On Progress**. Create Schedules is refused on any
  other status (**Confirmed**, **Done**, ...), even if the button is called by other
  means. **Date Start** and **Date End** must be filled, together with what the
  **Schedule Source** needs: **Working Schedule** for the Working Schedule source,
  **Schedule Pattern** for the Pattern source.
- **Record:** No other document refers to the existing **Attendance Schedules** lines.
  Modules that link documents to a schedule slot (for example leave or attendance
  revision) add themselves to this check; when one of them still refers to a slot,
  Create Schedules is refused.
- **Config:** **Check In Buffer** and **Check Out Buffer** are set on the company
  (Settings, Human Resources section, Attendance block; 3.0 hours by default). They
  decide which attendance is matched to which schedule slot.
- **Access:** User is in group _Timesheets — User_.

## Flow

1. Open the **Human Resource > Timesheets > Timesheets** menu.
2. Open the record (status **Draft** or **On Progress**).
3. On the **Attendance Schedules** tab, click **Create Schedules**
   (`action_compute_schedule`).
4. Click **OK** on the confirmation dialog ("Compute Schedules. Are you sure?").

## Post-Condition

- Existing `hr.timesheet_attendance_schedule` lines for this timesheet are removed and
  regenerated, excluding public holidays, from the **Schedule Source**:
  - **Working Schedule**: the attendance intervals of **Working Schedule** between
    **Date Start** and **Date End**.
  - **Pattern**: one slot for each working day that **Schedule Pattern** resolves
    between **Date Start** and **Date End**. A special date overrides the recurring
    rules; otherwise an **Off** line removes the day, and the first **Work** line that
    covers the day gives the slot. A national public holiday wins over a special date.
    Each slot records the pattern and the pattern line it came from (the line stays
    empty for a special date).
  - The hours are read in the employee's timezone, so the result does not depend on the
    timezone of the user who clicks the button.
- Each attendance record already recorded on the **Attendance** tab is matched again to
  the schedule slot whose window holds its **Check In**. The window of a slot starts
  **Check In Buffer** hours before the slot starts and ends **Check Out Buffer** hours
  after the slot ends; only **Check In** is tested, **Check Out** may fall anywhere.
  When more than one slot holds the check-in, the slot that starts closest to it is
  used. An attendance whose check-in is outside every window is left without a schedule:
  its hours are still counted in **Total Hour**, but its **Total Valid Hour** is 0.0.
- Each schedule slot's real attendance/deviation figures (Real Date Start/End, Early
  Start, Late Start, Finish Early, Finish Late) are recalculated from those attendance
  records.
- The **Daily Summary** of the timesheet is regenerated, so **Total Valid Attendance**
  follows the new matching.
- If the status is not **Draft** or **On Progress**, or another document still refers to
  a schedule slot, an error message names the problem (and the blocking documents) and
  nothing is deleted.
- This step can be repeated at any time while the record is **Draft** or **On
  Progress**; running it again discards and regenerates all **Attendance Schedules**
  lines.
