# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrMachineTransactionWizard(models.TransientModel):
    _name = "hr.attendance.machine.import.wizard"
    _description = "Import File Transaction Machine CSV"
    _rec_name = "datas_fname"

    datas = fields.Binary('File', required=True)
    datas_fname = fields.Char('Filename', readonly=True)

    def action_import(self):
        pass
