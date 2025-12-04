# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import jwt
import requests
from odoo import http, _
from odoo.http import request


class OnlyOfficeController(http.Controller):

    @http.route('/sgc_onlyoffice/editor/<int:attachment_id>', type='http', auth='user')
    def open_editor(self, attachment_id, **kwargs):
        """Render OnlyOffice editor page"""
        attachment = request.env['ir.attachment'].browse(attachment_id)
        if not attachment.exists():
            return request.not_found()
        
        company = request.env.company
        onlyoffice_url = company.sgc_onlyoffice_url
        
        if not onlyoffice_url:
            return request.render('sgc_onlyoffice.error_page', {
                'error': _('OnlyOffice Server chưa được cấu hình.')
            })
        
        # Generate document key
        doc_key = hashlib.md5(
            f"{attachment.id}_{attachment.write_date}".encode()
        ).hexdigest()
        
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        config = {
            'document': {
                'fileType': attachment.name.split('.')[-1].lower(),
                'key': doc_key,
                'title': attachment.name,
                'url': f"{base_url}/sgc_onlyoffice/download/{attachment.id}",
            },
            'documentType': attachment._get_onlyoffice_document_type(),
            'editorConfig': {
                'callbackUrl': f"{base_url}/sgc_onlyoffice/callback/{attachment.id}",
                'lang': request.env.user.lang or 'vi',
                'user': {
                    'id': str(request.env.user.id),
                    'name': request.env.user.name,
                },
                'customization': {
                    'autosave': True,
                    'forcesave': True,
                },
            },
        }
        
        # Sign with JWT if secret is configured
        secret = company.sgc_onlyoffice_secret
        if secret:
            config['token'] = jwt.encode(config, secret, algorithm='HS256')
        
        return request.render('sgc_onlyoffice.editor_page', {
            'onlyoffice_url': onlyoffice_url,
            'config': json.dumps(config),
            'attachment': attachment,
        })

    @http.route('/sgc_onlyoffice/download/<int:attachment_id>', type='http', auth='public')
    def download_file(self, attachment_id, **kwargs):
        """Serve file to OnlyOffice server"""
        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
        if not attachment.exists():
            return request.not_found()
        
        file_content = base64.b64decode(attachment.datas) if attachment.datas else b''
        
        return request.make_response(
            file_content,
            headers=[
                ('Content-Type', attachment.mimetype or 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{attachment.name}"'),
            ]
        )

    @http.route('/sgc_onlyoffice/callback/<int:attachment_id>', type='json', auth='public', csrf=False)
    def callback(self, attachment_id, **kwargs):
        """Handle callback from OnlyOffice server"""
        data = request.jsonrequest
        status = data.get('status')
        
        # Status 2 = document is ready for saving
        # Status 6 = document is being edited but changes are saved
        if status in [2, 6]:
            url = data.get('url')
            if url:
                try:
                    response = requests.get(url, timeout=30)
                    if response.status_code == 200:
                        attachment = request.env['ir.attachment'].sudo().browse(attachment_id)
                        if attachment.exists():
                            attachment.write({
                                'datas': base64.b64encode(response.content)
                            })
                except Exception as e:
                    return {'error': 1, 'message': str(e)}
        
        return {'error': 0}

