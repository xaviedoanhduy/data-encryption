from odoo import fields, models
from cryptography.fernet import Fernet

class PlainText(models.Model):
    _name = "plain.text"
    _description = "Plain Text"
    _rec_name = "title"

    title = fields.Char(required=True)
    content = fields.Text(required=True)
    key_id = fields.Many2one(
        comodel_name="encryption.key", 
    )
    encrypted_text_id = fields.Many2one(comodel_name="encryption.text")
    encrypted_text_content = fields.Text(related="encrypted_text_id.content")
    
    def button_generate_key(self):
        self.ensure_one()
        if not self.key_id:
            key = self.env["encryption.key"].create(
                {
                    "name": f"{self.title} - key",
                    "key_value": Fernet.generate_key(),
                }
            )
            self.key_id = key
        else:
            self.key_id.key_value = Fernet.generate_key()

    def _action_text_encrypt(self):
        for plain_text in self:
            fernet = Fernet(plain_text.key_id.key_value)
            encrypted_text = plain_text.env["encryption.text"].create({
                "title": f"{plain_text.title} - encrypted",
                "content": fernet.encrypt(plain_text.content.encode()),
                "key_id": plain_text.key_id.id,
            })
            plain_text.encrypted_text_id = encrypted_text

    def button_encrypt(self):
        self.ensure_one()
        self._action_text_encrypt()
