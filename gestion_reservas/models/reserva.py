from odoo import models, fields, api

class Reserva(models.Model):
    _name = "res.booking"
    _description = "Reserva"

    # Campos
    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción', required=True)
    duracion = fields.Integer(string='Duración (días)', required=True)
    fecha = fields.Datetime(string='Fecha y Hora de Inicio', required=True)
    estado = fields.Selection([  # Cambio de Text a Selection
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado de la reserva', default='pendiente', required=True)
    precio = fields.Float(string='Precio', compute='_calcular_precio', store=True)

    # Relación con coche y cliente
    coche_id = fields.Many2one('res.coche', string="Coche", required=True)
    cliente_id = fields.Many2one('res.partner', string="Cliente", required=True)

    # Relación con la factura
    factura_id = fields.Many2one('account.move', string='Factura')

    @api.depends('coche_id.precio_por_dia', 'cliente_id.is_vip')
    def _calcular_precio(self):
        for record in self:
            precio_por_dia = record.coche_id.precio_por_dia if record.coche_id else 0.0
            descuento = 0.1 if record.cliente_id and record.cliente_id.is_vip else 0.0
            record.precio = (precio_por_dia * record.duracion) * (1 - descuento)

    def action_confirmar_reserva(self):
        for record in self:
            if not record.factura_id:
                # Crear valores de la factura
                factura_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': record.cliente_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'name': 'Reserva de coche',
                        'quantity': 1,
                        'price_unit': record.precio,
                    })],
                }

                # Crear la factura
                factura = self.env['account.move'].create(factura_vals)
                record.factura_id = factura.id

                # Publicar la factura automáticamente
                factura.action_post()
