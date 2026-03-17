from odoo import models, fields, api

class TrainingProposal(models.Model):
    _name = 'training.proposal'
    _description = 'Proposal Pengajuan Training'
    _rec_name = 'proposal_number'

    proposal_number = fields.Char(string='Nomor', required=True, copy=False, default='Baru')
    description = fields.Char(string='Deskripsi', required=True, default='Training of Trainer')
    submitted_by = fields.Char(string='Diajukan Oleh', required=True)
    department = fields.Char(string='Departemen / Divisi')

    introduction = fields.Text(string='Pendahuluan')
    background = fields.Text(string='Latar Belakang Masalah')
    objective = fields.Text(string='Tujuan')
    solution = fields.Text(string='Solusi')

    cost_line_ids = fields.One2many('training.proposal.line', 'proposal_id', string='Permintaan Biaya')
    participant_ids = fields.One2many('training.proposal.participant', 'proposal_id', string='Daftar Peserta')
    total_cost = fields.Float(string='Total Biaya', compute='_compute_total_cost', store=True)
    amount_in_words = fields.Char(string='Terbilang')

    payment_schedule = fields.Date(string='Jadwal Pembayaran')
    execution_schedule = fields.Char(string='Jadwal Pelaksanaan')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Disetujui'),
        ('rejected', 'Tidak Disetujui')
    ], string='Status Persetujuan', default='draft', tracking=True)
    general_notes = fields.Text(string='Catatan Umum')

    @api.depends('cost_line_ids.price_subtotal')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.cost_line_ids.mapped('price_subtotal'))

    def action_approve(self): self.state = 'approved'
    def action_reject(self): self.state = 'rejected'
    def action_draft(self): self.state = 'draft'


class TrainingProposalLine(models.Model):
    _name = 'training.proposal.line'
    _description = 'Rincian Permintaan Biaya'

    proposal_id = fields.Many2one('training.proposal', string='Proposal', ondelete='cascade')
    name = fields.Char(string='Uraian', required=True)
    qty = fields.Float(string='Qty', default=1.0)
    price_unit = fields.Float(string='Harga Satuan')
    price_subtotal = fields.Float(string='Total Harga', compute='_compute_price_subtotal', store=True)
    notes = fields.Char(string='Keterangan')

    @api.depends('qty', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.qty * line.price_unit

class TrainingProposalParticipant(models.Model):
    _name = 'training.proposal.participant'
    _description = 'Daftar Peserta Pelatihan untuk Proposal'

    proposal_id = fields.Many2one('training.proposal', string='ID Proposal', ondelete='cascade')
    
    # Kolom-kolom di dalam tabel peserta
    name = fields.Char(string='Nama Peserta', required=True)
    employee_id = fields.Char(string='NIK / ID')
    position = fields.Char(string='Jabatan')
    department = fields.Char(string='Departemen')
    notes = fields.Char(string='Keterangan')