from odoo import fields, models
from cryptography.fernet import Fernet


class Text(models.Model):
    _name = "decryption.text"
    _description = "Decryption Text"
    _rec_name = "title"
    
    
    title = fields.Char(required=True)
    content = fields.Text(required=True)
    key_id = fields.Many2one(
        comodel_name="encryption.key", 
        required=True,
    )
