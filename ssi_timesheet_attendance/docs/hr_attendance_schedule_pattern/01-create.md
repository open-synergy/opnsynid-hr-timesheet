# Create Attendance Schedule Pattern

> **Module:** `ssi_timesheet_attendance`
>
> **Model:** `hr.attendance_schedule_pattern`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Schedule Patterns
>
> **Actor:** user in group _Attendance Schedule Pattern_

## Pre-Condition

- **Access:** User is in group _Attendance Schedule Pattern_.
- **Record:** At least one Frequency exists that repeats every **1** interval, for
  example every week on Saturday or every month on the second Saturday. Frequencies are
  created in the same group's reach, from the **Frequency** field of a pattern line.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Schedule
   Patterns** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter a short label for the pattern (for example "Weekdays
     and Second Saturday").
   - **Code** _(required)_: Enter a unique code, or fill in "/" to assign one
     automatically.
4. Open the **Pattern Lines** tab. For each recurring rule, add a line:
   - **Frequency** _(required)_: Select the recurrence rule that picks the days. It must
     repeat every 1 interval.
   - **Effect** _(required)_: Select **Work** for a working slot, or **Off** for days
     that are removed. Defaults to **Work**.
   - **Hour From** and **Hour To** _(required for Work)_: Enter the start and the end of
     the slot, inside one calendar day (0:00 to 24:00).
   - **Valid From** and **Valid Until**: Optionally limit the days the line applies to.
5. Optionally open the **Special Dates** tab and add a line for each exception:
   - **Date** _(required)_: Enter the calendar date. A date can be used only once in a
     pattern.
   - **Effect** _(required)_: Select **Work** to add a slot on that date, or **Off** to
     remove it.
   - **Hour From** and **Hour To** _(required for Work)_: Enter the slot hours.
6. Click **Save**.

## Post-Condition

- A new attendance schedule pattern record is created together with its lines and
  special dates.
- A line whose frequency does not repeat every 1 interval, or a Work slot that is not
  inside one calendar day, is rejected with an error and the record is not saved.
- A date used twice in the same pattern is rejected with an error and the record is not
  saved.
- The pattern can be selected as **Schedule Pattern** on an employee, on the company
  default, and on a timesheet whose **Schedule Source** is **Pattern**.
