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
    ],
    announcements: [
        { text: 'RankList for I Year PG Admission [2025-2026] Released' },
        { text: 'Special Quota Counselling on 02/06/2025 & 03/06/2025' },
        { text: 'Science Stream Counselling on 04/06/2025 & 05/06/2025' }
    ],
    staff: [
        { name: 'Dr. R. Mahesh', designation: 'Principal', department: 'Office' },
        { name: 'M. Sankaran', designation: 'Office Superintendent', department: 'Administrative Office' },
        { name: 'R. Venkatesan', designation: 'Junior Assistant', department: 'Administrative Office' },
        { name: 'S. Murugan', designation: 'Clerk', department: 'Administrative Office' },
        { name: 'P. Rajagopal', designation: 'Lab Assistant', department: 'Computer Science' },
        { name: 'K. Saravanan', designation: 'Library Assistant', department: 'Library' }
    ],
    departments: {
        english: {
            name: 'English',
            icon: 'fa-language',
            about: 'The Department of English at Sethupathy Government Arts College is dedicated to providing quality education in English language and literature. We offer comprehensive programs that explore classical and modern English literature, linguistics, and communication skills.',
            vision: 'To be a center of excellence in English language and literature, fostering critical thinking and effective communication.',
            mission: 'To provide quality education in English and develop language skills for global competitiveness.',
            hod: { name: 'Dr. K. Jeyamurugan', designation: 'Head of Department, Assistant Professor', qualification: 'M.A., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. K. Jeyamurugan', designation: 'Head of Department, Assistant Professor', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Barakkathu Nisha.T.A', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., SET, NET' },
                { name: 'Dr. Suthanthira Jothi.D', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., B.Ed.' },
                { name: 'Dr. Nagarajan.K', designation: 'Guest Lecturer', qualification: 'M.A., M.Ed., M.Phil.' },
                { name: 'Dr. Martin Prabahar.J', designation: 'Guest Lecturer', qualification: 'M.A., B.Ed., M.Phil., Ph.D.' },
                { name: 'Dr. Raihana Barvin.A', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Prema Latha.M', designation: 'Guest Lecturer', qualification: 'M.A., M.Ed., Ph.D.' },
                { name: 'Dr. Seeni Sulthan Ibrahim.M', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., B.Ed., Ph.D.' },
                { name: 'Dr. John Sujith.A', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., B.Ed., Ph.D.' },
                { name: 'Dr. Mohana Murugan.S', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Maheshwari.R', designation: 'Guest Lecturer', qualification: 'M.A., B.Ed., M.Phil., Ph.D.' },
                { name: 'Saratha.S', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil.' },
                { name: 'Dr. Rajam.G', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., B.Ed.' },
                { name: 'Dr. Lakshmi.T', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil.' },
                { name: 'Dr. Prabhakar.S', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., B.Ed., Ph.D.' },
                { name: 'Dr. Manimannan.V', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., B.Ed.' },
                { name: 'Dr. Kumar.A', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., MSW., B.Ed., Ph.D.' }
            ],
            courses: [
                { name: 'B.A. English', type: 'Under Graduate' },
                { name: 'M.A. English', type: 'Post Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        tamil: {
            name: 'Tamil',
            icon: 'fa-language',
            about: 'The Department of Tamil at Sethupathy Government Arts College is dedicated to preserving and promoting the rich heritage of Tamil language and literature. We offer comprehensive programs that explore classical and modern Tamil literature, linguistics, and cultural studies.',
            vision: 'To be a center of excellence in Tamil language, literature, and cultural studies.',
            mission: 'To provide quality education in Tamil and preserve the rich linguistic and cultural heritage.',
            hod: { name: 'Dr. M. Senthamarai', designation: 'Head of Department, Assistant Professor', qualification: 'M.A., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. M. Senthamarai', designation: 'Head of Department, Assistant Professor', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Muthuraman.S', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil.' },
                { name: 'Dr. Poornayogarani.K', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Ramamurthy.S', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Paul Murugan.V', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Rajasekar.A', designation: 'Guest Lecturer', qualification: 'M.A., B.Ed., M.Phil., Ph.D.' },
                { name: 'Dr. Nagapandi.M', designation: 'Guest Lecturer', qualification: 'M.A., B.Ed., M.Phil., Ph.D., PGDSA.' },
                { name: 'Dr. Alagumurugan.M', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Dr. Syed Kasim.M', designation: 'Guest Lecturer', qualification: 'M.A., M.Phil., Ph.D.' },
                { name: 'Govindaraju.T', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil.' },
                { name: 'Murugavel.U', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., DISM, Ph.D.' },
                { name: 'Baskaran.M', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil., B.Ed.' },
                { name: 'Sundari.K', designation: 'Guest Lecturer (2nd Shift)', qualification: 'M.A., M.Phil.' }
            ],
            courses: [
                { name: 'B.A. Tamil', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        commerce: {
            name: 'Commerce',
            icon: 'fa-calculator',
            about: 'The Department of Commerce provides quality education in accounting, finance, and business studies.',
            vision: 'To be a center of excellence in commerce education.',
            mission: 'To produce competent professionals in the field of commerce and business.',
            hod: { name: 'Dr. K. Rajagopal', designation: 'Associate Professor & Head', qualification: 'M.Com., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. K. Rajagopal', designation: 'Associate Professor & Head', qualification: 'M.Com., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Com.', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        computer: {
            name: 'Computer Science',
            icon: 'fa-laptop',
            about: 'The Department of Computer Science offers comprehensive programs in programming, software development, and IT.',
            vision: 'To be a center of excellence in computer science and information technology.',
            mission: 'To provide quality education in computing and produce skilled IT professionals.',
            hod: { name: 'Dr. A. Kumar', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. A. Kumar', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
                { name: 'Ms. R. Lakshmi', designation: 'Assistant Professor', qualification: 'M.Sc., M.Phil.' }
            ],
            courses: [
                { name: 'B.Sc. Computer Science', type: 'Under Graduate' },
                { name: 'M.Sc. Computer Science', type: 'Post Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        mathematics: {
            name: 'Mathematics',
            icon: 'fa-square-root-alt',
            about: 'The Department of Mathematics provides strong foundation in mathematical concepts and problem-solving skills.',
            vision: 'To be a center of excellence in mathematics education and research.',
            mission: 'To provide quality mathematics education and foster analytical thinking.',
            hod: { name: 'Dr. P. Venkatesan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. P. Venkatesan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Mathematics', type: 'Under Graduate' },
                { name: 'M.Sc. Mathematics', type: 'Post Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        physics: {
            name: 'Physics',
            icon: 'fa-atom',
            about: 'The Department of Physics offers comprehensive programs in fundamental and applied physics.',
            vision: 'To be a center of excellence in physics education and research.',
            mission: 'To provide quality physics education and promote scientific research.',
            hod: { name: 'Dr. S. Narayanan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. S. Narayanan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Physics', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        chemistry: {
            name: 'Chemistry',
            icon: 'fa-flask',
            about: 'The Department of Chemistry provides education in organic, inorganic, and physical chemistry.',
            vision: 'To be a center of excellence in chemistry education and research.',
            mission: 'To provide quality chemistry education and promote chemical research.',
            hod: { name: 'Dr. R. Sethuraman', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. R. Sethuraman', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Chemistry', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        botany: {
            name: 'Botany',
            icon: 'fa-leaf',
            about: 'The Department of Botany provides education in plant biology and biodiversity.',
            vision: 'To be a center of excellence in botanical sciences.',
            mission: 'To provide quality education in botany and promote environmental awareness.',
            hod: { name: 'Dr. M. Kannan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. M. Kannan', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Botany', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        zoology: {
            name: 'Zoology',
            icon: 'fa-paw',
            about: 'The Department of Zoology provides education in animal biology and wildlife studies.',
            vision: 'To be a center of excellence in zoological sciences.',
            mission: 'To provide quality education in zoology and promote wildlife conservation.',
            hod: { name: 'Dr. K. Gopal', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. K. Gopal', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Zoology', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        economics: {
            name: 'Economics',
            icon: 'fa-chart-line',
            about: 'The Department of Economics provides education in economic theory and applied economics.',
            vision: 'To be a center of excellence in economics education and research.',
            mission: 'To provide quality economics education and promote economic development.',
            hod: { name: 'Dr. T. Raman', designation: 'Associate Professor & Head', qualification: 'M.A., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. T. Raman', designation: 'Associate Professor & Head', qualification: 'M.A., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.A. Economics', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        commerceca: {
            name: 'Commerce CA',
            icon: 'fa-calculator',
            about: 'The Department of Commerce with Computer Applications provides education in commerce with emphasis on computer applications.',
            vision: 'To be a center of excellence in commerce education with computer applications.',
            mission: 'To produce skilled professionals in commerce and computer applications.',
            hod: { name: 'Dr. R. Baskaran', designation: 'Associate Professor & Head', qualification: 'M.Com., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. R. Baskaran', designation: 'Associate Professor & Head', qualification: 'M.Com., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Com. CA', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        },
        marinebiology: {
            name: 'Marine Biology',
            icon: 'fa-water',
            about: 'The Department of Marine Biology provides education in marine science and ocean studies.',
            vision: 'To be a center of excellence in marine biology education and research.',
            mission: 'To provide quality education in marine biology and promote marine conservation.',
            hod: { name: 'Dr. M. Nehru', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' },
            faculty: [
                { name: 'Dr. M. Nehru', designation: 'Associate Professor & Head', qualification: 'M.Sc., M.Phil., Ph.D.' }
            ],
            courses: [
                { name: 'B.Sc. Marine Biology', type: 'Under Graduate' }
            ],
            activities: [],
            achievements: [],
            econtent: [],
            gallery: []
        }
    }
};

function saveSiteData(data) {
    localStorage.setItem('sgac_site_data', JSON.stringify(data));
}

function loadSiteData() {
    const saved = localStorage.getItem('sgac_site_data');
    if (saved) {
        const parsed = JSON.parse(saved);
        if (!parsed.departments) {
            parsed.departments = SiteData.departments;
        }
        return parsed;
    }
    return SiteData;
}

function getDepartmentData(deptKey) {
    const data = loadSiteData();
    return data.departments && data.departments[deptKey] ? data.departments[deptKey] : null;
}
