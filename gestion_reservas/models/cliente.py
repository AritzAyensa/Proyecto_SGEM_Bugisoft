from odoo import models, fields

class Cliente(models.Model):  # Cambio de Models a Model
    _inherit = "res.partner"
    
    is_vip = fields.Boolean(string="Cliente VIP", default=False, help="Si el cliente es VIP, recibe un 10% de descuento en reservas.")
    reserva_ids = fields.One2many("res.booking", "cliente_id")
    
def action_save(self): 
        # Lógica para guardar la reserva
        for campo in self:
            # Asegúrate de que todos los campos sean válidos (por ejemplo, no vacíos)
            if not campo.name or not campo.description or not campo.duracion or not campo.fecha:
                raise ValueError("Todos los campos deben ser completados.")

            campo._calcular_precio()

            campo.write({
                'name': campo.name,
                'description': campo.description,
                'duracion': campo.duracion,
                'fecha': campo.fecha,
                'estado': True,
                'precio': campo.precio
            })

        # Si todo salió bien, devolver algo
        return True
        
def action_cancel():
    return {
        'type': 'ir.actions.act_window',
        'name': 'Reservas',
        'res_model': 'res.booking',
        'view_mode': 'tree',
        'target': 'current',
    }
