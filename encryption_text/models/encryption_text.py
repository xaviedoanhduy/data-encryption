from odoo import fields, models
from cryptography.fernet import Fernet


class Text(models.Model):
    _name = "encryption.text"
    _description = "Encryption Text"
    _rec_name = "title"
    
    
    title = fields.Char(required=True)
    content = fields.Text(string="Encryption Content")
    decrypted_text_id = fields.Many2one(comodel_name="decryption.text", )
    decrypted_text_content = fields.Text(
        related="decrypted_text_id.content",
        string="Decrypted Content", 
    )
    key_id = fields.Many2one(
        comodel_name="encryption.key", 
        required=True,
    )

    def _action_text_decrypt(self):
        for encryption_text in self:
            fernet = Fernet(encryption_text.key_id.key_value)
            decrypted_text = encryption_text.env["decryption.text"].create({
                "title": f"{encryption_text.title} - decrypted",
                "content": fernet.decrypt(encryption_text.content.encode()),
                "key_id": encryption_text.key_id.id,
            })
            encryption_text.decrypted_text_id = decrypted_text

    def button_decrypt(self):
        self._action_text_decrypt()
