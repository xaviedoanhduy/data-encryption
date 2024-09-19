from odoo import fields, models


class Key(models.Model):
    _name = "encryption.key"
    _description = "Encryption Key"

    name = fields.Char()
    key_value = fields.Char()
    text_ids = fields.One2many(
        comodel_name="encryption.text", 
        inverse_name="key_id",
        string="Texts",
    )
