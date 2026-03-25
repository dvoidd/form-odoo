from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


class AcademicSession(models.Model):
    _name = 'academic.session'
    _description = 'Academic Session'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    duration = fields.Float(string='Duration (Days)', digits=(6, 2))
    seats = fields.Integer(string='Number of Seats')
    active = fields.Boolean(string='Is Active', default=True)
    color = fields.Integer(string='Color Index')

    # Relasi
    instructor_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        domain=[('is_instructor', '=', True)],
    )
    course_id = fields.Many2one(
        'academic.course',
        string='Course',
        required=True,
        ondelete='cascade',
    )
    attendee_ids = fields.Many2many(
        'academic.attendee',
        string='Attendees',
    )

    # Related Field (Section 14)
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible',
        related='course_id.responsible_id',
        store=True,
        readonly=True,
    )

    # Workflow Status (Section 16)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True)

    # Compute Fields (Section 9)
    taken_seats = fields.Float(
        string='Taken Seats (%)',
        compute='_compute_taken_seats',
        store=True,
    )
    end_date = fields.Date(
        string='End Date',
        compute='_compute_end_date',
        inverse='_inverse_end_date',
        store=True,
    )
    attendees_count = fields.Integer(
        string='Attendees Count',
        compute='_compute_attendees_count',
        store=True,
    )

    # SQL Constraints (Section 10)
    _sql_constraints = [
        ('name_course_unique',
         'UNIQUE(name, course_id)',
         'Session name must be unique per course!'),
    ]

    # Compute Methods
    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.end_date = record.start_date
            else:
                duration = timedelta(days=record.duration - 1) if record.duration > 0 else timedelta(days=0)
                record.end_date = record.start_date + duration

    def _inverse_end_date(self):
        for record in self:
            if not (record.start_date and record.end_date):
                continue
            record.duration = (record.end_date - record.start_date).days + 1

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    # Python Constraints (Section 10)
    @api.constrains('seats')
    def _check_seats(self):
        for record in self:
            if record.seats < 0:
                raise ValidationError("The number of seats cannot be negative!")

    # Onchange (Section 19)
    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': 'Incorrect seats value',
                    'message': 'The number of seats cannot be negative!',
                },
            }
        if self.seats and self.taken_seats > 100:
            return {
                'warning': {
                    'title': 'Too many attendees',
                    'message': 'You have more attendees than seats!',
                },
            }

    # Workflow Actions (Section 16)
    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_done(self):
        for record in self:
            record.state = 'done'

    # Duplicate Record (Section 12)
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': '%s (copy)' % self.name,
            'attendee_ids': [],
        })
        return super().copy(default)