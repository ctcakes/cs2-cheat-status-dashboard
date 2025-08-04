import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timezone
from collections import defaultdict

def get_nixware_latest_news():
    """获取Nixware上次更新的消息"""
    url = "https://nixware.cc/forums/news/?prefix_id=10"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 按日期分组消息
        news_by_date = defaultdict(list)
        
        # 查找主题容器
        topic_containers = soup.find_all('div', class_='structItem')
        
        for container in topic_containers:
            try:
                # 查找标题链接
                title_link = container.find('a', {'data-tp-primary': 'on'})
                if not title_link:
                    continue
                    
                title = title_link.get_text(strip=True)
                
                # 只获取包含"Update"关键字的帖子
                if 'Update' not in title:
                    continue
                
                link = title_link.get('href', '')
                if link and not link.startswith('http'):
                    link = 'https://nixware.cc' + link
                
                # 获取作者
                author = '未知'
                author_link = container.find('a', class_='username')
                if author_link:
                    author = author_link.get_text(strip=True)
                
                # 获取时间信息
                date_obj = datetime.now()  # 默认当前本地时间
                time_elem = container.find('time')
                if time_elem:
                    datetime_attr = time_elem.get('datetime')
                    if datetime_attr:
                        try:
                            # 解析UTC时间并转换为本地时间
                            utc_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                            date_obj = utc_date.astimezone()
                        except:
                            pass
                
                date_key = date_obj.strftime('%Y-%m-%d')
                
                # 获取回复数和查看数
                replies = '0'
                views = '0'
                
                # 查找统计信息
                stats = container.find_all('dd')
                if len(stats) >= 2:
                    replies = stats[0].get_text(strip=True)
                    views = stats[1].get_text(strip=True)
                
                news_item = {
                    'title': title,
                    'link': link,
                    'author': author,
                    'date': date_obj.isoformat(),
                    'replies': replies,
                    'views': views,
                    'source': 'Nixware'
                }
                
                news_by_date[date_key].append(news_item)
                
            except Exception as e:
                continue
        
        if not news_by_date:
            return {
                'success': True,
                'count': 0,
                'latest_date': None,
                'news': []
            }
        
        # 获取最新日期的消息
        latest_date = max(news_by_date.keys())
        latest_news = news_by_date[latest_date]
        
        return {
            'success': True,
            'count': len(latest_news),
            'latest_date': latest_date,
            'news': latest_news
        }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"请求错误: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"解析错误: {str(e)}"
        }

def get_neverlose_latest_news():
    """获取Neverlose最新Update消息"""
    import json
    
    # 使用Discourse的JSON API
    url = "https://forum.neverlose.cc/c/news/31/l/latest.json"
    
    # 使用正常浏览器请求头，优先JSON，不使用压缩
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 尝试解析JSON
        try:
            data = response.json()
            
            # 检查是否有topic_list和topics
            if 'topic_list' in data and 'topics' in data['topic_list']:
                topics = data['topic_list']['topics']
                
                # 查找包含"Update"的最新主题
                for topic in topics:
                    title = topic.get('title', '')
                    if 'Update' in title:
                        # 构建完整链接
                        topic_id = topic.get('id')
                        slug = topic.get('slug', '')
                        link = f"https://forum.neverlose.cc/t/{slug}/{topic_id}" if topic_id else ''
                        
                        # 解析创建时间
                        created_at = topic.get('created_at', '')
                        try:
                            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        except:
                            date_obj = datetime.now(timezone.utc)
                        
                        news_item = {
                            'title': title,
                            'link': link,
                            'author': '未知',  # JSON中没有直接的作者信息
                            'date': date_obj.isoformat(),
                            'replies': str(topic.get('reply_count', 0)),
                            'views': str(topic.get('posts_count', 0)),
                            'source': 'Neverlose'
                        }
                        
                        return {
                            'success': True,
                            'count': 1,
                            'latest_date': date_obj.strftime('%Y-%m-%d'),
                            'news': [news_item]
                        }
                
                # 如果没找到包含"Update"的主题
                return {
                    'success': True,
                    'count': 0,
                    'latest_date': None,
                    'news': []
                }
            else:
                return {
                    'success': False,
                    'error': "JSON响应格式不正确"
                }
                
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': "无法解析JSON响应"
            }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"请求错误: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"解析错误: {str(e)}"
        }

