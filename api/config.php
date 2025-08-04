<?php
// Steam API配置
// 获取方法：
// 1. 登录steam
// 2. 打开 https://store.steampowered.com/pointssummary/ajaxgetasyncconfig
// 3. 复制JSON响应中的 webapi_token 值
// 注意: 这个token是便宜白号，不值钱，token将于 2025 年 8 月 5 日 14:46 过期
define('STEAM_ACCESS_TOKEN', 'eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwQV8yNjlCMjlGMl8zMDk3OSIsICJzdWIiOiAiNzY1NjExOTk2Mzk3NjYyNjIiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTc1NDM3NjM2OCwgIm5iZiI6IDE3NDU2NDgyNDEsICJpYXQiOiAxNzU0Mjg4MjQxLCAianRpIjogIjAwMEFfMjZCODBCODdfMzY2QTUiLCAib2F0IjogMTc1MjM0Mjg2OCwgInJ0X2V4cCI6IDE3NzAyOTIzNzIsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxMDMuMTUxLjE3Mi44NCIsICJpcF9jb25maXJtZXIiOiAiMTAzLjE1MS4xNzIuMzEiIH0.OBUolL0vS5NG8hKkHq-gKFb260UyYGJeLMkGunZm3BiXnrdjXwAXTBQ4T9jLo1TlO7nRvjyK9deo80zzkyMDAw');

// Fatality Cookies (如果需要)
define('FATALITY_COOKIES', 'cf_clearance=JSVTp90X4F4LnAClnwfvS5iMK0bZbkYqc9NC3UbeQXY-1754284830-1.2.1.1-g1_KOWfh0EhLeAL4mTWFqNrgbHEgean7Hwxgpf.oCvnimuWvkXgYE.h.ZGinShx6xZl90nDnFKXh_pBDm4zpxLoRp0.xLO3246fM4Jc5gzCfdpH5zm3WKdKqvbyoCGdjWV3w4UgGQ5Chjyu3HZR.I0u1p6tYFYdiFXCxwZOrdgtOaZ8h0MrxPU7bo3Air80eigA8ILzGP6t3aU52h9oyM4GmGJ7BtXyebIXcydXBQkQ; xf_csrf=Q-m37-x8ge0ShyBN; xf_session=b54A18IGjZZwatPDmCWzICm39-K5NBQp');

// 请求超时设置
define('REQUEST_TIMEOUT', 60);

// User-Agent
define('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36');
?>