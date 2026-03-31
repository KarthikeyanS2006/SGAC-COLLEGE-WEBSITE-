<?php
// API to save data from admin panel
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

include 'db-config.php';

// Get request method and data
$method = $_SERVER['REQUEST_METHOD'];
$data = json_decode(file_get_contents('php://input'), true);

try {
    switch($data['type']) {
        case 'news':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_news (title, date, icon) VALUES (?, ?, ?)");
                $stmt->execute([$data['title'], $data['date'], $data['icon']]);
                echo json_encode(array('success' => true, 'id' => $pdo->lastInsertId()));
            } elseif ($method == 'DELETE') {
                $stmt = $pdo->prepare("DELETE FROM sgac_news WHERE id = ?");
                $stmt->execute([$data['id']]);
                echo json_encode(array('success' => true));
            }
            break;
            
        case 'events':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_events (title, date, icon) VALUES (?, ?, ?)");
                $stmt->execute([$data['title'], $data['date'], $data['icon']]);
                echo json_encode(array('success' => true, 'id' => $pdo->lastInsertId()));
            } elseif ($method == 'DELETE') {
                $stmt = $pdo->prepare("DELETE FROM sgac_events WHERE id = ?");
                $stmt->execute([$data['id']]);
                echo json_encode(array('success' => true));
            }
            break;
            
        case 'downloads':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_downloads (title, link, icon) VALUES (?, ?, ?)");
                $stmt->execute([$data['title'], $data['link'], $data['icon']]);
                echo json_encode(array('success' => true, 'id' => $pdo->lastInsertId()));
            } elseif ($method == 'DELETE') {
                $stmt = $pdo->prepare("DELETE FROM sgac_downloads WHERE id = ?");
                $stmt->execute([$data['id']]);
                echo json_encode(array('success' => true));
            }
            break;
            
        case 'announcements':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_announcements (text) VALUES (?)");
                $stmt->execute([$data['text']]);
                echo json_encode(array('success' => true, 'id' => $pdo->lastInsertId()));
            } elseif ($method == 'DELETE') {
                $stmt = $pdo->prepare("DELETE FROM sgac_announcements WHERE id = ?");
                $stmt->execute([$data['id']]);
                echo json_encode(array('success' => true));
            }
            break;
            
        case 'carousel':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_carousel (img, alt) VALUES (?, ?)");
                $stmt->execute([$data['img'], $data['alt']]);
                echo json_encode(array('success' => true, 'id' => $pdo->lastInsertId()));
            } elseif ($method == 'DELETE') {
                $stmt = $pdo->prepare("DELETE FROM sgac_carousel WHERE id = ?");
                $stmt->execute([$data['id']]);
                echo json_encode(array('success' => true));
            }
            break;
            
        case 'department':
            if ($method == 'POST' || $method == 'PUT') {
                $stmt = $pdo->prepare("INSERT INTO sgac_departments (dept_key, name, about, vision, mission, hod_name, hod_designation, hod_qualification, gallery_json) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) 
                    ON DUPLICATE KEY UPDATE name=VALUES(name), about=VALUES(about), vision=VALUES(vision), mission=VALUES(mission), 
                    hod_name=VALUES(hod_name), hod_designation=VALUES(hod_designation), hod_qualification=VALUES(hod_qualification), gallery_json=VALUES(gallery_json)");
                $stmt->execute([
                    $data['dept_key'], $data['name'], $data['about'], $data['vision'], $data['mission'],
                    $data['hod_name'], $data['hod_designation'], $data['hod_qualification'], 
                    json_encode($data['gallery'])
                ]);
                echo json_encode(array('success' => true));
            }
            break;
            
        default:
            echo json_encode(array('error' => 'Invalid type'));
    }
} catch(PDOException $e) {
    http_response_code(500);
    echo json_encode(array('error' => $e->getMessage()));
}