def get_fatality_latest_news(cookies=None):
    """获取Fatality上次更新的消息
    
    Args:
        cookies (str): 可选的cookie字符串，格式如 "key1=value1; key2=value2"
    """
    url = "https://fatality.win/forums/updates.44/"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"138.0.3351.121"',
        "sec-ch-ua-full-version-list": '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.184", "Microsoft Edge";v="138.0.3351.121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"19.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    
    # 如果提供了cookies，添加到headers中
    if cookies:
        headers["Cookie"] = cookies
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 按日期分组消息
        news_by_date = defaultdict(list)
        
        # 查找所有帖子 - 尝试多种选择器
        threads = soup.find_all('div', class_='structItem') or \
                 soup.find_all('div', class_=lambda x: x and 'thread' in x.lower()) or \
                 soup.find_all('article') or \
                 soup.find_all('li', class_=lambda x: x and 'thread' in x.lower())
        
        for thread in threads:
            try:
                # 获取标题链接
                title_element = thread.find('a', href=lambda x: x and ('/threads/' in x or '/posts/' in x)) or \
                               thread.find('a', {'data-tp-primary': 'on'})
                
                if not title_element:
                    continue
                    
                title = title_element.get_text(strip=True)
                link = title_element.get('href', '')
                
                if not title:
                    continue
                
                # 获取日期
                date_element = thread.find('time') or \
                              thread.find('span', class_=lambda x: x and 'date' in x.lower()) or \
                              thread.find('div', class_=lambda x: x and 'date' in x.lower())
                
                date_str = ''
                if date_element:
                    date_str = date_element.get('datetime', '') or \
                              date_element.get('title', '') or \
                              date_element.get_text(strip=True)
                
                # 解析日期
                try:
                    if 'T' in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        date_key = date_obj.date().isoformat()
                    else:
                        date_key = date_str
                except:
                    date_key = date_str
                
                # 获取作者
                author_element = thread.find('a', class_='username') or \
                                thread.find('a', href=lambda x: x and '/members/' in x) or \
                                thread.find('span', class_=lambda x: x and 'author' in x.lower())
                author = author_element.get_text(strip=True) if author_element else ''
                
                # 获取统计信息
                replies = '0'
                views = '0'
                stats = thread.find_all('dd') or thread.find_all('span', class_=lambda x: x and 'count' in x.lower())
                for stat in stats:
                    stat_text = stat.get_text(strip=True)
                    if stat_text.isdigit():
                        if replies == '0':
                            replies = stat_text
                        else:
                            views = stat_text
                            break
                
                news_item = {
                    'title': title,
                    'link': f"https://fatality.win{link}" if link.startswith('/') else link,
                    'author': author,
                    'date': date_str,
                    'replies': replies,
                    'views': views,
                    'source': 'Fatality'
                }
                
                news_by_date[date_key].append(news_item)
                    
            except Exception as e:
                continue
        
        # 获取上次更新的消息
        if news_by_date:
            latest_date = max(news_by_date.keys())
            latest_news = news_by_date[latest_date]
            
            return {
                'success': True,
                'latest_date': latest_date,
                'count': len(latest_news),
                'news': latest_news
            }
        else:
            return {
                'success': True,
                'latest_date': None,
                'count': 0,
                'news': []
            }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"请求错误: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"解析错误: {str(e)}"
        }

