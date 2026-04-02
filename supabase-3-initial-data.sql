-- ============================================================
-- STEP 3: Insert initial data
-- Run this THIRD in Supabase SQL Editor
-- ============================================================

-- Site Config
INSERT INTO site_config (id, college_name, college_name_tamil, address, naac_grade, affiliated_to, email, phone, principal_name, principal_qualification)
VALUES (1, 'Sethupathy Government Arts College', 'செதுபாதி அரசு கலை கல்லூரி', 'Ramanathapuram-623501', 'B', 'Alagappa University, Karaikudi', 'administration@sgacrmd.edu.in', '+91-4567-221343', 'Dr. P. Seenuvasa Kumaran', 'M.Sc., M.Phil., B.Ed., PGDCA, Ph.D.')
ON CONFLICT (id) DO NOTHING;

-- Departments
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

-- News
INSERT INTO news (title, date, icon) VALUES
('International Virtual Conference on Innovation and Intelligence in Computing System', 'May 02, 2022', 'fa-university'),
('E-Workshop on "Writing Skills" Organised by English Department', 'July 03 & July 05', 'fas fa-book-open'),
('E-Quiz Organised By Computer Science Department', 'May 21 & May 22', 'fa-laptop'),
('E-Quiz Organised By National Service Scheme Club', 'May 26 & May 27', 'fas fa-running')
ON CONFLICT DO NOTHING;

-- Events
INSERT INTO events (title, date, icon) VALUES
('Annual Day Celebration', 'March 15, 2025', 'fa-calendar'),
('Sports Day Events', 'February 28, 2025', 'fa-trophy')
ON CONFLICT DO NOTHING;

-- Downloads
INSERT INTO downloads (title, link, icon) VALUES
('Bonafide Certificate', 'Documents/Forms/Bonafide.pdf', 'fa-download'),
('Attendance Certificate', 'Documents/Forms/Attendance.pdf', 'fa-download'),
('Academic Calendar 2024-2025', 'Documents/calendar/2024-2025 calendar.pdf', 'fa-download')
ON CONFLICT DO NOTHING;

-- Carousel
INSERT INTO carousel (img, alt, sort_order) VALUES
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/1.jpg', 'College Campus', 1),
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/2.jpg', 'Laboratory', 2),
('https://sgacrmd.edu.in/assets/carousel/7-01-2026/3.jpg', 'Library', 3)
ON CONFLICT DO NOTHING;

-- Announcements
INSERT INTO announcements (text) VALUES
('RankList for I Year PG Admission [2025-2026] Released'),
('Special Quota Counselling on 02/06/2025 & 03/06/2025'),
('Science Stream Counselling on 04/06/2025 & 05/06/2025')
ON CONFLICT DO NOTHING;
