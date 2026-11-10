<?php
/**
 * Contact / chat endpoint -> emails messages to the site owner.
 *
 *   POST /api/contact.php   fields: name, email, message, topic?, page?, website (honeypot), t (ms timestamp)
 *   -> {"ok": true} | {"ok": false, "error": "..."}
 *
 * Spam protection: honeypot field, minimum fill time, per-visitor rate limit (hashed IP),
 * strict header sanitising. Every message is also appended to data/messages.log as a backup.
 */

const TO_EMAIL   = 'rnamocotdev@gmail.com';          // where messages are delivered
const FROM_EMAIL = 'noreply@rnamocotdev.com';         // sender on your domain (better deliverability)
const SITE_NAME  = 'rnamocotdev.com';
const MAX_PER_HOUR = 5;

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');

function out($ok, $error = null, $code = 200) {
    http_response_code($code);
    echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    out(false, 'Method not allowed', 405);
}

$in = $_POST;
if (empty($in)) {
    $raw = json_decode(file_get_contents('php://input'), true);
    $in = is_array($raw) ? $raw : [];
}

$clean = function ($v, $max) {
    $v = trim((string) $v);
    $v = preg_replace('/[\r\n\t]+/', ' ', $v);      // no header injection
    return mb_substr($v, 0, $max);
};

$name    = $clean($in['name'] ?? '', 80);
$email   = $clean($in['email'] ?? '', 120);
$topic   = $clean($in['topic'] ?? '', 120);
$budget  = $clean($in['budget'] ?? '', 60);
$page    = $clean($in['page'] ?? '', 200);
$message = mb_substr(trim((string) ($in['message'] ?? '')), 0, 5000);
$honey   = trim((string) ($in['website'] ?? ''));
$t       = (int) ($in['t'] ?? 0);

// bots: honeypot filled, or submitted impossibly fast -> pretend success, send nothing
if ($honey !== '' || ($t > 0 && (microtime(true) * 1000 - $t) < 2500)) {
    out(true);
}
if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    out(false, 'Please add your name, a valid email and a message.', 422);
}

// rate limit per visitor (IP hashed with a server salt, never stored in plain text)
$dir = __DIR__ . '/data';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
$saltFile = $dir . '/salt.txt';
if (!file_exists($saltFile)) { file_put_contents($saltFile, bin2hex(random_bytes(32)), LOCK_EX); }
$salt = trim((string) @file_get_contents($saltFile));
$ip = trim(explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '')[0]);
$who = substr(hash('sha256', $salt . '|' . $ip), 0, 20);

$rateFile = $dir . '/contact-rate.json';
$fp = fopen($rateFile, 'c+');
flock($fp, LOCK_EX);
$rate = json_decode(stream_get_contents($fp) ?: '{}', true) ?: [];
$now = time();
foreach ($rate as $k => $times) {
    $rate[$k] = array_values(array_filter($times, fn($x) => $x > $now - 3600));
    if (!$rate[$k]) unset($rate[$k]);
}
if (count($rate[$who] ?? []) >= MAX_PER_HOUR) {
    flock($fp, LOCK_UN); fclose($fp);
    out(false, 'Too many messages. Please email ' . TO_EMAIL . ' directly.', 429);
}
$rate[$who][] = $now;
ftruncate($fp, 0); rewind($fp); fwrite($fp, json_encode($rate)); fflush($fp);
flock($fp, LOCK_UN); fclose($fp);

// compose
$subject = 'New message from ' . $name . ' (' . SITE_NAME . ')';
$body  = "You have a new message from your website.\n\n";
$body .= "Name:    {$name}\n";
$body .= "Email:   {$email}\n";
if ($topic)  $body .= "Topic:   {$topic}\n";
if ($budget) $body .= "Budget:  {$budget}\n";
if ($page)   $body .= "Page:    {$page}\n";
$body .= "Time:    " . gmdate('Y-m-d H:i') . " UTC\n";
$body .= "\n----------------------------------------\n\n{$message}\n\n";
$body .= "----------------------------------------\nReply directly to this email to answer {$name}.\n";

$headers = [
    'From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
];

// backup copy (data/ is blocked from the web)
@file_put_contents($dir . '/messages.log', "==== " . gmdate('c') . "\n" . $body . "\n", FILE_APPEND | LOCK_EX);

if (is_file($dir . '/.dryrun')) {   // local testing: create api/data/.dryrun to skip sending
    out(true);
}

$sent = @mail(TO_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);
if (!$sent) {
    out(false, 'Message could not be sent right now. Please email ' . TO_EMAIL . ' directly.', 500);
}
out(true);
