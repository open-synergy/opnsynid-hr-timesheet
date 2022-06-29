# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinWorkObject(models.AbstractModel):
    _name = "mixin.work_object"
    _description = "Work Object Mixin"

    _work_log_create_page = False
    _work_log_page_xpath = "//page[last()]"

    work_log_ids = fields.One2many(
        string="Work Logs",
        comodel_name="hr.work_log",
        inverse_name="work_object_id",
        domain=lambda self: [("model_name", "=", self._name)],
        auto_join=True,
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
            if work_log.sheet_id.state == "done":
                strWarning = _(
                    "You cannot delete the work log. Timesheet %s is already 'Done'"
                ) % (work_log.sheet_id.name)
                raise UserError(strWarning)
        work_log_ids.unlink()
        return super(MixinWorkObject, self).unlink()
