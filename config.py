# 配置文件
# 请在这里设置Fatality网站的cookies

# Fatality网站的cookies
# 在论坛官网按F12，点击网络(Network)，然后刷新页面，找到第一个请求，点击，找到请求标头，下方有cookie，一整串复制下来，粘贴到下方
# 如果第一个请求没有cookie，那就找第二个请求，以此类推
# 格式: "key1=value1; key2=value2; key3=value3"
FATALITY_COOKIES = "cf_clearance=JSVTp90X4F4LnAClnwfvS5iMK0bZbkYqc9NC3UbeQXY-1754284830-1.2.1.1-g1_KOWfh0EhLeAL4mTWFqNrgbHEgean7Hwxgpf.oCvnimuWvkXgYE.h.ZGinShx6xZl90nDnFKXh_pBDm4zpxLoRp0.xLO3246fM4Jc5gzCfdpH5zm3WKdKqvbyoCGdjWV3w4UgGQ5Chjyu3HZR.I0u1p6tYFYdiFXCxwZOrdgtOaZ8h0MrxPU7bo3Air80eigA8ILzGP6t3aU52h9oyM4GmGJ7BtXyebIXcydXBQkQ; xf_csrf=Q-m37-x8ge0ShyBN; xf_session=b54A18IGjZZwatPDmCWzICm39-K5NBQp"

# 示例（请替换为你的实际cookies）:
# FATALITY_COOKIES = "xf_csrf=abc123; xf_session=def456; xf_user=789xyz"

# 如果你不需要访问Fatality，可以保持为空字符串
# FATALITY_COOKIES = ""

# Steam API Token配置
# 用于获取CS2官方更新信息
# 获取方法：
# 1、浏览器登录 s.team
# 2、浏览器打开 https://store.steampowered.com/pointssummary/ajaxgetasyncconfig
# 3、复制显示结果中的webapi_token值
# 注意：这个token是便宜白号，不值钱，token将于 2025 年 8 月 5 日 14:46 过期
STEAM_ACCESS_TOKEN = "eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAxNl8yNkIyRUNCRl9DRjkzRCIsICJzdWIiOiAiNzY1NjExOTk3MzE0MjY3MzUiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTc1NDM3NTc4OCwgIm5iZiI6IDE3NDU2NDg5NzAsICJpYXQiOiAxNzU0Mjg4OTcwLCAianRpIjogIjAwMDhfMjZCOTRCM0ZfQkU4MTQiLCAib2F0IjogMTc1NDI4ODk3MCwgInJ0X2V4cCI6IDE3NzI0NDkyMzIsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxMDMuMTUxLjE3Mi4yNSIsICJpcF9jb25maXJtZXIiOiAiMTAzLjE1MS4xNzIuMjUiIH0.lCEVQyLuqg9M51Fd0SYWzN6WaVgqmjfCKiqyZgodZdwKgcWq29mmq_hLrc07K4IWBIruWK7AepsEJa8v7d6qBg"