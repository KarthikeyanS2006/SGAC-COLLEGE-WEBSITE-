<?php
// Database Configuration - Upload this to your cPanel hosting
$db_host = 'localhost';
$db_name = 'sgacrmde_db';
$db_user = 'sgacrmde_admin';
$db_pass = 'SGAC2025@';

try {
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8", $db_user, $db_pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

// Create tables if not exist
$sql = "
CREATE TABLE IF NOT EXISTS sgac_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date VARCHAR(50),
    icon VARCHAR(50) DEFAULT 'fa-bullhorn',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sgac_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date VARCHAR(50),
    icon VARCHAR(50) DEFAULT 'fa-calendar',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sgac_downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link VARCHAR(500),
    icon VARCHAR(50) DEFAULT 'fa-download',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sgac_announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sgac_carousel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    img VARCHAR(500) NOT NULL,
    alt VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sgac_departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dept_key VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    about TEXT,
    vision TEXT,
    mission TEXT,
    hod_name VARCHAR(100),
    hod_designation VARCHAR(100),
    hod_qualification VARCHAR(100),
    gallery_json TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
";

$pdo->exec($sql);

// Initialize with default data if empty
$stmt = $pdo->query("SELECT COUNT(*) FROM sgac_news");
if ($stmt->fetchColumn() == 0) {
    $initSql = "
    INSERT INTO sgac_news (title, date, icon) VALUES 
    ('International Virtual Conference on Innovation and Intelligence in Computing System', 'May 02, 2022', 'fa-university'),
    ('E-Workshop on Writing Skills Organised by English Department', 'July 03 & July 05', 'fas fa-book-open'),
    ('E-Quiz Organised By Computer Science Department', 'May 21 & May 22', 'fa-laptop'),
    ('E-Quiz Organised By National Service Scheme Club', 'May 26 & May 27', 'fas fa-running');
    
    INSERT INTO sgac_events (title, date, icon) VALUES 
    ('Annual Day Celebration', 'March 15, 2025', 'fa-calendar'),
    ('Sports Day Events', 'February 28, 2025', 'fa-trophy');
    
    INSERT INTO sgac_downloads (title, link, icon) VALUES 
    ('Bonafide Certificate', 'Documents/Forms/Bonafide.pdf', 'fa-download'),
    ('Attendance Certificate', 'Documents/Forms/Attendance.pdf', 'fa-download'),
    ('Academic Calendar 2024-2025', 'Documents/calendar/2024-2025 calendar.pdf', 'fa-download');
    
    INSERT INTO sgac_carousel (img, alt) VALUES 
    ('https://sgacrmd.edu.in/assets/carousel/7-01-2026/1.jpg', 'College Campus'),
    ('https://sgacrmd.edu.in/assets/carousel/7-01-2026/2.jpg', 'Laboratory'),
    ('https://sgacrmd.edu.in/assets/carousel/7-01-2026/3.jpg', 'Library');
    ";
    $pdo->exec($initSql);
}

echo "Database initialized successfully!";
