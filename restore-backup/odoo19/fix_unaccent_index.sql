-- Fix UNACCENT function to be IMMUTABLE for PostgreSQL indexes
-- This fixes the error: "functions in index expression must be marked IMMUTABLE"

-- Step 1: Ensure extensions are installed
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Step 2: Create IMMUTABLE wrapper for unaccent function
CREATE OR REPLACE FUNCTION unaccent(text) 
RETURNS text 
AS $$ 
    SELECT unaccent('unaccent', $1) 
$$ 
LANGUAGE sql IMMUTABLE;

-- Step 3: Drop existing problematic index if exists
DROP INDEX IF EXISTS ir_attachment_index_content_applicant_trgm_idx;

-- Step 4: Recreate index with IMMUTABLE function
CREATE INDEX IF NOT EXISTS ir_attachment_index_content_applicant_trgm_idx
    ON ir_attachment 
    USING gin (unaccent(index_content) gin_trgm_ops)
    WHERE res_model = 'hr.applicant';

-- Verify
SELECT 
    proname, 
    provolatile,
    CASE 
        WHEN provolatile = 'i' THEN 'IMMUTABLE ✓'
        WHEN provolatile = 's' THEN 'STABLE'
        ELSE 'VOLATILE ✗'
    END as status
FROM pg_proc 
WHERE proname = 'unaccent' AND pronargs = 1;

