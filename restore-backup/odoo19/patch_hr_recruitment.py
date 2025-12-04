#!/usr/bin/env python3
# Patch hr_recruitment module to handle index creation error

file_path = '/usr/lib/python3/dist-packages/odoo/addons/hr_recruitment/models/ir_attachment.py'

with open(file_path, 'r') as f:
    content = f.read()

# Add import if not exists
if 'import logging' not in content:
    content = content.replace(
        'from odoo import models',
        'from odoo import models\nimport logging\n\n_logger = logging.getLogger(__name__)'
    )

# Replace the init method
old_init = '''    def init(self):
        if self.env.registry.has_trigram:
            indexed_field = SQL('UNACCENT(index_content)') if self.env.registry.has_unaccent else SQL('index_content')

            self.env.cr.execute(SQL('''
                CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
                    ON ir_attachment USING gin (%(indexed_field)s gin_trgm_ops)
                 WHERE res_model = 'hr.applicant'
            ''', indexed_field=indexed_field))'''

new_init = '''    def init(self):
        if self.env.registry.has_trigram:
            indexed_field = SQL('UNACCENT(index_content)') if self.env.registry.has_unaccent else SQL('index_content')

            try:
                self.env.cr.execute(SQL('''
                    CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
                        ON ir_attachment USING gin (%(indexed_field)s gin_trgm_ops)
                     WHERE res_model = 'hr.applicant'
                ''', indexed_field=indexed_field))
            except Exception as e:
                # Index creation failed, but continue without it
                _logger.warning("Failed to create index ir_attachment_index_content_applicant_trgm_idx: %s", e)'''

content = content.replace(old_init, new_init)

with open(file_path, 'w') as f:
    f.write(content)

print("File patched successfully")