def get_memesense_latest_news():
    """获取Memesense最新更新消息"""
    url = "https://api.memesense.gg/forums/26/threads"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'threads' not in data:
            return {
                'success': False,
                'error': '响应中未找到threads数据'
            }
        
        threads = data['threads']
        
        if not threads:
            return {
                'success': True,
                'count': 0,
                'news': [],
                'latest_date': None
            }
        
        # 按日期分组消息
        news_by_date = defaultdict(list)
        
        for thread in threads:
            try:
                # 获取基本信息
                thread_id = thread.get('id', '')
                title = thread.get('name', '').strip()
                
                if not title:
                    continue
                
                # 构建链接
                link = f"https://memesense.gg/forums/26/threads/{thread_id}/"
                
                # 获取时间信息
                created_at = thread.get('created_at', '')
                updated_at = thread.get('updated_at', '')
                
                # 使用更新时间作为主要时间，如果没有则使用创建时间
                date_str = updated_at or created_at
                
                try:
                    if date_str:
                        # 解析ISO格式时间
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        date_key = date_obj.date().isoformat()
                        formatted_date = date_obj.strftime('%Y-%m-%d')
                    else:
                        date_obj = datetime.now(timezone.utc)
                        date_key = date_obj.date().isoformat()
                        formatted_date = date_key
                except:
                    date_obj = datetime.now(timezone.utc)
                    date_key = date_obj.date().isoformat()
                    formatted_date = date_key
                
                # 获取用户信息
                user_info = thread.get('user', {})
                author = user_info.get('login', '未知')
                
                # 获取统计信息
                views_count = thread.get('views_count', 0)
                posts_count = thread.get('posts_count', 0)
                
                news_item = {
                    'title': title,
                    'link': link,
                    'author': author,
                    'date': formatted_date,
                    'replies': str(posts_count),
                    'views': str(views_count),
                    'timestamp': date_obj
                }
                
                news_by_date[date_key].append(news_item)
                
            except Exception as e:
                print(f"处理thread时出错: {e}")
                continue
        
        if not news_by_date:
            return {
                'success': True,
                'count': 0,
                'news': [],
                'latest_date': None
            }
        
        # 获取最新日期的消息
        latest_date = max(news_by_date.keys())
        latest_news = news_by_date[latest_date]
        
        # 按时间戳排序（最新的在前）
        latest_news.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # 只返回最新的一条消息
        latest_news = latest_news[:1]
        
        return {
            'success': True,
            'count': len(latest_news),
            'news': latest_news,
            'latest_date': latest_date
        }
        
    except requests.RequestException as e:
        return {
            'success': False,
            'error': f"请求错误: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"解析错误: {str(e)}"
        }

def get_plaguecheat_latest_news():
    """由于瘟疫官网使用的Cloudflare防护严格，暂时无法获取。"""
    return {
        'success': False,
        'error': '由于瘟疫官网使用的Cloudflare防护严格，暂时无法获取。B站CTCAKE 敬请期待。'
    }

