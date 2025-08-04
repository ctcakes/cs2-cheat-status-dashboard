<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

require_once 'config.php';
require_once 'functions.php';

$action = $_GET['action'] ?? 'all';

switch ($action) {
    case 'all':
        $result = getAllLatestNews();
        break;
    case 'nixware':
        $result = getNixwareLatestNews();
        break;
    case 'neverlose':
        $result = getNeverkoseLatestNews();
        break;
    case 'fatality':
        $result = getFatalityLatestNews();
        break;
    case 'memesense':
        $result = getMemesenseLatestNews();
        break;
    case 'plaguecheat':
        $result = getPlaguecheateLatestNews();
        break;
    case 'cs2':
        $result = getCS2LatestNews();
        break;
    case 'summary':
        $result = getUpdateSummary();
        break;
    default:
        $result = ['error' => 'Invalid action'];
        break;
}

echo json_encode($result, JSON_UNESCAPED_UNICODE);
?>