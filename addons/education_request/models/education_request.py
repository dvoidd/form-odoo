from odoo import models, fields

class EducationRequest(models.Model):
    _name = 'education.request'
    _description = 'Formulir Pengajuan Pendidikan & Pelatihan'
    _rec_name = 'document_number'

    # --- Bagian Header (Mulai dari Nomor Dokumen) ---
    document_number = fields.Char(string='Nomor Dokumen', required=True, default='Baru', copy=False)
    request_date = fields.Date(string='Tanggal Pengajuan', default=fields.Date.context_today)
    applicant_name = fields.Char(string='Nama Pemohon', required=True)
    applicant_dept = fields.Char(string='Departemen / Divisi')

    training_name = fields.Char(string='Program Pendidikan/Pelatihan', required=True)
    provider_name = fields.Char(string='Nama Penyelenggara')
    start_date = fields.Date(string='Tanggal Mulai')
    end_date = fields.Date(string='Tanggal Selesai')
    location = fields.Char(string='Tempat Pelaksanaan')

    # --- Bagian Daftar Peserta ---
    participant_ids = fields.One2many('education.request.participant', 'request_id', string='Daftar Peserta')


class EducationRequestParticipant(models.Model):
    _name = 'education.request.participant'
    _description = 'Daftar Peserta Pelatihan'

    request_id = fields.Many2one('education.request', string='ID Pengajuan', ondelete='cascade')
    
    # Kolom-kolom di dalam tabel peserta
    name = fields.Char(string='Nama Peserta', required=True)
    employee_id = fields.Char(string='NIK / ID')
    position = fields.Char(string='Jabatan')
    department = fields.Char(string='Departemen')
    notes = fields.Char(string='Keterangan')