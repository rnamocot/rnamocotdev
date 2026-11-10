<?php
/**
 * Privacy-friendly visitor counter for a static site.
 *
 *   GET  /api/visits.php            -> {"total": 1234}            (read only)
 *   POST /api/visits.php            -> counts this visitor once per day, returns {"total": n}
 *
 * - No cookies, no third parties.
 * - IP addresses are never stored: only a salted SHA-256 hash for the current day,
 *   and that list is discarded when the day changes.
 * - Data lives in /api/data/ (blocked from the web by .htaccess).
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

$dir = __DIR__ . '/data';
if (!is_dir($dir)) {
    @mkdir($dir, 0750, true);
}
$file = $dir . '/visits.json';
$saltFile = $dir . '/salt.txt';

if (!file_exists($saltFile)) {
    file_put_contents($saltFile, bin2hex(random_bytes(32)), LOCK_EX);
}
$salt = trim((string) @file_get_contents($saltFile));

$fp = fopen($file, 'c+');
if (!$fp) {
    http_response_code(500);
    echo json_encode(['error' => 'storage unavailable']);
    exit;
}
flock($fp, LOCK_EX);
$raw = stream_get_contents($fp);
$data = $raw ? json_decode($raw, true) : null;
if (!is_array($data)) {
    $data = ['total' => 0, 'day' => '', 'seen' => []];
}

$today = gmdate('Y-m-d');
if ($data['day'] !== $today) {          // new day: forget yesterday's hashes
    $data['day'] = $today;
    $data['seen'] = [];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
    $isBot = $ua === '' || preg_match('/bot|crawl|spider|slurp|preview|monitor|headless|lighthouse|curl|wget|python|php/i', $ua);
    if (!$isBot) {
        $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
        $ip = trim(explode(',', $ip)[0]);
        $id = substr(hash('sha256', $salt . '|' . $today . '|' . $ip . '|' . $ua), 0, 20);
        if (!isset($data['seen'][$id])) {
            $data['seen'][$id] = 1;
            $data['total']++;
        }
    }
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data));
    fflush($fp);
}

flock($fp, LOCK_UN);
fclose($fp);

echo json_encode(['total' => (int) $data['total']]);
