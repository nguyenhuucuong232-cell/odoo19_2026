-- Fix UNACCENT function for PostgreSQL index creation
-- This script fixes the error: "functions in index expression must be marked IMMUTABLE"

-- Step 1: Ensure extensions are installed
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Step 2: Create text search dictionary if not exists
CREATE TEXT SEARCH DICTIONARY IF NOT EXISTS unaccent (TEMPLATE = unaccent);

-- Step 3: Drop existing problematic index if exists
DROP INDEX IF EXISTS ir_attachment_index_content_applicant_trgm_idx;

-- Step 4: Drop and recreate unaccent function as IMMUTABLE
DROP FUNCTION IF EXISTS unaccent(text) CASCADE;

-- Create IMMUTABLE wrapper function
-- Note: This uses the built-in unaccent function from the extension
CREATE OR REPLACE FUNCTION unaccent(text) 
RETURNS text 
LANGUAGE sql 
IMMUTABLE 
AS $$ 
    SELECT public.unaccent(public.unaccent('unaccent'::regdictionary), $1) 
$$;

-- Step 5: Create the index
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

SELECT 
    indexname,
    CASE 
        WHEN indexname IS NOT NULL THEN 'Index created ✓'
        ELSE 'Index not found ✗'
    END as status
FROM pg_indexes 
WHERE indexname = 'ir_attachment_index_content_applicant_trgm_idx';

