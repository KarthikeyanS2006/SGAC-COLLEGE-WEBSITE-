-- Fix RLS policies for Supabase
-- Run this in Supabase SQL Editor

-- Drop existing policies
DROP POLICY IF EXISTS "Allow public read access for news" ON public.news;
DROP POLICY IF EXISTS "Allow authenticated insert for news" ON public.news;
DROP POLICY IF EXISTS "news_insert" ON public.news;

DROP POLICY IF EXISTS "Allow public read access for events" ON public.events;
DROP POLICY IF EXISTS "Allow authenticated insert for events" ON public.events;
DROP POLICY IF EXISTS "events_insert" ON public.events;

DROP POLICY IF EXISTS "Allow public read access for downloads" ON public.downloads;
DROP POLICY IF EXISTS "Allow authenticated insert for downloads" ON public.downloads;
DROP POLICY IF EXISTS "downloads_insert" ON public.downloads;

DROP POLICY IF EXISTS "Allow public read access for carousel" ON public.carousel;
DROP POLICY IF EXISTS "Allow authenticated insert for carousel" ON public.carousel;
DROP POLICY IF EXISTS "carousel_insert" ON public.carousel;

DROP POLICY IF EXISTS "Allow public read access for announcements" ON public.announcements;
DROP POLICY IF EXISTS "Allow authenticated insert for announcements" ON public.announcements;
DROP POLICY IF EXISTS "announcements_insert" ON public.announcements;

DROP POLICY IF EXISTS "departments_read" ON public.departments;
DROP POLICY IF EXISTS "departments_insert" ON public.departments;

-- Create permissive policies for anon key
CREATE POLICY "anon_read_news" ON public.news FOR SELECT USING (true);
CREATE POLICY "anon_insert_news" ON public.news FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_news" ON public.news FOR UPDATE USING (true);
CREATE POLICY "anon_delete_news" ON public.news FOR DELETE USING (true);

CREATE POLICY "anon_read_events" ON public.events FOR SELECT USING (true);
CREATE POLICY "anon_insert_events" ON public.events FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_events" ON public.events FOR UPDATE USING (true);
CREATE POLICY "anon_delete_events" ON public.events FOR DELETE USING (true);

CREATE POLICY "anon_read_downloads" ON public.downloads FOR SELECT USING (true);
CREATE POLICY "anon_insert_downloads" ON public.downloads FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_downloads" ON public.downloads FOR UPDATE USING (true);
CREATE POLICY "anon_delete_downloads" ON public.downloads FOR DELETE USING (true);

CREATE POLICY "anon_read_carousel" ON public.carousel FOR SELECT USING (true);
CREATE POLICY "anon_insert_carousel" ON public.carousel FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_carousel" ON public.carousel FOR UPDATE USING (true);
CREATE POLICY "anon_delete_carousel" ON public.carousel FOR DELETE USING (true);

CREATE POLICY "anon_read_announcements" ON public.announcements FOR SELECT USING (true);
CREATE POLICY "anon_insert_announcements" ON public.announcements FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_announcements" ON public.announcements FOR UPDATE USING (true);
CREATE POLICY "anon_delete_announcements" ON public.announcements FOR DELETE USING (true);

CREATE POLICY "anon_read_departments" ON public.departments FOR SELECT USING (true);
CREATE POLICY "anon_insert_departments" ON public.departments FOR INSERT WITH CHECK (true);
CREATE POLICY "anon_update_departments" ON public.departments FOR UPDATE USING (true);
CREATE POLICY "anon_delete_departments" ON public.departments FOR DELETE USING (true);

SELECT 'RLS policies fixed!' AS status;
