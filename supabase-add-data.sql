-- =====================================================
-- SUPABASE - CHECK AND ADD DATA (Safe version)
-- =====================================================
-- This won't cause duplicate errors
-- =====================================================

-- Check if news has data
SELECT COUNT(*) AS news_count FROM public.news;

-- Check if events has data  
SELECT COUNT(*) AS events_count FROM public.events;

-- Check if carousel has data
SELECT COUNT(*) AS carousel_count FROM public.carousel;

-- If any table is empty, insert data using IDENTITY
INSERT INTO public.news (title, date, icon) VALUES 
('International Virtual Conference on Innovation and Intelligence in Computing System', 'May 02, 2022', 'fa-university'),
('E-Workshop on Writing Skills Organised by English Department', 'July 03 & July 05', 'fas fa-book-open'),
('E-Quiz Organised By Computer Science Department', 'May 21 & May 22', 'fa-laptop'),
('E-Quiz Organised By National Service Scheme Club', 'May 26 & May 27', 'fas fa-running');

INSERT INTO public.events (title, date, icon) VALUES 
('Annual Day Celebration', 'March 15, 2025', 'fa-calendar'),
('Sports Day Events', 'February 28, 2025', 'fa-trophy');

INSERT INTO public.downloads (title, link, icon) VALUES 
('Bonafide Certificate', 'Documents/Forms/Bonafide.pdf', 'fa-download'),
('Attendance Certificate', 'Documents/Forms/Attendance.pdf', 'fa-download'),
('Academic Calendar 2024-2025', 'Documents/calendar/2024-2025 calendar.pdf', 'fa-download');

INSERT INTO public.carousel (img, alt) VALUES 
('https://sgacrmd.edu.in/assets/carousel/1.jpg', 'College Campus'),
('https://sgacrmd.edu.in/assets/carousel/2.jpg', 'Academic Block'),
('https://sgacrmd.edu.in/assets/carousel/3.jpg', 'Library'),
('https://sgacrmd.edu.in/assets/carousel/4.jpg', 'Laboratory');

SELECT 'Done!' AS status;
