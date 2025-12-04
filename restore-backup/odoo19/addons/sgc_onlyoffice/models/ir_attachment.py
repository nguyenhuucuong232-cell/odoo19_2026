# -*- coding: utf-8 -*-
import hashlib
import time
import jwt
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    sgc_can_edit_onlyoffice = fields.Boolean(
        string='Có thể chỉnh sửa với OnlyOffice',
        compute='_compute_can_edit_onlyoffice'
    )

    SUPPORTED_FORMATS = {
        'word': ['doc', 'docx', 'docm', 'dot', 'dotx', 'dotm', 'odt', 'fodt', 'ott', 'rtf', 'txt'],
        'cell': ['xls', 'xlsx', 'xlsm', 'xlt', 'xltx', 'xltm', 'ods', 'fods', 'ots', 'csv'],
        'slide': ['ppt', 'pptx', 'pptm', 'pot', 'potx', 'potm', 'odp', 'fodp', 'otp'],
    }

    @api.depends('name')
    def _compute_can_edit_onlyoffice(self):
        all_formats = []
        for formats in self.SUPPORTED_FORMATS.values():
            all_formats.extend(formats)
        
        for attachment in self:
            if attachment.name:
                ext = attachment.name.split('.')[-1].lower() if '.' in attachment.name else ''
                attachment.sgc_can_edit_onlyoffice = ext in all_formats
            else:
                attachment.sgc_can_edit_onlyoffice = False

    def _get_onlyoffice_document_type(self):
        """Get document type for OnlyOffice"""
        self.ensure_one()
        if not self.name:
            return None
        
        ext = self.name.split('.')[-1].lower() if '.' in self.name else ''
        
        for doc_type, formats in self.SUPPORTED_FORMATS.items():
            if ext in formats:
                return doc_type
        return None

    def action_open_onlyoffice(self):
        """Open attachment in OnlyOffice editor"""
        self.ensure_one()
        
        if not self.sgc_can_edit_onlyoffice:
            raise UserError(_('Định dạng file không được hỗ trợ bởi OnlyOffice.'))
        
        onlyoffice_url = self.env.company.sgc_onlyoffice_url
        if not onlyoffice_url:
            raise UserError(_('Vui lòng cấu hình URL OnlyOffice Server trong Cài đặt.'))
        
        # Generate document key
        doc_key = hashlib.md5(
            f"{self.id}_{self.write_date}".encode()
        ).hexdigest()
        
        # Build configuration
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        config = {
            'document': {
                'fileType': self.name.split('.')[-1].lower(),
                'key': doc_key,
                'title': self.name,
                'url': f"{base_url}/sgc_onlyoffice/download/{self.id}",
            },
            'documentType': self._get_onlyoffice_document_type(),
            'editorConfig': {
                'callbackUrl': f"{base_url}/sgc_onlyoffice/callback/{self.id}",
                'lang': self.env.user.lang or 'vi',
                'user': {
                    'id': str(self.env.user.id),
                    'name': self.env.user.name,
                },
                'customization': {
                    'autosave': True,
                    'forcesave': True,
                },
            },
        }
        
        # Sign with JWT if secret is configured
        secret = self.env.company.sgc_onlyoffice_secret
        if secret:
            config['token'] = jwt.encode(config, secret, algorithm='HS256')
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/sgc_onlyoffice/editor/{self.id}',
            'target': 'new',
        }

