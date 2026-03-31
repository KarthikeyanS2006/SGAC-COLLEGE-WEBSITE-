// API-based data loader - Use this instead of site-data.js for live server
// This fetches data from PHP API connected to MySQL database

const API_URL = 'https://sgacrmd.edu.in/api/'; // Change to your actual domain

async function loadSiteDataFromAPI() {
    try {
        const response = await fetch(API_URL + 'get-data.php');
        if (!response.ok) throw new Error('Failed to fetch data');
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        // Fallback to local data if API fails
        return loadLocalData();
    }
}

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
            { img: 'https://sgacrmd.edu.in/assets/carousel/7-01-2026/1.jpg', alt: 'College Campus' },
            { img: 'https://sgacrmd.edu.in/assets/carousel/7-01-2026/2.jpg', alt: 'Laboratory' },
            { img: 'https://sgacrmd.edu.in/assets/carousel/7-01-2026/3.jpg', alt: 'Library' }
        ],
        announcements: [
            { text: 'RankList for I Year PG Admission [2025-2026] Released' },
            { text: 'Special Quota Counselling on 02/06/2025 & 03/06/2025' }
        ]
    };
}

// Save data to API
async function saveToAPI(type, data) {
    try {
        const response = await fetch(API_URL + 'save-data.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type, ...data })
        });
        return await response.json();
    } catch (error) {
        console.error('Save Error:', error);
        return { success: false, error: error.message };
    }
}

// Override the loadSiteData function used by the website
window.loadSiteData = loadSiteDataFromAPI;
