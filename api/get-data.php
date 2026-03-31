<?php
// API to get all site data - returns JSON
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'db-config.php';

try {
    $data = array();
    
    // Get News
    $stmt = $pdo->query("SELECT title, date, icon FROM sgac_news ORDER BY id DESC");
    $data['news'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get Events
    $stmt = $pdo->query("SELECT title, date, icon FROM sgac_events ORDER BY id DESC");
    $data['events'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get Downloads
    $stmt = $pdo->query("SELECT title, link, icon FROM sgac_downloads ORDER BY id DESC");
    $data['downloads'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get Announcements
    $stmt = $pdo->query("SELECT text FROM sgac_announcements ORDER BY id DESC");
    $data['announcements'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get Carousel
    $stmt = $pdo->query("SELECT img, alt FROM sgac_carousel ORDER BY id ASC");
    $data['carousel'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get Departments
    $stmt = $pdo->query("SELECT dept_key, name, about, vision, mission, hod_name, hod_designation, hod_qualification, gallery_json FROM sgac_departments");
    $departments = $stmt->fetchAll(PDO::FETCH_ASSOC);
    $data['departments'] = array();
    foreach ($departments as $dept) {
        $data['departments'][$dept['dept_key']] = array(
            'name' => $dept['name'],
            'about' => $dept['about'],
            'vision' => $dept['vision'],
            'mission' => $dept['mission'],
            'hod' => array(
                'name' => $dept['hod_name'],
                'designation' => $dept['hod_designation'],
                'qualification' => $dept['hod_qualification']
            ),
            'gallery' => $dept['gallery_json'] ? json_decode($dept['gallery_json'], true) : array()
        );
    }
    
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(array('error' => $e->getMessage()));
}
