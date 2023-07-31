# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinWorkObject(models.AbstractModel):
    _name = "mixin.work_object"
    _description = "Work Object Mixin"

    _work_log_create_page = False
    _work_log_page_xpath = "//page[last()]"

    work_estimation = fields.Float(
        string="Work Estimation",
    )

    work_log_ids = fields.One2many(
        string="Work Logs",
        comodel_name="hr.work_log",
        inverse_name="work_object_id",
        domain=lambda self: [("model_name", "=", self._name)],
        auto_join=True,
        readonly=False,
    )

    @api.depends(
        "work_estimation",
        "work_log_ids",
        "work_log_ids.amount",
    )
    def _compute_work_realization(self):
        for record in self:
            total_work = remaining_work = excess_work = 0.0
            for work in record.work_log_ids:
                total_work += work.amount

            remaining_work = record.work_estimation - total_work
            if remaining_work < 0.0:
                excess_work = remaining_work
                remaining_work = 0.0
            record.total_work = total_work
            record.remaining_work = remaining_work
            record.excess_work = excess_work

    total_work = fields.Float(
        string="Total Work",
        compute="_compute_work_realization",
        store=True,
    )
    remaining_work = fields.Float(
        string="Remaining Work",
        compute="_compute_work_realization",
        store=True,
    )
    excess_work = fields.Float(
        string="Excess Work",
        compute="_compute_work_realization",
        store=True,
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._work_log_create_page:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._work_log_page_xpath)
            if node_xpath:
                str_element = self.env["ir.qweb"]._render(
                    "ssi_work_log_mixin.work_log_page"
                )
                for node in node_xpath:
                    new_node = etree.fromstring(str_element)
                    node.addnext(new_node)

            View = self.env["ir.ui.view"]

            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res

    @api.depends(
        "work_log_ids",
        "work_log_ids.analytic_account_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        for document in self:
            document.allowed_analytic_account_ids = []

    allowed_analytic_account_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        compute="_compute_allowed_analytic_account_ids",
    )

    def unlink(self):
        work_log_ids = self.mapped("work_log_ids")
        for work_log in work_log_ids:
            if work_log.sheet_id.state in ["confirm", "done"]:
                strWarning = _(
                    "You cannot delete the work log!\n"
                    "Timesheet with number %s is already on '%s' state!"
                ) % (work_log.sheet_id.name, work_log.sheet_id.state)
                raise UserError(strWarning)
        work_log_ids.unlink()
        return super(MixinWorkObject, self).unlink()
