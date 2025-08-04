<?php

function makeRequest($url, $options = []) {
    $ch = curl_init();
    
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => REQUEST_TIMEOUT,
        CURLOPT_USERAGENT => USER_AGENT,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_ENCODING => '',  // Enable all supported encodings
        CURLOPT_HTTPHEADER => $options['headers'] ?? [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8'
        ]
    ]);
    

    
    // 设置Cookie
    if (isset($options['cookie'])) {
        curl_setopt($ch, CURLOPT_COOKIE, $options['cookie']);
    }
    
    if (isset($options['post_data'])) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $options['post_data']);
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    
    if ($response === false) {
        error_log("cURL Error for $url: $curlError");
        return ['error' => "连接失败: $curlError"];
    }
    
    if ($httpCode !== 200) {
        error_log("HTTP Error for $url: HTTP $httpCode");
        return ['error' => "HTTP错误: $httpCode"];
    }
    
    return $response;
}

function getNixwareLatestNews() {
    $url = 'https://nixware.cc/forums/news/?prefix_id=10';
    
    $options = [
        'headers' => [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language: en-US,en;q=0.5',
            'Accept-Encoding: gzip, deflate',
            'DNT: 1',
            'Connection: keep-alive',
            'Upgrade-Insecure-Requests: 1',
            'User-Agent: ' . USER_AGENT
        ]
    ];
    
    $html = makeRequest($url, $options);
    if (is_array($html) && isset($html['error'])) {
        return ['success' => false, 'error' => 'Nixware: ' . $html['error']];
    }
    if (!$html) {
        return ['success' => false, 'error' => '无法连接到Nixware'];
    }
    
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $xpath = new DOMXPath($dom);
    
    $threads = $xpath->query('//div[contains(@class, "structItem--thread")]');
    
    if ($threads->length === 0) {
        return ['success' => false, 'error' => '未找到相关内容'];
    }
    
    $news = [];
    $latestDate = null;
    
    foreach ($threads as $thread) {
        $titleElement = $xpath->query('.//div[contains(@class, "structItem-title")]//a', $thread)->item(0);
        $timeElement = $xpath->query('.//time', $thread)->item(0);
        
        if ($titleElement && $timeElement) {
            $title = trim($titleElement->textContent);
            $href = '';
            if ($titleElement instanceof DOMElement) {
                $href = $titleElement->getAttribute('href');
            }
            $link = 'https://nixware.cc' . $href;
            
            $datetime = null;
            if ($timeElement instanceof DOMElement) {
                $datetime = $timeElement->getAttribute('datetime');
            }
            
            if ($datetime) {
                $date = date('Y-m-d', strtotime($datetime));
                if (!$latestDate || $date > $latestDate) {
                    $latestDate = $date;
                }
                
                $news[] = [
                    'title' => $title,
                    'link' => $link,
                    'date' => $date
                ];
            }
        }
    }
    
    return [
        'success' => true,
        'count' => count($news),
        'latest_date' => $latestDate,
        'news' => $news
    ];
}

function getNeverkoseLatestNews() {
    $url = 'https://forum.neverlose.cc/c/news/31/l/latest.json';
    
    $response = makeRequest($url, [
        'headers' => [
            'Accept: application/json',
            'User-Agent: ' . USER_AGENT
        ]
    ]);
    
    if (is_array($response) && isset($response['error'])) {
        return ['success' => false, 'error' => 'Neverlose: ' . $response['error']];
    }
    if (!$response) {
        return ['success' => false, 'error' => '无法连接到Neverlose'];
    }
    
    $data = json_decode($response, true);
    if (!$data || !isset($data['topic_list']['topics'])) {
        return ['success' => false, 'error' => '解析响应失败'];
    }
    
    $topics = $data['topic_list']['topics'];
    $news = [];
    $latestDate = null;
    
    foreach ($topics as $topic) {
        if (isset($topic['title']) && isset($topic['id']) && isset($topic['created_at'])) {
            $title = $topic['title'];
            $link = 'https://forum.neverlose.cc/t/' . $topic['id'];
            $date = date('Y-m-d', strtotime($topic['created_at']));
            
            if (!$latestDate || $date > $latestDate) {
                $latestDate = $date;
            }
            
            $news[] = [
                'title' => $title,
                'link' => $link,
                'date' => $date
            ];
        }
    }
    
    return [
        'success' => true,
        'count' => count($news),
        'latest_date' => $latestDate,
        'news' => $news
    ];
}