def get_cs2_latest_news(steam_token=None):
    """获取CS2最新更新消息
    
    Args:
        steam_token (str): Steam API访问令牌
    
    注意: 这个token是便宜白号上抓的，不值钱，token于 2025 年 8 月 5 日 14:46 过期，请看config.py中教程自行获取
    """
    # 如果没有提供token，直接使用备用Steam新闻API
    if steam_token:
        url = f"https://api.steampowered.com/IAssetSetPublishingService/UpdatePublishTime/v1/?access_token={steam_token}&appid=730"
    else:
        # 直接跳转到备用API
        url = None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://steamcommunity.com',
        'Referer': 'https://steamcommunity.com/'
    }
    
    # POST请求数据
    data = {
        'appid': '730'  # CS2的Steam应用ID
    }
    
    try:
        # 如果有token，先尝试主API
        if url:
            response = requests.post(url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            # 尝试解析JSON响应
            try:
                json_data = response.json()
                # 如果主API有有效响应，处理它
                if json_data:
                    # 这里可以根据实际API响应格式进行解析
                    # 目前使用备用的Steam新闻API
                    pass
            except:
                pass
        
        # 使用备用Steam新闻API
            news_url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=730&count=5&maxlength=300&format=json"
            news_response = requests.get(news_url, timeout=15)
            news_response.raise_for_status()
            json_data = news_response.json()
            
            if 'appnews' in json_data and 'newsitems' in json_data['appnews']:
                news_items = json_data['appnews']['newsitems']
                
                if news_items:
                    # 获取最新的新闻
                    latest_news = news_items[0]
                    
                    # 转换时间戳为本地时间
                    timestamp = latest_news.get('date', 0)
                    date_obj = datetime.fromtimestamp(timestamp)
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': latest_news.get('title', 'CS2 Update'),
                        'link': latest_news.get('url', 'https://store.steampowered.com/app/730/Counter_Strike_2/'),
                        'author': latest_news.get('author', 'Valve'),
                        'date': formatted_date,
                        'content': latest_news.get('contents', ''),
                        'timestamp': date_obj
                    }
                    
                    return {
                        'success': True,
                        'count': 1,
                        'news': [news_item],
                        'latest_date': formatted_date
                    }
            
            return {
                'success': True,
                'count': 0,
                'news': [],
                'latest_date': None
            }
        
        # 如果原始API有响应，处理它
        if json_data:
            # 这里可以根据实际API响应格式进行解析
            # 目前使用备用的Steam新闻API
            return {
                'success': True,
                'count': 0,
                'news': [],
                'latest_date': None
            }
        
    except requests.RequestException as e:
        # 如果主API失败，尝试备用Steam新闻API
        try:
            news_url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=730&count=5&maxlength=300&format=json"
            news_response = requests.get(news_url, timeout=15)
            news_response.raise_for_status()
            json_data = news_response.json()
            
            if 'appnews' in json_data and 'newsitems' in json_data['appnews']:
                news_items = json_data['appnews']['newsitems']
                
                if news_items:
                    # 获取最新的新闻
                    latest_news = news_items[0]
                    
                    # 转换时间戳为本地时间
                    timestamp = latest_news.get('date', 0)
                    date_obj = datetime.fromtimestamp(timestamp)
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': latest_news.get('title', 'CS2 Update'),
                        'link': latest_news.get('url', 'https://store.steampowered.com/app/730/Counter_Strike_2/'),
                        'author': latest_news.get('author', 'Valve'),
                        'date': formatted_date,
                        'content': latest_news.get('contents', ''),
                        'timestamp': date_obj
                    }
                    
                    return {
                        'success': True,
                        'count': 1,
                        'news': [news_item],
                        'latest_date': formatted_date
                    }
            
            return {
                'success': True,
                'count': 0,
                'news': [],
                'latest_date': None
            }
            
        except Exception as backup_e:
            return {
                'success': False,
                'error': f"请求错误: {str(e)}, 备用API错误: {str(backup_e)}"
            }
    except Exception as e:
        return {
            'success': False,
            'error': f"解析错误: {str(e)}"
        }

def get_all_latest_news(fatality_cookies=None):
    """获取所有网站的最新消息
    
    Args:
        fatality_cookies (str): Fatality网站的cookie字符串
    """
    results = []
    
    # 获取Nixware消息
    nixware_result = get_nixware_latest_news()
    if nixware_result['success'] and nixware_result['count'] > 0:
        results.extend(nixware_result['news'])
    
    # 获取Neverlose消息
    neverlose_result = get_neverlose_latest_news()
    if neverlose_result['success'] and neverlose_result['count'] > 0:
        results.extend(neverlose_result['news'])
    
    # 获取Fatality消息
    fatality_result = get_fatality_latest_news(fatality_cookies)
    if fatality_result['success'] and fatality_result['count'] > 0:
        results.extend(fatality_result['news'])
    
    # 获取Memesense消息
    memesense_result = get_memesense_latest_news()
    if memesense_result['success'] and memesense_result['count'] > 0:
        results.extend(memesense_result['news'])
    
    # 获取Plaguecheat消息
    plaguecheat_result = get_plaguecheat_latest_news()
    if plaguecheat_result['success'] and plaguecheat_result['count'] > 0:
        results.extend(plaguecheat_result['news'])
    
    # 获取CS2消息
    try:
        from config import STEAM_ACCESS_TOKEN
        cs2_result = get_cs2_latest_news(STEAM_ACCESS_TOKEN)
    except ImportError:
        cs2_result = get_cs2_latest_news()
    if cs2_result['success'] and cs2_result['count'] > 0:
        results.extend(cs2_result['news'])
    
    return {
        'success': True,
        'total_count': len(results),
        'nixware': nixware_result,
        'neverlose': neverlose_result,
        'fatality': fatality_result,
        'memesense': memesense_result,
        'plaguecheat': plaguecheat_result,
        'cs2': cs2_result,
        'all_news': results
    }

