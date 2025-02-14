from odoo import models, fields

class Cliente(models.Model):  # Cambio de Models a Model
    _inherit = "res.partner"
    
    is_vip = fields.Boolean(string="Cliente VIP", default=False, help="Si el cliente es VIP, recibe un 10% de descuento en reservas.")
    reserva_ids = fields.One2many("res.booking", "cliente_id")