function getFatalityLatestNews() {
    $url = 'https://fatality.win/forums/updates.44/';
    
    // Check if cookies are available
    if (!defined('FATALITY_COOKIES') || empty(FATALITY_COOKIES)) {
        return ['success' => false, 'error' => 'Fatality: 未配置cookies'];
    }
    
    $html = makeRequest($url, [
        'headers' => [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding: gzip, deflate',
            'DNT: 1',
            'Connection: keep-alive',
            'Upgrade-Insecure-Requests: 1',
            'Sec-Ch-Ua: "Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            'Sec-Ch-Ua-Arch: "x86"',
            'Sec-Ch-Ua-Bitness: "64"',
            'Sec-Ch-Ua-Full-Version: "138.0.3351.121"',
            'Sec-Ch-Ua-Mobile: ?0',
            'Sec-Ch-Ua-Model: ""',
            'Sec-Ch-Ua-Platform: "Windows"',
            'Sec-Ch-Ua-Platform-Version: "19.0.0"',
            'Sec-Fetch-Dest: empty',
            'Sec-Fetch-Mode: navigate',
            'Sec-Fetch-Site: same-origin',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
        ],
        'cookie' => FATALITY_COOKIES
    ]);
    if (is_array($html) && isset($html['error'])) {
        return ['success' => false, 'error' => 'Fatality: ' . $html['error']];
    }
    if (!$html) {
        return ['success' => false, 'error' => '无法连接到Fatality'];
    }
    
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $xpath = new DOMXPath($dom);
    
    $threads = $xpath->query('//div[contains(@class, "structItem--thread")]');
    
    if ($threads->length === 0) {
        return ['success' => false, 'error' => '未找到相关内容'];
    }
    
    $news = [];
    $latestDate = null;
    
    foreach ($threads as $thread) {
        $titleElement = $xpath->query('.//a[contains(@class, "structItem-title")]', $thread)->item(0);
        $timeElement = $xpath->query('.//time', $thread)->item(0);
        
        if ($titleElement && $timeElement) {
            $title = trim($titleElement->textContent);
            $link = 'https://fatality.win' . $titleElement->getAttribute('href');
            $datetime = $timeElement->getAttribute('datetime');
            
            if ($datetime) {
                $date = date('Y-m-d', strtotime($datetime));
                if (!$latestDate || $date > $latestDate) {
                    $latestDate = $date;
                }
                
                $news[] = [
                    'title' => $title,
                    'link' => $link,
                    'date' => $date
                ];
            }
        }
    }
    
    return [
        'success' => true,
        'count' => count($news),
        'latest_date' => $latestDate,
        'news' => $news
    ];
}

function getMemesenseLatestNews() {
    $url = 'https://api.memesense.gg/forums/26/threads';
    
    $response = makeRequest($url, [
        'headers' => [
            'Accept: application/json',
            'User-Agent: ' . USER_AGENT
        ]
    ]);
    
    if (is_array($response) && isset($response['error'])) {
        return ['success' => false, 'error' => 'Memesense: ' . $response['error']];
    }
    if (!$response) {
        return ['success' => false, 'error' => '无法连接到Memesense'];
    }
    
    $data = json_decode($response, true);
    if (!$data || !isset($data['threads'])) {
        return ['success' => false, 'error' => '响应中未找到threads数据'];
    }
    
    $threads = $data['threads'];
    $news = [];
    $latestDate = null;
    
    foreach ($threads as $thread) {
        if (isset($thread['name']) && isset($thread['id']) && isset($thread['created_at'])) {
            $title = $thread['name'];
            $link = 'https://memesense.gg/threads/' . $thread['id'];
            $date = date('Y-m-d', strtotime($thread['created_at']));
            
            if (!$latestDate || $date > $latestDate) {
                $latestDate = $date;
            }
            
            $news[] = [
                'title' => $title,
                'link' => $link,
                'date' => $date
            ];
        }
    }
    
    return [
        'success' => true,
        'count' => count($news),
        'latest_date' => $latestDate,
        'news' => $news
    ];
}

function getPlaguecheateLatestNews() {
    return [
        'success' => false,
        'error' => '由于瘟疫官网使用的Cloudflare防护严格，暂时无法获取。B站CTCAKE 敬请期待。'
    ];
}

