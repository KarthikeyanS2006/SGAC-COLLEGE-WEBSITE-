// Simple loader - uses localStorage for data

function loadSiteData() {
    const saved = localStorage.getItem('sgac_site_data');
    if (saved) {
        try {
            const parsed = JSON.parse(saved);
            if (parsed.departments) {
                return parsed;
            }
        } catch(e) {}
    }
    return SiteData;
}

window.loadSiteData = loadSiteData;
async function loadSiteData() {
    try {
        const [newsRes, eventsRes, downloadsRes, carouselRes, announcementsRes, deptRes] = await Promise.all([
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
            })
        ]);

        // Check if responses are OK
        if (!newsRes.ok || !eventsRes.ok || !downloadsRes.ok || !carouselRes.ok) {
            throw new Error('Supabase API error');
        }

        const news = await newsRes.json();
        const events = await eventsRes.json();
        const downloads = await downloadsRes.json();
        const carousel = await carouselRes.json();
        const announcements = await announcementsRes.json();
        const departments = await deptRes.json();

        // Verify we got arrays
        if (!Array.isArray(news) || !Array.isArray(events)) {
            throw new Error('Invalid data from Supabase');
        }

        // Build departments object from Supabase
        const deptObj = {};
        if (Array.isArray(departments)) {
            departments.forEach(d => {
                deptObj[d.dept_key] = {
                    name: d.name,
                    icon: d.icon,
                    about: d.about,
                    vision: d.vision,
                    mission: d.mission,
                    hod: { 
                        name: d.hod_name, 
                        designation: d.hod_designation, 
                        qualification: d.hod_qualification 
                    },
                    faculty: d.faculty_json ? JSON.parse(d.faculty_json) : [],
                    activities: d.activities_json ? JSON.parse(d.activities_json) : [],
                    achievements: d.achievements_json ? JSON.parse(d.achievements_json) : [],
                    econtent: d.econtent_json ? JSON.parse(d.econtent_json) : [],
                    gallery: d.gallery_json ? JSON.parse(d.gallery_json) : []
                };
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
        console.log('Supabase Error:', error.message, '- Using static data');
        return SiteData;
    }
}

// Make available globally
window.loadSiteData = loadSiteData;
