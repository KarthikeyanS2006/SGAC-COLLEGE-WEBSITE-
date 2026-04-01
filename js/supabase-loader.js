// Supabase API Loader - For Vercel/GitHub Pages deployment
// Supabase credentials
const SUPABASE_URL = 'https://fqdwvbgbzusqushsxzlx.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxZHd2YmdienVzcXVzaHN4emx4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5Njc1NzUsImV4cCI6MjA5MDU0MzU3NX0.C6Xs8eMSqd50ZSWa6YkhOpppdpF0A5aLDljffmF2rXU';

const supabaseApi = {
    // Fetch all data from Supabase
    async loadSiteData() {
        try {
            const [newsRes, eventsRes, downloadsRes, carouselRes, announcementsRes] = await Promise.all([
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

            // Check if responses are arrays (not error objects)
            if (!Array.isArray(news) || !Array.isArray(events) || !Array.isArray(downloads)) {
                console.log('Supabase returned error, using local data');
                return loadLocalData();
            }

            return {
                news: news.map(n => ({ title: n.title, date: n.date, icon: n.icon || 'fa-bullhorn' })),
                events: events.map(e => ({ title: e.title, date: e.date, icon: e.icon || 'fa-calendar' })),
                downloads: downloads.map(d => ({ title: d.title, link: d.link, icon: d.icon || 'fa-download' })),
                carousel: carousel.map(c => ({ img: c.img, alt: c.alt })),
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
            const response = await fetch(`${SUPABASE_URL}/rest/v1/${type}?id=eq.${id}`, {
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
