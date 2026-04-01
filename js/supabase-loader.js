// Supabase API Loader - For Vercel/GitHub Pages deployment
// Supabase credentials
const SUPABASE_URL = 'https://fqdwvbgbzusqushsxzlx.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxZHd2YmdienVzcXVzaHN4emx4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5Njc1NzUsImV4cCI6MjA5MDU0MzU3NX0.C6Xs8eMSqd50ZSWa6YkhOpppdpF0A5aLDljffmF2rXU';

const supabaseApi = {
    // Fetch all data from Supabase
    async loadSiteData() {
        try {
            const [newsRes, eventsRes, downloadsRes, carouselRes, announcementsRes, deptRes, facultyRes, activitiesRes, achievementsRes, galleryRes] = await Promise.all([
                fetch(`${SUPABASE_URL}/rest/v1/news?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/events?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/downloads?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/carousel?select=*&order=id.asc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/announcements?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/departments?select=*`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/faculty?select=*`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/activities?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/achievements?select=*&order=id.desc`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                }),
                fetch(`${SUPABASE_URL}/rest/v1/gallery?select=*`, {
                    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
                })
            ]);

            // Check if responses are OK (200-299)
            if (!newsRes.ok || !eventsRes.ok || !downloadsRes.ok || !carouselRes.ok || !announcementsRes.ok) {
                console.log('Supabase response not OK, using local data');
                return loadLocalData();
            }

            const news = await newsRes.json();
            const events = await eventsRes.json();
            const downloads = await downloadsRes.json();
            const carousel = await carouselRes.json();
            const announcements = await announcementsRes.json();
            const departments = await deptRes.json();
            const faculty = await facultyRes.json();
            const activities = await activitiesRes.json();
            const achievements = await achievementsRes.json();
            const gallery = await galleryRes.json();

            // Check if responses are arrays (not error objects)
            if (!Array.isArray(news) || !Array.isArray(events) || !Array.isArray(downloads)) {
                console.log('Supabase returned error, using local data');
                return loadLocalData();
            }

            // Build departments object from Supabase data
            const deptObj = {};
            if (Array.isArray(departments)) {
                departments.forEach(d => {
                    deptObj[d.dept_key] = {
                        name: d.name,
                        icon: d.icon,
                        about: d.about,
                        vision: d.vision,
                        mission: d.mission,
                        hod: { name: d.hod_name, designation: d.hod_designation, qualification: d.hod_qualification },
                        faculty: [],
                        activities: [],
                        achievements: [],
                        gallery: []
                    };
                });
            }

            // Add faculty to departments
            if (Array.isArray(faculty)) {
                faculty.forEach(f => {
                    if (deptObj[f.dept_key]) {
                        deptObj[f.dept_key].faculty.push({
                            name: f.name,
                            designation: f.designation,
                            qualification: f.qualification,
                            email: f.email,
                            phone: f.phone,
                            image: f.image,
                            resume: f.resume
                        });
                    }
                });
            }

            // Add activities to departments
            if (Array.isArray(activities)) {
                activities.forEach(a => {
                    if (deptObj[a.dept_key]) {
                        deptObj[a.dept_key].activities.push({
                            title: a.title,
                            description: a.description
                        });
                    }
                });
            }

            // Add achievements to departments
            if (Array.isArray(achievements)) {
                achievements.forEach(a => {
                    if (deptObj[a.dept_key]) {
                        deptObj[a.dept_key].achievements.push({
                            title: a.title,
                            description: a.description,
                            student_name: a.student_name
                        });
                    }
                });
            }

            // Add gallery to departments
            if (Array.isArray(gallery)) {
                gallery.forEach(g => {
                    if (deptObj[g.dept_key]) {
                        deptObj[g.dept_key].gallery.push({
                            src: g.img,
                            caption: g.caption
                        });
                    }
                });
            }

            return {
                news: news.map(n => ({ title: n.title, date: n.date, icon: n.icon || 'fa-bullhorn' })),
                events: events.map(e => ({ title: e.title, date: e.date, icon: e.icon || 'fa-calendar' })),
                downloads: downloads.map(d => ({ title: d.title, link: d.link, icon: d.icon || 'fa-download' })),
                carousel: carousel.map(c => ({ img: c.img, alt: c.alt })),
                announcements: announcements.map(a => ({ text: a.text })),
                departments: deptObj
            };
        } catch (error) {
            console.log('Supabase Error:', error.message, '- Using local data');
            return loadLocalData();
        }
    },
                announcements: announcements.map(a => ({ text: a.text }))
            };
        } catch (error) {
            console.log('Supabase Error:', error.message, '- Using local data');
            return loadLocalData();
        }
    },

    // Save data to Supabase (for admin)
    async saveData(type, data) {
        try {
            let endpoint = '';
            let body = {};

            switch(type) {
                case 'news':
                    endpoint = `${SUPABASE_URL}/rest/v1/news`;
                    body = { title: data.title, date: data.date, icon: data.icon };
                    break;
                case 'events':
                    endpoint = `${SUPABASE_URL}/rest/v1/events`;
                    body = { title: data.title, date: data.date, icon: data.icon };
                    break;
                case 'downloads':
                    endpoint = `${SUPABASE_URL}/rest/v1/downloads`;
                    body = { title: data.title, link: data.link, icon: data.icon };
                    break;
                case 'announcements':
                    endpoint = `${SUPABASE_URL}/rest/v1/announcements`;
                    body = { text: data.text };
                    break;
                case 'carousel':
                    endpoint = `${SUPABASE_URL}/rest/v1/carousel`;
                    body = { img: data.img, alt: data.alt };
                    break;
                case 'department':
                    endpoint = `${SUPABASE_URL}/rest/v1/departments`;
                    body = { 
                        dept_key: data.dept_key, 
                        name: data.name, 
                        icon: data.icon,
                        about: data.about,
                        vision: data.vision,
                        mission: data.mission,
                        hod_name: data.hod_name,
                        hod_designation: data.hod_designation,
                        hod_qualification: data.hod_qualification
                    };
                    break;
                case 'faculty':
                    endpoint = `${SUPABASE_URL}/rest/v1/faculty`;
                    body = { 
                        dept_key: data.dept_key,
                        name: data.name, 
                        designation: data.designation, 
                        qualification: data.qualification,
                        email: data.email,
                        phone: data.phone,
                        image: data.image,
                        resume: data.resume
                    };
                    break;
                case 'activities':
                    endpoint = `${SUPABASE_URL}/rest/v1/activities`;
                    body = { 
                        dept_key: data.dept_key,
                        title: data.title, 
                        description: data.description,
                        date: data.date
                    };
                    break;
                case 'achievements':
                    endpoint = `${SUPABASE_URL}/rest/v1/achievements`;
                    body = { 
                        dept_key: data.dept_key,
                        title: data.title, 
                        description: data.description,
                        student_name: data.student_name
                    };
                    break;
                case 'gallery':
                    endpoint = `${SUPABASE_URL}/rest/v1/gallery`;
                    body = { 
                        dept_key: data.dept_key,
                        img: data.img, 
                        caption: data.caption
                    };
                    break;
                default:
                    return { success: false, error: 'Invalid type' };
            }

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`,
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                },
                body: JSON.stringify(body)
            });

            if (!response.ok) throw new Error('Failed to save');
            return { success: true, data: await response.json() };
        } catch (error) {
            console.error('Save Error:', error);
            return { success: false, error: error.message };
        }
    },

    // Delete data from Supabase
    async deleteData(type, id) {
        try {
            let tableName = type;
            // Map admin types to table names
            if (type === 'news') tableName = 'news';
            else if (type === 'events') tableName = 'events';
            else if (type === 'downloads') tableName = 'downloads';
            else if (type === 'carousel') tableName = 'carousel';
            else if (type === 'announcements') tableName = 'announcements';
            else if (type === 'department') tableName = 'departments';
            else if (type === 'faculty') tableName = 'faculty';
            else if (type === 'activities') tableName = 'activities';
            else if (type === 'achievements') tableName = 'achievements';
            else if (type === 'gallery') tableName = 'gallery';
            
            const response = await fetch(`${SUPABASE_URL}/rest/v1/${tableName}?id=eq.${id}`, {
                method: 'DELETE',
                headers: {
                    'apikey': SUPABASE_KEY,
                    'Authorization': `Bearer ${SUPABASE_KEY}`
                }
            });
            return { success: response.ok };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
};

// Fallback local data (for when Supabase is not available)
// Using real images from live college website
function loadLocalData() {
    return {
        news: [
            { title: 'International Virtual Conference', date: 'May 02, 2022', icon: 'fa-university' },
            { title: 'E-Workshop on Writing Skills', date: 'July 03 & July 05', icon: 'fas fa-book-open' },
            { title: 'E-Quiz Organised By Computer Science', date: 'May 21 & May 22', icon: 'fa-laptop' },
            { title: 'E-Quiz Organised By NSS Club', date: 'May 26 & May 27', icon: 'fas fa-running' }
        ],
        events: [
            { title: 'Annual Day Celebration', date: 'March 15, 2025', icon: 'fa-calendar' },
            { title: 'Sports Day Events', date: 'February 28, 2025', icon: 'fa-trophy' }
        ],
        downloads: [
            { title: 'Bonafide Certificate', link: 'Documents/Forms/Bonafide.pdf', icon: 'fa-download' },
            { title: 'Attendance Certificate', link: 'Documents/Forms/Attendance.pdf', icon: 'fa-download' },
            { title: 'Academic Calendar 2024-2025', link: 'Documents/calendar/2024-2025 calendar.pdf', icon: 'fa-download' }
        ],
        carousel: [
            { img: 'https://sgacrmd.edu.in/assets/carousel/1.jpg', alt: 'College Entrance' },
            { img: 'https://sgacrmd.edu.in/assets/carousel/2.jpg', alt: 'Academic Block' },
            { img: 'https://sgacrmd.edu.in/assets/carousel/3.jpg', alt: 'Library' },
            { img: 'https://sgacrmd.edu.in/assets/carousel/4.jpg', alt: 'Laboratory' }
        ],
        announcements: [
            { text: 'RankList for I Year PG Admission [2025-2026] Released' },
            { text: 'Special Quota Counselling on 02/06/2025 & 03/06/2025' }
        ]
    };
}

// Override loadSiteData to use Supabase
window.loadSiteData = async function() {
    try {
        return await supabaseApi.loadSiteData();
    } catch (e) {
        console.log('Using local data');
        return loadLocalData();
    }
};
