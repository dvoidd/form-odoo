from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string='Is Instructor', default=False)
    session_ids = fields.One2many(
        'academic.session',
        'instructor_id',
        string='Sessions',
    )
