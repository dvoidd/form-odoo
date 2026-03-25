from odoo import api, fields, models


class CreateAttendeeWizard(models.TransientModel):
    _name = 'academic.create_attendee.wizard'
    _description = 'Wizard to Add Attendees to Sessions'

    session_id = fields.Many2one(
        'academic.session',
        string='Session',
        required=True,
    )
    attendee_ids = fields.Many2many(
        'academic.attendee',
        string='Attendees',
        required=True,
    )

    def action_add_attendees(self):
        self.ensure_one()
        self.session_id.attendee_ids |= self.attendee_ids
        return {'type': 'ir.actions.act_window_close'}


class AttendeeWizard(models.TransientModel):
    _name = 'academic.attendee.wizard'
    _description = 'Wizard to Add Attendees to Multiple Sessions'

    session_ids = fields.Many2many(
        'academic.session',
        string='Sessions',
        required=True,
    )
    attendee_ids = fields.Many2many(
        'academic.attendee',
        string='Attendees',
        required=True,
    )

    def action_add_attendees(self):
        self.ensure_one()
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {'type': 'ir.actions.act_window_close'}
