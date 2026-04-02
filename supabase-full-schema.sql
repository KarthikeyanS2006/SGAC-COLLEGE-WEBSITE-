-- ============================================================
-- SGAC College Website - Supabase Database Setup
-- ============================================================
-- Run this in Supabase SQL Editor:
-- 1. Go to https://supabase.com/dashboard
-- 2. Select your project
-- 3. Go to SQL Editor
-- 4. Paste this entire script and run it
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- NEWS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS news (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-bullhorn',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- EVENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-calendar',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- DOWNLOADS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS downloads (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT DEFAULT '',
    icon TEXT DEFAULT 'fa-download',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- CAROUSEL TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS carousel (
    id BIGSERIAL PRIMARY KEY,
    img TEXT NOT NULL,
    alt TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ANNOUNCEMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS announcements (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- DEPARTMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS departments (
    id BIGSERIAL PRIMARY KEY,
    dept_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT DEFAULT 'fa-book',
    about TEXT DEFAULT '',
    vision TEXT DEFAULT '',
    mission TEXT DEFAULT '',
    hod_name TEXT DEFAULT '',
    hod_designation TEXT DEFAULT '',
    hod_qualification TEXT DEFAULT '',
    hod_email TEXT DEFAULT '',
    hod_phone TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- FACULTY TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS faculty (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    designation TEXT DEFAULT '',
    qualification TEXT DEFAULT '',
    email TEXT DEFAULT '',
    phone TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- GALLERY TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS gallery (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    src TEXT NOT NULL,
    caption TEXT DEFAULT '',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ACTIVITIES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS activities (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    date TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ACHIEVEMENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS achievements (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    student_name TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ECONTENT TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS econtent (
    id BIGSERIAL PRIMARY KEY,
    department_id BIGINT REFERENCES departments(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    link TEXT DEFAULT '',
    description TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SITE CONFIG TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS site_config (
    id SERIAL PRIMARY KEY,
    college_name TEXT DEFAULT 'Sethupathy Government Arts College',
    college_name_tamil TEXT DEFAULT 'செதுபாதி அரசு கலை கல்லூரி',
    address TEXT DEFAULT 'Ramanathapuram-623501',
    naac_grade TEXT DEFAULT 'B',
    affiliated_to TEXT DEFAULT 'Alagappa University, Karaikudi',
    email TEXT DEFAULT 'administration@sgacrmd.edu.in',
    phone TEXT DEFAULT '+91-4567-221343',
    principal_name TEXT DEFAULT 'Dr. P. Seenuvasa Kumaran',
    principal_qualification TEXT DEFAULT 'M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(id)
);

-- ============================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
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

-- ============================================================
-- PUBLIC READ ACCESS (Anyone can read content)
-- ============================================================

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

-- ============================================================
-- ADMIN WRITE ACCESS (Authenticated users only)
-- ============================================================

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

-- ============================================================
-- INITIAL DATA: Site Config
-- ============================================================
INSERT INTO site_config (id, college_name, college_name_tamil, address, naac_grade, affiliated_to, email, phone, principal_name, principal_qualification)
VALUES (1, 'Sethupathy Government Arts College', 'செதுபாதி அரசு கலை கல்லூரி', 'Ramanathapuram-623501', 'B', 'Alagappa University, Karaikudi', 'administration@sgacrmd.edu.in', '+91-4567-221343', 'Dr. P. Seenuvasa Kumaran', 'M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.')
ON CONFLICT (id) DO NOTHING;

-- ============================================================
-- INITIAL DATA: Departments (matching existing SiteData)
-- ============================================================
INSERT INTO departments (dept_key, name, icon, about, vision, mission, hod_name, hod_designation, hod_qualification, sort_order) VALUES
('tamil', 'Tamil', 'fa-language', 'The Department of Tamil at Sethupathy Government Arts College is dedicated to preserving and promoting the rich heritage of Tamil language and literature.', 'To be a center of excellence in Tamil language, literature, and cultural studies.', 'To provide quality education in Tamil and preserve the rich linguistic and cultural heritage.', 'Dr. M. Senthamarai', 'Head of Department, Assistant Professor', 'M.A., M.Phil., Ph.D.', 1),
('english', 'English', 'fa-language', 'The Department of English at Sethupathy Government Arts College is dedicated to providing quality education in English language and literature.', 'To be a center of excellence in English language and literature, fostering critical thinking and effective communication.', 'To provide quality education in English and develop language skills for global competitiveness.', 'Dr. K. Jeyamurugan', 'Head of Department, Assistant Professor', 'M.A., M.Phil., Ph.D.', 2),
('botany', 'Botany', 'fa-leaf', 'The Department of Botany provides education in plant biology and biodiversity.', 'To be a center of excellence in botanical sciences.', 'To provide quality education in botany and promote environmental awareness.', 'Dr. K. Raveendra Rethnam', 'Head of Department, Assistant Professor', 'M.Sc., M.Phil., Ph.D.', 3),
('chemistry', 'Chemistry', 'fa-flask', 'The Department of Chemistry provides education in organic, inorganic, and physical chemistry.', 'To be a center of excellence in chemistry education and research.', 'To provide quality chemistry education and promote chemical research.', 'Dr. N. Uma Sankari', 'Head of Department, Associate Professor', 'M.A., M.Phil., Ph.D.', 4),
('computer', 'Computer Science', 'fa-laptop', 'The Department of Computer Science offers comprehensive programs in programming, software development, and IT.', 'To be a center of excellence in computer science and information technology.', 'To provide quality education in computing and produce skilled IT professionals.', 'Dr. K. Rathidevi', 'Head of Department I/C, Assistant Professor', 'M.A., M.Phil., Ph.D.', 5),
('physics', 'Physics', 'fa-atom', 'The Department of Physics offers comprehensive programs in fundamental and applied physics.', 'To be a center of excellence in physics education and research.', 'To provide quality physics education and promote scientific research.', 'B. Senthil', 'Head of Department, Assistant Professor', 'M.Sc., M.Phil.', 6),
('mathematics', 'Mathematics', 'fa-square-root-alt', 'The Department of Mathematics provides strong foundation in mathematical concepts and problem-solving skills.', 'To be a center of excellence in mathematics education and research.', 'To provide quality mathematics education and foster analytical thinking.', 'Prof. C. Shanmuga Vadivu', 'Head of Department', 'M.Sc., M.Phil., B.Ed., Ph.D., PGDCA', 7),
('zoology', 'Zoology', 'fa-paw', 'The Department of Zoology provides education in animal biology and wildlife studies.', 'To be a center of excellence in zoological sciences.', 'To provide quality education in zoology and promote wildlife conservation.', 'Dr. V. Sivakumaran', 'Head of Department, Assistant Professor', 'M.sc(Zoo)., M.Sc(Micro), Ph.D., M.Ed, M.L., D.Sc., D.Mechanic', 8),
('marinebiology', 'Marine Biology', 'fa-water', 'The Department of Marine Biology provides education in marine science and ocean studies.', 'To be a center of excellence in marine biology education and research.', 'To provide quality education in marine biology and promote marine conservation.', 'Dr. M. A. Badhul Haq', 'Head of Department, Assistant Professor', 'M.A., Ph.D.', 9),
('economics', 'Economics', 'fa-chart-line', 'The Department of Economics provides education in economic theory and applied economics.', 'To be a center of excellence in economics education and research.', 'To provide quality economics education and promote economic development.', 'Dr. K. Ramakrishnan', 'Head of Department, Associate Professor', 'M.A., M.Phil., M.B.A, Ph.D., PGDCA', 10),
('commerce', 'Commerce', 'fa-calculator', 'The Department of Commerce provides quality education in accounting, finance, and business studies.', 'To be a center of excellence in commerce education.', 'To produce competent professionals in the field of commerce and business.', 'Dr. K. Muthalagu', 'Head of Department', 'M.Com., M.Phil., Ph.D.', 11),
('commerceca', 'Commerce CA', 'fa-calculator', 'The Department of Commerce with Computer Applications provides education in commerce with emphasis on computer applications.', 'To be a center of excellence in commerce education with computer applications.', 'To produce skilled professionals in commerce and computer applications.', 'Dr. N. Kesavan', 'Head of Department', 'M.Com., M.B.A., PGDCA., Ph.D.', 12)
ON CONFLICT (dept_key) DO NOTHING;

-- ============================================================
-- INITIAL DATA: Faculty for each department
-- ============================================================
DO $$
DECLARE
    tamil_id BIGINT;
    english_id BIGINT;
    botany_id BIGINT;
    chemistry_id BIGINT;
    computer_id BIGINT;
    physics_id BIGINT;
    mathematics_id BIGINT;
    zoology_id BIGINT;
    marinebiology_id BIGINT;
    economics_id BIGINT;
    commerce_id BIGINT;
    commerceca_id BIGINT;
BEGIN
    SELECT id INTO tamil_id FROM departments WHERE dept_key = 'tamil';
    SELECT id INTO english_id FROM departments WHERE dept_key = 'english';
    SELECT id INTO botany_id FROM departments WHERE dept_key = 'botany';
    SELECT id INTO chemistry_id FROM departments WHERE dept_key = 'chemistry';
    SELECT id INTO computer_id FROM departments WHERE dept_key = 'computer';
    SELECT id INTO physics_id FROM departments WHERE dept_key = 'physics';
    SELECT id INTO mathematics_id FROM departments WHERE dept_key = 'mathematics';
    SELECT id INTO zoology_id FROM departments WHERE dept_key = 'zoology';
    SELECT id INTO marinebiology_id FROM departments WHERE dept_key = 'marinebiology';
    SELECT id INTO economics_id FROM departments WHERE dept_key = 'economics';
    SELECT id INTO commerce_id FROM departments WHERE dept_key = 'commerce';
    SELECT id INTO commerceca_id FROM departments WHERE dept_key = 'commerceca';

    -- Tamil Faculty
    IF tamil_id IS NOT NULL THEN
        INSERT INTO faculty (department_id, name, designation, qualification, email, sort_order) VALUES
        (tamil_id, 'Dr. Muthuraman.S', 'Guest Lecturer', 'M.A., M.Phil.', 'muthuraman@sgac.edu.in', 1),
        (tamil_id, 'Dr. Poornayogarani.K', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', 'poornayogarani@sgac.edu.in', 2),
        (tamil_id, 'Dr. Ramamurthy.S', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', 'ramamurthy@sgac.edu.in', 3),
        (tamil_id, 'Dr. Paul Murugan.V', 'Guest Lecturer', 'M.A., M.Phil., Ph.D., PDF', 'paulmurugan@sgac.edu.in', 4),
        (tamil_id, 'Dr. Rajasekar.A', 'Guest Lecturer', 'M.A., B.Ed., M.Phil., Ph.D.', 'rajasekar@sgac.edu.in', 5),
        (tamil_id, 'Dr. Nagapandi.M', 'Guest Lecturer', 'M.A., M.A., M.A., M.A., B.Ed., M.Phil., Ph.D., PGDSA', 'nagapandi@sgac.edu.in', 6),
        (tamil_id, 'Dr. Alagumurugan.M', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', 'alagumurugan@sgac.edu.in', 7),
        (tamil_id, 'Dr. Syed Kasim.M', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', 'syedkasim@sgac.edu.in', 8)
        ON CONFLICT DO NOTHING;
    END IF;

    -- English Faculty
    IF english_id IS NOT NULL THEN
        INSERT INTO faculty (department_id, name, designation, qualification, email, sort_order) VALUES
        (english_id, 'Barakkathu Nisha.T.A', 'Guest Lecturer', 'M.A., M.Phil., SET, NET', 'barakkathu@sgac.edu.in', 1),
        (english_id, 'Dr. Suthanthira Jothi.D', 'Guest Lecturer', 'M.A., M.Phil., B.Ed.', 'suthanthira@sgac.edu.in', 2),
        (english_id, 'Dr. Nagarajan.K', 'Guest Lecturer', 'M.A., M.Ed., M.Phil.', 'nagarajan@sgac.edu.in', 3),
        (english_id, 'Dr. Martin Prabahar.J', 'Guest Lecturer', 'M.A., B.Ed., M.Phil., Ph.D.', 'martinprabahar@sgac.edu.in', 4),
        (english_id, 'Dr. Raihana Barvin.A', 'Guest Lecturer', 'M.A., M.Phil., Ph.D.', 'raihanabarvin@sgac.edu.in', 5),
        (english_id, 'Dr. Prema Latha.M', 'Guest Lecturer', 'M.A., M.Ed., Ph.D.', 'premalatha@sgac.edu.in', 6),
        (english_id, 'Dr. Seeni Sulthan Ibrahim.M', 'Guest Lecturer', 'M.A., M.Phil., B.Ed., Ph.D.', 'seenisulthan@sgac.edu.in', 7),
        (english_id, 'Dr. John Sujith.A', 'Guest Lecturer', 'M.A., M.Phil., B.Ed., Ph.D.', 'johnsujith@sgac.edu.in', 8)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Computer Science Faculty
    IF computer_id IS NOT NULL THEN
        INSERT INTO faculty (department_id, name, designation, qualification, email, sort_order) VALUES
        (computer_id, 'Fathima Zahira.M', 'Guest Lecturer', 'M.Sc., M.Phil., Ph.D., B.Ed.', 'fathimazahira@sgac.edu.in', 1),
        (computer_id, 'Kalaiselvi.V', 'Guest Lecturer', 'M.Sc., B.Ed., M.Phil., SET', 'kalaiselvi@sgac.edu.in', 2)
        ON CONFLICT DO NOTHING;
    END IF;

    -- Commerce Faculty
    IF commerce_id IS NOT NULL THEN
        INSERT INTO faculty (department_id, name, designation, qualification, email, sort_order) VALUES
        (commerce_id, 'Dr. N. Kesavan', 'Associate Professor', 'M.Com., M.B.A., M.Phil., Ph.D., PGDCA', 'kesavan@sgac.edu.in', 1),
        (commerce_id, 'Dr. Namburajan.N', 'Guest Lecturer', 'M.Com., M.Phil., B.Ed., PGDCS., Ph.D', 'namburajan@sgac.edu.in', 2),
        (commerce_id, 'Dr. Muneeswaran.K', 'Guest Lecturer', 'M.Com., M.Phil., Ph.D., M.Com(PSTM)., PGDCA., PGDCM., PGDMM', 'muneeswaran@sgac.edu.in', 3),
        (commerce_id, 'Dr. Ramachandran.R', 'Guest Lecturer', 'M.Com(CA)., MBA., M.Ed., M.Phil., Ph.D.', 'ramachandran@sgac.edu.in', 4)
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- ============================================================
-- INITIAL DATA: Gallery images
-- ============================================================
DO $$
DECLARE
    tamil_id BIGINT;
    english_id BIGINT;
BEGIN
    SELECT id INTO tamil_id FROM departments WHERE dept_key = 'tamil';
    SELECT id INTO english_id FROM departments WHERE dept_key = 'english';

    IF tamil_id IS NOT NULL THEN
        INSERT INTO gallery (department_id, src, caption, sort_order) VALUES
        (tamil_id, 'https://sgacrmd.edu.in/assets/entrance.jpg', 'College Entrance', 1),
        (tamil_id, 'https://sgacrmd.edu.in/assets/college3.jpg', 'Academic Block', 2),
        (tamil_id, 'https://sgacrmd.edu.in/assets/culturals01.jpg', 'Cultural Activities', 3)
        ON CONFLICT DO NOTHING;
    END IF;

    IF english_id IS NOT NULL THEN
        INSERT INTO gallery (department_id, src, caption, sort_order) VALUES
        (english_id, 'https://sgacrmd.edu.in/assets/entrance.jpg', 'English Department - College View', 1),
        (english_id, 'https://sgacrmd.edu.in/assets/college3.jpg', 'English Department - Academic Block', 2),
        (english_id, 'https://sgacrmd.edu.in/assets/culturals01.jpg', 'English Department - Student Activities', 3)
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- ============================================================
-- INITIAL DATA: News
-- ============================================================
INSERT INTO news (title, date, icon) VALUES
('International Virtual Conference on Innovation and Intelligence in Computing System', 'May 02, 2022', 'fa-university'),
('E-Workshop on "Writing Skills" Organised by English Department', 'July 03 & July 05', 'fas fa-book-open'),
('E-Quiz Organised By Computer Science Department', 'May 21 & May 22', 'fa-laptop'),
('E-Quiz Organised By National Service Scheme Club', 'May 26 & May 27', 'fas fa-running')
ON CONFLICT DO NOTHING;

-- ============================================================
-- INITIAL DATA: Events
-- ============================================================
INSERT INTO events (title, date, icon) VALUES
('Annual Day Celebration', 'March 15, 2025', 'fa-calendar'),
('Sports Day Events', 'February 28, 2025', 'fa-trophy')
ON CONFLICT DO NOTHING;

-- ============================================================
-- INITIAL DATA: Downloads
-- ============================================================
INSERT INTO downloads (title, link, icon) VALUES
('Bonafide Certificate', 'Documents/Forms/Bonafide.pdf', 'fa-download'),
('Attendance Certificate', 'Documents/Forms/Attendance.pdf', 'fa-download'),
('Academic Calendar 2024-2025', 'Documents/calendar/2024-2025 calendar.pdf', 'fa-download')
ON CONFLICT DO NOTHING;

-- ============================================================
-- INITIAL DATA: Carousel
-- ============================================================
INSERT INTO carousel (img, alt, sort_order) VALUES
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/1.jpg', 'College Campus', 1),
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/2.jpg', 'Laboratory', 2),
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/3.jpg', 'Library', 3)
ON CONFLICT DO NOTHING;

-- ============================================================
-- INITIAL DATA: Announcements
-- ============================================================
INSERT INTO announcements (text) VALUES
('RankList for I Year PG Admission [2025-2026] Released'),
('Special Quota Counselling on 02/06/2025 & 03/06/2025'),
('Science Stream Counselling on 04/06/2025 & 05/06/2025')
ON CONFLICT DO NOTHING;

-- ============================================================
-- FUNCTION: Auto-update updated_at timestamp
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply auto-update triggers
CREATE TRIGGER update_news_updated_at BEFORE UPDATE ON news FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_downloads_updated_at BEFORE UPDATE ON downloads FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_carousel_updated_at BEFORE UPDATE ON carousel FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_announcements_updated_at BEFORE UPDATE ON announcements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_faculty_updated_at BEFORE UPDATE ON faculty FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_site_config_updated_at BEFORE UPDATE ON site_config FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- INDEXES for better query performance
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_faculty_department ON faculty(department_id);
CREATE INDEX IF NOT EXISTS idx_gallery_department ON gallery(department_id);
CREATE INDEX IF NOT EXISTS idx_activities_department ON activities(department_id);
CREATE INDEX IF NOT EXISTS idx_achievements_department ON achievements(department_id);
CREATE INDEX IF NOT EXISTS idx_econtent_department ON econtent(department_id);
CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_carousel_sort ON carousel(sort_order ASC);
