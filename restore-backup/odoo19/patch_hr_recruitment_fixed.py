#!/usr/bin/env python3
"""Patch hr_recruitment module to handle index creation error gracefully"""

file_path = '/usr/lib/python3/dist-packages/odoo/addons/hr_recruitment/models/ir_attachment.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Step 1: Add logging import if not present
if 'import logging' not in content:
    # Insert after 'from odoo import models'
    content = content.replace(
        'from odoo import models\nfrom odoo.tools import SQL',
        'from odoo import models\nfrom odoo.tools import SQL\nimport logging\n\n_logger = logging.getLogger(__name__)'
    )

# Step 2: Replace the execute call with try-except
# Find the exact pattern
old_pattern = r'(            self\.env\.cr\.execute\(SQL\('''
            r'                CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx'
            r'                    ON ir_attachment USING gin \(%(indexed_field)s gin_trgm_ops\)'
            r'                 WHERE res_model = \'hr\.applicant\''
            r'            ''', indexed_field=indexed_field\)\))'

new_code = '''            try:
                self.env.cr.execute(SQL('''
                    CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
                        ON ir_attachment USING gin (%(indexed_field)s gin_trgm_ops)
                     WHERE res_model = 'hr.applicant'
                ''', indexed_field=indexed_field))
            except Exception as e:
                # Index creation failed, but continue without it
                _logger.warning("Failed to create index ir_attachment_index_content_applicant_trgm_idx: %s", e)'''

# More flexible replacement - find the execute line and replace the whole block
import re

# Pattern to match the execute block
pattern = r'(            self\.env\.cr\.execute\(SQL\('''\s+CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx\s+ON ir_attachment USING gin \(%(indexed_field)s gin_trgm_ops\)\s+WHERE res_model = \'hr\.applicant\'\s+''', indexed_field=indexed_field\)\))'

if re.search(pattern, content, re.MULTILINE):
    content = re.sub(pattern, new_code, content, flags=re.MULTILINE)
    print("✓ Replaced using regex")
else:
    # Manual replacement - find the line and replace
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        if 'self.env.cr.execute(SQL' in lines[i] and 'ir_attachment_index_content_applicant_trgm_idx' in ''.join(lines[i:i+5]):
            # Found the execute line, replace with try-except
            indent = '            '
            new_lines.append(indent + 'try:')
            # Copy the execute line with extra indent
            new_lines.append(indent + '    ' + lines[i].replace('            ', '    '))
            i += 1
            # Copy SQL block lines
            while i < len(lines) and (lines[i].strip().startswith("'''") or 'CREATE INDEX' in lines[i] or 'ON ir_attachment' in lines[i] or 'WHERE res_model' in lines[i] or "indexed_field=indexed_field" in lines[i]):
                if lines[i].strip() and not lines[i].strip().startswith("'''"):
                    new_lines.append(indent + '    ' + lines[i].lstrip())
                else:
                    new_lines.append(lines[i])
                i += 1
            # Add except block
            new_lines.append(indent + 'except Exception as e:')
            new_lines.append(indent + '    _logger.warning("Failed to create index ir_attachment_index_content_applicant_trgm_idx: %s", e)')
        else:
            new_lines.append(lines[i])
            i += 1
    content = '\n'.join(new_lines)
    print("✓ Replaced using line-by-line")

# Write the file
with open(file_path, 'w') as f:
    f.write(content)

print("✓ File patched successfully")

