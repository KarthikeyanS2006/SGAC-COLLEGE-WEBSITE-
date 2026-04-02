-- ============================================================
-- STEP 2: Set up Row Level Security
-- Run this SECOND in Supabase SQL Editor
-- ============================================================

-- Enable RLS on all tables
ALTER TABLE news ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE downloads ENABLE ROW LEVEL SECURITY;
ALTER TABLE carousel ENABLE ROW LEVEL SECURITY;
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;
ALTER TABLE departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE faculty ENABLE ROW LEVEL SECURITY;
ALTER TABLE gallery ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE econtent ENABLE ROW LEVEL SECURITY;
ALTER TABLE site_config ENABLE ROW LEVEL SECURITY;

-- Public read policies (everyone can read)
CREATE POLICY "Public read news" ON news FOR SELECT USING (true);
CREATE POLICY "Public read events" ON events FOR SELECT USING (true);
CREATE POLICY "Public read downloads" ON downloads FOR SELECT USING (true);
CREATE POLICY "Public read carousel" ON carousel FOR SELECT USING (true);
CREATE POLICY "Public read announcements" ON announcements FOR SELECT USING (true);
CREATE POLICY "Public read departments" ON departments FOR SELECT USING (true);
CREATE POLICY "Public read faculty" ON faculty FOR SELECT USING (true);
CREATE POLICY "Public read gallery" ON gallery FOR SELECT USING (true);
CREATE POLICY "Public read activities" ON activities FOR SELECT USING (true);
CREATE POLICY "Public read achievements" ON achievements FOR SELECT USING (true);
CREATE POLICY "Public read econtent" ON econtent FOR SELECT USING (true);
CREATE POLICY "Public read site_config" ON site_config FOR SELECT USING (true);

-- Admin write policies (only authenticated users can write)
CREATE POLICY "Admin insert news" ON news FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update news" ON news FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete news" ON news FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert events" ON events FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update events" ON events FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete events" ON events FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert downloads" ON downloads FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update downloads" ON downloads FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete downloads" ON downloads FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert carousel" ON carousel FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update carousel" ON carousel FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete carousel" ON carousel FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert announcements" ON announcements FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update announcements" ON announcements FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete announcements" ON announcements FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert departments" ON departments FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update departments" ON departments FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete departments" ON departments FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert faculty" ON faculty FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update faculty" ON faculty FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete faculty" ON faculty FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert gallery" ON gallery FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update gallery" ON gallery FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete gallery" ON gallery FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert activities" ON activities FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update activities" ON activities FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete activities" ON activities FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert achievements" ON achievements FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update achievements" ON achievements FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete achievements" ON achievements FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert econtent" ON econtent FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update econtent" ON econtent FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Admin delete econtent" ON econtent FOR DELETE USING (auth.role() = 'authenticated');

CREATE POLICY "Admin insert site_config" ON site_config FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Admin update site_config" ON site_config FOR UPDATE USING (auth.role() = 'authenticated');

-- Auto-update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_news_updated_at BEFORE UPDATE ON news FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_downloads_updated_at BEFORE UPDATE ON downloads FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_carousel_updated_at BEFORE UPDATE ON carousel FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_announcements_updated_at BEFORE UPDATE ON announcements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_faculty_updated_at BEFORE UPDATE ON faculty FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_site_config_updated_at BEFORE UPDATE ON site_config FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Indexes
CREATE INDEX IF NOT EXISTS idx_faculty_department ON faculty(department_id);
CREATE INDEX IF NOT EXISTS idx_gallery_department ON gallery(department_id);
CREATE INDEX IF NOT EXISTS idx_activities_department ON activities(department_id);
CREATE INDEX IF NOT EXISTS idx_achievements_department ON achievements(department_id);
CREATE INDEX IF NOT EXISTS idx_econtent_department ON econtent(department_id);
CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_carousel_sort ON carousel(sort_order ASC);