def print_all_latest_news(fatality_cookies=None):
    """打印所有网站的最新消息
    
    Args:
        fatality_cookies (str): Fatality网站的cookie字符串
    """
    print("正在获取各大论坛最新消息...\n")
    
    result = get_all_latest_news(fatality_cookies)
    
    if result['success']:
        print(f"总共找到 {result['total_count']} 条最新消息\n")
        
        # 显示Nixware消息
        nixware = result['nixware']
        print("=== Nixware ===")
        if nixware['success'] and nixware['count'] > 0:
            print(f"上次更新: {nixware['latest_date']}")
            for i, news in enumerate(nixware['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = nixware.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 显示Neverlose消息
        neverlose = result['neverlose']
        print("\n=== Neverlose ===")
        if neverlose['success'] and neverlose['count'] > 0:
            print(f"上次更新: {neverlose['latest_date']}")
            for i, news in enumerate(neverlose['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = neverlose.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 显示Fatality消息
        fatality = result['fatality']
        print("\n=== Fatality ===")
        if fatality['success'] and fatality['count'] > 0:
            print(f"上次更新: {fatality['latest_date']}")
            for i, news in enumerate(fatality['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = fatality.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 显示Memesense消息
        memesense = result['memesense']
        print("\n=== Memesense ===")
        if memesense['success'] and memesense['count'] > 0:
            print(f"上次更新: {memesense['latest_date']}")
            for i, news in enumerate(memesense['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = memesense.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 显示Plaguecheat消息
        plaguecheat = result['plaguecheat']
        print("\n=== Plaguecheat ===")
        if plaguecheat['success'] and plaguecheat['count'] > 0:
            print(f"上次更新: {plaguecheat['latest_date']}")
            for i, news in enumerate(plaguecheat['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = plaguecheat.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 显示CS2消息
        cs2 = result['cs2']
        print("\n=== CS2[来自SteamAPI] ====")
        if cs2['success'] and cs2['count'] > 0:
            print(f"上次更新: {cs2['latest_date']}")
            for i, news in enumerate(cs2['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            error_msg = cs2.get('error', '无消息')
            print(f"获取失败: {error_msg}")
        
        # 添加更新总结
        print("\n" + "=" * 60)
        print("📊 更新总结 (纯日期计算，仅供参考)")
        print("=" * 60)
        
        # 获取CS2更新日期
        cs2_date = None
        if cs2['success'] and cs2['count'] > 0:
            cs2_date = cs2['latest_date']
            print(f"🎮 CS2最新更新: {cs2_date}")
        else:
            print("🎮 CS2更新日期: 获取失败")
        
        if cs2_date:
            print("\n各大cheat可用性分析:")
            
            # 检查各个cheat的状态
            cheats = [
                ('Nixware', nixware),
                ('Neverlose', neverlose), 
                ('Fatality', fatality),
                ('Memesense', memesense),
                ('Plaguecheat', plaguecheat)
            ]
            
            for cheat_name, cheat_data in cheats:
                if cheat_data['success'] and cheat_data['count'] > 0:
                    cheat_date = cheat_data['latest_date']
                    
                    # 比较日期
                    try:
                        cs2_dt = datetime.strptime(cs2_date, '%Y-%m-%d')
                        cheat_dt = datetime.strptime(cheat_date, '%Y-%m-%d')
                        
                        if cheat_dt >= cs2_dt:
                            status = "✅ 可正常使用"
                        else:
                            status = "❌ 可能不可用"
                        
                        print(f"  {cheat_name}: {cheat_date} - {status}")
                    except:
                        print(f"  {cheat_name}: {cheat_date} - ⚠️ 日期格式异常")
                else:
                    print(f"  {cheat_name}: 获取失败 - ⚠️ 无法判断")
        else:
            print("\n⚠️ 无法获取CS2更新日期，无法进行可用性分析")
            
        print("\n💡 提示: 此分析基于更新日期对比，实际可用性可能因其他因素而异")
    else:
        print("获取所有消息失败")

def print_nixware_only():
    """只打印Nixware最新消息"""
    print("正在获取Nixware最新消息...\n")
    
    result = get_nixware_latest_news()
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

def print_neverlose_only():
    """只打印Neverlose最新消息"""
    print("正在获取Neverlose最新消息...\n")
    
    result = get_neverlose_latest_news()
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

def print_fatality_only(cookies=None):
    """只打印Fatality最新消息
    
    Args:
        cookies (str): 可选的cookie字符串
    """
    print("正在获取Fatality最新消息...\n")
    
    result = get_fatality_latest_news(cookies)
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

def print_memesense_only():
    """只打印Memesense最新消息"""
    print("正在获取Memesense最新消息...\n")
    
    result = get_memesense_latest_news()
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

def print_plaguecheat_only():
    """只打印Plaguecheat最新消息"""
    print("正在获取Plaguecheat最新消息...\n")
    
    result = get_plaguecheat_latest_news()
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

def print_cs2_only():
    """只打印CS2最新消息"""
    print("正在获取CS2最新消息...\n")
    
    try:
        from config import STEAM_ACCESS_TOKEN
        result = get_cs2_latest_news(STEAM_ACCESS_TOKEN)
    except ImportError:
        result = get_cs2_latest_news()
    
    if result['success']:
        if result['count'] > 0:
            print(f"上次更新: {result['latest_date']}\n")
            for i, news in enumerate(result['news'], 1):
                print(f"{i}. {news['title']}")
                print(f"   🔗 {news['link']}")
                print("-" * 50)
        else:
            print("暂无最新消息")
    else:
        print(f"获取失败: {result['error']}")

if __name__ == "__main__":
    import sys
    
    # 尝试从配置文件读取cookies
    try:
        from config import FATALITY_COOKIES
    except ImportError:
        print("警告: 未找到config.py文件，Fatality功能无法正常使用")
        FATALITY_COOKIES = ""
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == '--nixware':
            print_nixware_only()
        elif arg == '--neverlose':
            print_neverlose_only()
        elif arg == '--fatality':
            print_fatality_only(FATALITY_COOKIES)
        elif arg == '--memesense':
            print_memesense_only()
        elif arg == '--plaguecheat':
            print_plaguecheat_only()
        elif arg == '--cs2':
            print_cs2_only()
        elif arg == '--help' or arg == '-h':
            print("使用方法:")
            print("  python cheatstatus.py            # 获取所有网站最新消息")
            print("  python cheatstatus.py --nixware  # 只获取Nixware最新消息")
            print("  python cheatstatus.py --neverlose # 只获取Neverlose最新消息")
            print("  python cheatstatus.py --fatality # 只获取Fatality最新消息")
            print("  python cheatstatus.py --memesense # 只获取Memesense最新消息")
            print("  python cheatstatus.py --plaguecheat # 只获取Plaguecheat最新消息")
            print("  python cheatstatus.py --cs2      # 只获取CS2官方最新消息")
            print("  python cheatstatus.py --help     # 显示帮助信息")
            print("\n注意: 访问Fatality需要在config.py中配置cookies")
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("使用 --help 查看可用参数")
    else:
        print_all_latest_news(FATALITY_COOKIES)