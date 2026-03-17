from odoo import models, fields

class AcademicSession(models.Model):
    _name = 'academic.session'
    _description = 'Academic Session'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    duration = fields.Float(string='Duration (Days)', digits=(6, 2))
    seats = fields.Integer(string='Number of Seats')
    
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    
    # Relasi balik ke Course
    course_id = fields.Many2one('academic.course', string='Course', required=True, ondelete='cascade')
    seats = fields.Integer(string='Number of Seats')
    
    active = fields.Boolean(string='Is Active', default=True)