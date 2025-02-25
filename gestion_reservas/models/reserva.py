from odoo import models, fields, api
from datetime import timedelta, datetime, timezone
from odoo.exceptions import ValidationError

class Reserva(models.Model):
    _name = "res.booking"
    _description = "Reserva"

    # Campos
    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción', required=True)
    duracion = fields.Integer(string='Duración (días)', required=True)
    fecha = fields.Datetime(string='Fecha y Hora de Inicio', required=True)
    estado = fields.Selection([
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

    def _comprobar_solapamiento_reservas(self):
        """
        Comprueba si hay reservas que se solapen con el período de tiempo de esta reserva
        para el mismo coche.
        """
        for record in self:
            if record.fecha and record.duracion and record.coche_id:
                fecha_inicio = record.fecha
                fecha_fin = fecha_inicio + timedelta(days=record.duracion)

# Verificación de fecha pasada
            if fecha_inicio < datetime.now():
                raise ValidationError("La fecha de la reserva no puede ser anterior a la fecha actual.")

            # Buscar reservas que se solapen con el período de tiempo
            reservas_solapadas = self.search([
                ('coche_id', '=', record.coche_id.id),
                ('id', '!=', record.id),  # Excluir la reserva actual
                ('fecha', '<', fecha_fin),
                ('fecha', '>=', fecha_inicio),
            ])

            if reservas_solapadas:
                raise ValidationError(
                    "El coche ya está reservado en el período de tiempo seleccionado."
                )

    @api.model
    def create(self, vals):
        # Antes de crear la reserva, comprobar si hay solapamiento
        reserva = super(Reserva, self).create(vals)
        reserva._comprobar_solapamiento_reservas()
        return reserva

    def write(self, vals):
        # Antes de actualizar la reserva, comprobar si hay solapamiento
        result = super(Reserva, self).write(vals)
        self._comprobar_solapamiento_reservas()
        return result


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
                record.write({'estado': 'confirmada'})


    def action_cancelar_reserva(self):
        self.write({'estado': 'cancelada'})
    
    def cancelar_reservas_pendientes(self):
        """Cancela las reservas en estado 'pendiente' por más de 24 horas."""
        ahora = datetime.now(timezone.utc)
        limite_tiempo = ahora - timedelta(hours=24)
        reservas_pendientes = self.search([
            ('estado', '=', 'pendiente'),
            ('create_date', '<', fields.Datetime.to_string(limite_tiempo)),
        ])
        for reserva in reservas_pendientes:
            reserva.action_cancelar_reserva()




