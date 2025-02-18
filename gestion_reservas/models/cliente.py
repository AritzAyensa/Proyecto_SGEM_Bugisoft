from odoo import models, fields, api

class Cliente(models.Model):
    _inherit = "res.partner"
    
    is_vip = fields.Boolean(string="Cliente VIP", default=False, help="Si el cliente es VIP, recibe un 10% de descuento en reservas.")
    reserva_ids = fields.One2many("res.booking", "cliente_id", string="Reservas")
    
    def action_save(self):
        for campo in self:
            if not campo.name or not campo.description or not campo.duracion or not campo.fecha:
                raise ValueError("Todos los campos deben ser completados.")
            campo._calcular_precio()
            campo.write({
                'name': campo.name,
                'description': campo.description,
                'duracion': campo.duracion,
                'fecha': campo.fecha,
                'estado': True,
                'precio': campo.precio,
            })
        return True
        
    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reservas',
            'res_model': 'res.booking',
            'view_mode': 'tree',
            'target': 'current',
        }
