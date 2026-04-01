-- =====================================================
-- ADD JSON COLUMNS TO DEPARTMENTS TABLE
-- Run this in Supabase SQL Editor to add missing columns
-- =====================================================

ALTER TABLE public.departments 
ADD COLUMN IF NOT EXISTS faculty_json text,
ADD COLUMN IF NOT EXISTS activities_json text,
ADD COLUMN IF NOT EXISTS achievements_json text,
ADD COLUMN IF NOT EXISTS econtent_json text,
ADD COLUMN IF NOT EXISTS gallery_json text;

-- Insert default department data with faculty info
INSERT INTO public.departments (dept_key, name, icon, about, vision, mission, hod_name, hod_designation, hod_qualification, faculty_json, activities_json, achievements_json, econtent_json, gallery_json) VALUES
('tamil', 'Tamil', 'fa-language', 'The Department of Tamil at Sethupathy Government Arts College is dedicated to preserving and promoting the rich heritage of Tamil language and literature.', 'To be a center of excellence in Tamil language, literature, and cultural studies.', 'To provide quality education in Tamil and preserve the rich linguistic and cultural heritage.', 'Dr. M. Senthamarai', 'Head of Department, Assistant Professor', 'M.A., M.Phil., Ph.D.', '[{"name":"Dr. Muthuraman.S","designation":"Guest Lecturer","qualification":"M.A., M.Phil.","email":"muthuraman@sgac.edu.in","phone":"+91-9876-543211","image":"","resume":"https://drive.google.com/file/d/t2"},{"name":"Dr. Poornayogarani.K","designation":"Guest Lecturer","qualification":"M.A., M.Phil., Ph.D.","email":"poornayogarani@sgac.edu.in","phone":"+91-9876-543212","image":"","resume":"https://drive.google.com/file/d/t3"}]', '[]', '[]', '[]', '[{"src":"https://sgacrmd.edu.in/assets/entrance.jpg","caption":"College Entrance"},{"src":"https://sgacrmd.edu.in/assets/college3.jpg","caption":"Academic Block"}]')
ON CONFLICT (dept_key) DO UPDATE SET
    name = EXCLUDED.name,
    icon = EXCLUDED.icon,
    about = EXCLUDED.about,
    vision = EXCLUDED.vision,
    mission = EXCLUDED.mission,
    hod_name = EXCLUDED.hod_name,
    hod_designation = EXCLUDED.hod_designation,
    hod_qualification = EXCLUDED.hod_qualification,
    faculty_json = EXCLUDED.faculty_json,
    activities_json = EXCLUDED.activities_json,
    achievements_json = EXCLUDED.achievements_json,
    econtent_json = EXCLUDED.econtent_json,
    gallery_json = EXCLUDED.gallery_json;

SELECT 'Department columns added successfully!' AS status;
