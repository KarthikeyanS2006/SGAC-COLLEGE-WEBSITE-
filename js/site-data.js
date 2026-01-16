// Shared site data for News, Events, and Downloads
const SiteData = {
    news: [
        { title: 'International Virtual Conference on Innovation and Intelligence in Computing System', date: 'May 02, 2022', icon: 'fa-university' },
        { title: 'E-Workshop on "Writing Skills" Organised by English Department', date: 'July 03 & July 05', icon: 'fas fa-book-open' },
        { title: 'E-Quiz Organised By Computer Science Department', date: 'May 21 & May 22', icon: 'fa-laptop' },
        { title: 'E-Quiz Organised By National Service Scheme Club', date: 'May 26 & May 27', icon: 'fas fa-running' }
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
    ]
};

// Function to save data to localStorage
function saveSiteData(data) {
    localStorage.setItem('sgac_site_data', JSON.stringify(data));
}

// Function to load data (prioritizes localStorage)
function loadSiteData() {
    const saved = localStorage.getItem('sgac_site_data');
    return saved ? JSON.parse(saved) : SiteData;
}
