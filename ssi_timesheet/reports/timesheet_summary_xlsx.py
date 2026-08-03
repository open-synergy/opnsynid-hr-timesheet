# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, models


class TimesheetSummaryXlsx(models.AbstractModel):
    _name = "report.ssi_timesheet.timesheet_summary_xlsx"
    _description = "Timesheet Summary XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def _get_computation_items(self, timesheets):
        """Return the distinct computation items used across the timesheets.

        The columns of the report are dynamic: one column per computation
        item that actually appears on the selected timesheets, sorted by
        code then name.
        """
        items = self.env["hr.timesheet_computation_item"]
        for timesheet in timesheets:
            for computation in timesheet.computation_ids:
                items |= computation.item_id
        return items.sorted(key=lambda item: (item.code or "", item.name or ""))

    def _get_amounts_by_employee(self, timesheets):
        """Return {employee_id: {item_id: final_amount}} for the timesheets.

        ``final_amount`` (``amount`` plus any manual
        ``correction_amount``) is summed, not the raw ``amount``, so
        the report reflects corrections applied to a computation line.
        When an employee has several timesheets in the period, the
        amount of each computation item is summed across those
        timesheets.
        """
        result = {}
        for timesheet in timesheets:
            employee = timesheet.employee_id
            employee_data = result.setdefault(employee.id, {})
            for computation in timesheet.computation_ids:
                item_id = computation.item_id.id
                employee_data[item_id] = (
                    employee_data.get(item_id, 0.0) + computation.final_amount
                )
        return result

    def generate_xlsx_report(self, workbook, data, wizards):
        # Workbook formats
        fmt_title = workbook.add_format(
            {"bold": True, "font_size": 13, "align": "left"}
        )
        fmt_info = workbook.add_format({"font_size": 10})
        fmt_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#C6EFCE",
                "text_wrap": True,
                "font_size": 9,
            }
        )
        fmt_cell_center = workbook.add_format(
            {"border": 1, "align": "center", "font_size": 9, "valign": "vcenter"}
        )
        fmt_cell_left = workbook.add_format(
            {"border": 1, "align": "left", "font_size": 9, "valign": "vcenter"}
        )
        fmt_amount = workbook.add_format(
            {
                "border": 1,
                "num_format": "#,##0.00",
                "align": "right",
                "font_size": 9,
                "valign": "vcenter",
            }
        )
        fmt_total_label = workbook.add_format(
            {"bold": True, "border": 1, "font_size": 9, "bg_color": "#FFFFCC"}
        )
        fmt_total_amount = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "num_format": "#,##0.00",
                "align": "right",
                "font_size": 9,
                "bg_color": "#FFFFCC",
            }
        )

        for wizard in wizards:
            timesheets = wizard._get_timesheets()
            items = self._get_computation_items(timesheets)
            item_list = list(items)
            amounts_by_employee = self._get_amounts_by_employee(timesheets)

            # 2 fixed cols (No, Employee Name) + N computation item cols
            total_cols = 2 + len(item_list)

            sheet = workbook.add_worksheet(_("Timesheet Summary")[:31])

            # --- Column widths ---
            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 38)
            for i in range(len(item_list)):
                sheet.set_column(2 + i, 2 + i, 18)

            # --- Title & period ---
            row = 0
            sheet.merge_range(
                row, 0, row, total_cols - 1, _("TIMESHEET SUMMARY"), fmt_title
            )
            row += 1
            period_text = _("Period: %s s/d %s") % (
                wizard.date_start.strftime("%d/%m/%Y") if wizard.date_start else "",
                wizard.date_end.strftime("%d/%m/%Y") if wizard.date_end else "",
            )
            sheet.merge_range(row, 0, row, total_cols - 1, period_text, fmt_info)
            row += 2

            # --- Column headers ---
            sheet.set_row(row, 30)
            sheet.write(row, 0, _("No"), fmt_header)
            sheet.write(row, 1, _("Employee Name"), fmt_header)
            for i, item in enumerate(item_list):
                sheet.write(row, 2 + i, item.name or item.code or "", fmt_header)
            row += 1

            # --- Data rows ---
            item_totals = {item.id: 0.0 for item in item_list}
            employees = timesheets.mapped("employee_id").sorted("name")

            for seq, employee in enumerate(employees, 1):
                employee_data = amounts_by_employee.get(employee.id, {})
                sheet.write(row, 0, seq, fmt_cell_center)
                sheet.write(row, 1, employee.name or "", fmt_cell_left)
                for i, item in enumerate(item_list):
                    amount = employee_data.get(item.id, 0.0)
                    item_totals[item.id] += amount
                    sheet.write_number(row, 2 + i, amount, fmt_amount)
                row += 1

            # --- Totals row ---
            sheet.write(row, 0, "", fmt_total_label)
            sheet.write(row, 1, _("Total"), fmt_total_label)
            for i, item in enumerate(item_list):
                sheet.write_number(row, 2 + i, item_totals[item.id], fmt_total_amount)
