from odoo import models, fields


class AcademicAttendee(models.Model):
    _name = 'academic.attendee'
    _description = 'Academic Attendee'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    session_ids = fields.Many2many(
        'academic.session',
        string='Sessions',
    )