function getCS2LatestNews() {
    $token = STEAM_ACCESS_TOKEN;
    
    if ($token) {
        $url = "https://api.steampowered.com/IAssetSetPublishingService/UpdatePublishTime/v1/?access_token={$token}&appid=730";
        
        $response = makeRequest($url, [
            'headers' => [
                'Content-Type: application/x-www-form-urlencoded',
                'Origin: https://steamcommunity.com',
                'Referer: https://steamcommunity.com/'
            ],
            'post_data' => 'appid=730'
        ]);
        
        if (is_array($response) && isset($response['error'])) {
            // 主API失败，继续使用备用API
            error_log('CS2主API失败: ' . $response['error']);
        }
    }
    
    // 使用备用Steam新闻API
    $newsUrl = 'https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=730&count=5&maxlength=300&format=json';
    $newsResponse = makeRequest($newsUrl);
    
    if (is_array($newsResponse) && isset($newsResponse['error'])) {
        return ['success' => false, 'error' => 'CS2: ' . $newsResponse['error']];
    }
    if (!$newsResponse) {
        return ['success' => false, 'error' => '无法获取CS2更新信息'];
    }
    
    $newsData = json_decode($newsResponse, true);
    if (!$newsData || !isset($newsData['appnews']['newsitems'])) {
        return ['success' => false, 'error' => '解析CS2新闻失败'];
    }
    
    $newsItems = $newsData['appnews']['newsitems'];
    $news = [];
    $latestDate = null;
    
    foreach ($newsItems as $item) {
        if (isset($item['title']) && isset($item['url']) && isset($item['date'])) {
            $title = $item['title'];
            $link = $item['url'];
            $date = date('Y-m-d', $item['date']);
            
            if (!$latestDate || $date > $latestDate) {
                $latestDate = $date;
            }
            
            $news[] = [
                'title' => $title,
                'link' => $link,
                'date' => $date
            ];
        }
    }
    
    return [
        'success' => true,
        'count' => count($news),
        'latest_date' => $latestDate,
        'news' => $news
    ];
}

function getAllLatestNews() {
    $results = [];
    $totalCount = 0;
    
    // 获取各个cheat的消息
    $sources = [
        'nixware' => 'getNixwareLatestNews',
        'neverlose' => 'getNeverkoseLatestNews',
        'fatality' => 'getFatalityLatestNews',
        'memesense' => 'getMemesenseLatestNews',
        'plaguecheat' => 'getPlaguecheateLatestNews',
        'cs2' => 'getCS2LatestNews'
    ];
    
    foreach ($sources as $source => $function) {
        $result = $function();
        $results[$source] = $result;
        if ($result['success'] && isset($result['count'])) {
            $totalCount += $result['count'];
        }
    }
    
    return [
        'success' => true,
        'total_count' => $totalCount,
        'results' => $results
    ];
}

function getUpdateSummary() {
    $allNews = getAllLatestNews();
    
    if (!$allNews['success']) {
        return ['success' => false, 'error' => '获取数据失败'];
    }
    
    $results = $allNews['results'];
    $cs2Data = $results['cs2'];
    
    if (!$cs2Data['success'] || !isset($cs2Data['latest_date'])) {
        return [
            'success' => false,
            'error' => '无法获取CS2更新日期',
            'results' => $results
        ];
    }
    
    $cs2Date = $cs2Data['latest_date'];
    $summary = [];
    
    $cheats = ['nixware', 'neverlose', 'fatality', 'memesense', 'plaguecheat'];
    
    foreach ($cheats as $cheat) {
        $cheatData = $results[$cheat];
        
        if ($cheatData['success'] && isset($cheatData['latest_date'])) {
            $cheatDate = $cheatData['latest_date'];
            $status = (strtotime($cheatDate) >= strtotime($cs2Date)) ? 'available' : 'unavailable';
            
            $summary[] = [
                'name' => ucfirst($cheat),
                'date' => $cheatDate,
                'status' => $status
            ];
        } else {
            $summary[] = [
                'name' => ucfirst($cheat),
                'date' => null,
                'status' => 'unknown',
                'error' => $cheatData['error'] ?? '获取失败'
            ];
        }
    }
    
    // 按照可用>不可用>未知的顺序排序
    usort($summary, function($a, $b) {
        $statusOrder = ['available' => 1, 'unavailable' => 2, 'unknown' => 3];
        $aOrder = $statusOrder[$a['status']] ?? 4;
        $bOrder = $statusOrder[$b['status']] ?? 4;
        
        if ($aOrder === $bOrder) {
            // 如果状态相同，按名称排序
            return strcmp($a['name'], $b['name']);
        }
        
        return $aOrder - $bOrder;
    });
    
    return [
        'success' => true,
        'cs2_date' => $cs2Date,
        'summary' => $summary,
        'results' => $results
    ];
}

?>