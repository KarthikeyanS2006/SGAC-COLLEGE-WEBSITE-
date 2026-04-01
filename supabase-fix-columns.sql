-- Add all missing columns to departments table
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS icon text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS hod_name text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS hod_designation text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS hod_qualification text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS faculty_json text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS activities_json text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS achievements_json text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS econtent_json text;
ALTER TABLE public.departments ADD COLUMN IF NOT EXISTS gallery_json text;

SELECT 'All columns added!' AS status;
