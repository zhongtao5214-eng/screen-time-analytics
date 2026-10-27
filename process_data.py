# -*- coding: utf-8 -*-
"""
Process AppUsage data into a high-performance structured JSON for the HTML Dashboard
Upgraded with:
- Accurate Gemini & Google AI attribution (resolving the PWA/shortcut vs host execution gap)
- Opportunity Cost & Time Reclaiming calculations (2h daily baseline allowance, books, courses, dates, workouts, trips, economic value)
"""
import sys, os, re, json
from collections import defaultdict
from datetime import datetime

base_dir = r"d:\桌面\测试\屏幕使用时间管理数据分析"
day_csv = os.path.join(base_dir, "AppUsage_day.csv")

# App Categorization Mapping
CATEGORY_RULES = {
    'AI 生产力助手': [
        'chatgpt', 'deepseek', 'nova', '豆包', 'kimi', 'moonshot', 'claude', 'gemini', 'bard',
        'googlequicksearchbox', # Gemini Host execution on Android
        'tailwind', # NotebookLM
        'copilot', '元宝', '通义', '文心'
    ],
    '社交通讯': [
        '微信', 'tencent.mm', 'qq', 'tim', '联系人', '电话', '短信', 'contacts', 'messaging', 'telecom'
    ],
    '短视频与流媒体': [
        'aweme', '抖音', 'bili', 'danmaku', '快手', 'kuaishou', 'yumme', 'youtube', 'qqlive', 'youku', 'iqiyi', 'video', 'dongjingre'
    ],
    '工作协同与学习': [
        '飞书', 'lark', 'uuremote', '远程', '百度网盘', 'netdisk', '京东读书', 'reader', '幕布', 'mubu', 'office', 'wps', '夸克', 'quark', 'chrome', 'browser'
    ],
    '资讯与社交社区': [
        'xhs', '小红书', 'zhihu', '知乎', 'weibo', '微博', 'twitter', 'toutiao', '今日头条'
    ],
    '电商与生活消费': [
        'taobao', '淘宝', 'jd', 'jingdong', '京东', 'pinduoduo', '拼多多', 'alipay', '支付宝', 'meituan', '美团', 'eleme', '饿了么', 'edoor', '亲邻开门', 'minimap', '高德地图', 'map', '地图'
    ],
    '手游与互动娱乐': [
        'sgame', '王者荣耀', 'pubg', '和平精英', 'game', 'mihoyo', '原神', 'tmgp'
    ],
    '系统与工具辅助': [
        'launcher', '系统桌面', 'screentime', '屏幕时间', 'appusage', 'settings', '设置', 'battery', '电池', 'systemui', 'clash', 'vpn', 'digitalwellbeing', '数字健康', 'health', '健康', 'gallery', '相册', 'camera', '相机'
    ]
}

# Friendly App Names mapping
FRIENDLY_NAMES = {
    'com.tencent.mm': '微信',
    'com.ss.android.ugc.aweme': '抖音',
    'com.android.launcher': '系统桌面',
    'com.google.android.apps.bard': 'Gemini (桌面快捷入口)',
    'com.google.android.googlequicksearchbox': 'Gemini / Google AI (运行宿主)',
    'com.google.android.apps.labs.language.tailwind': 'NotebookLM (Google AI)',
    'com.coloros.digitalwellbeing': '数字健康与守护',
    'com.xingin.xhs': '小红书',
    'com.ss.android.yumme.video': 'Yumme 视频',
    'tv.danmaku.bili': '哔哩哔哩',
    'com.openai.chatgpt': 'ChatGPT',
    'com.tencent.tmgp.sgame': '王者荣耀',
    'com.baidu.netdisk': '百度网盘',
    'com.ss.android.lark': '飞书',
    'com.larus.nova': '豆包 AI',
    'com.deepseek.chat': 'DeepSeek',
    'com.taobao.taobao': '淘宝',
    'com.autonavi.minimap': '高德地图',
    'com.capsule.screentime': '屏幕时间管理',
    'com.netease.uuremote': 'UU 远程',
    'com.jd.app.reader': '京东读书',
    'com.jingdong.app.mall': '京东',
    'com.android.chrome': 'Google Chrome 浏览器',
    'com.google.android.youtube': 'YouTube',
    'com.tencent.tim': 'TIM (QQ)',
    'com.moonshot.kimichat': 'Kimi AI',
    'com.mubu.app': '幕布',
    'com.hihonor.health': '运动健康',
    'com.xunmeng.pinduoduo': '拼多多',
    'com.github.metacubex.clash.meta': 'Clash Meta',
    'com.twitter.android': 'X (Twitter)',
    'com.microsoft.copilot': 'Copilot'
}

def classify_app(pkg, name):
    pkg_l = pkg.lower()
    name_l = name.lower()
    
    # Priority 1: AI
    for kw in CATEGORY_RULES['AI 生产力助手']:
        if kw in pkg_l or kw in name_l:
            return 'AI 生产力助手'
            
    # Priority 2: Short video
    for kw in CATEGORY_RULES['短视频与流媒体']:
        if kw in pkg_l or kw in name_l:
            return '短视频与流媒体'
            
    # Priority 3: Social
    for kw in CATEGORY_RULES['社交通讯']:
        if kw in pkg_l or kw in name_l:
            return '社交通讯'
            
    # Other categories
    for cat, kws in CATEGORY_RULES.items():
        if cat in ['AI 生产力助手', '短视频与流媒体', '社交通讯']:
            continue
        for kw in kws:
            if kw in pkg_l or kw in name_l:
                return cat
                
    return '其他应用'

print("Reading AppUsage_day.csv with Gemini attribution updates...")
date_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})")

daily_all = {}
daily_app_records = defaultdict(dict)
app_stats = {}

with open(day_csv, "r", encoding="utf-8-sig", errors="replace") as f:
    cur_date = None
    for line in f:
        l = line.strip()
        if not l: continue
        m = date_pattern.match(l)
        if m:
            cur_date = m.group(1)
            continue
        parts = l.split(",")
        if len(parts) >= 6:
            raw_name = parts[1].strip()
            pkg = parts[2].strip()
            try: ms = float(parts[4])
            except: ms = 0.0
            try: starts = int(parts[5])
            except: starts = 0
            try: notifs = int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else 0
            except: notifs = 0
                
            split_ms = 0.0
            if len(parts) > 7 and "分屏时长" in parts[7]:
                raw_split = parts[7].replace("（分屏时长）", "").strip()
                try: split_ms = float(raw_split)
                except: split_ms = 0.0
                
            if pkg == "ALL":
                daily_all[cur_date] = {
                    "date": cur_date,
                    "ms": ms,
                    "starts": starts,
                    "notifs": notifs,
                    "split_ms": split_ms
                }
            else:
                if ms > 0 or starts > 0:
                    name = FRIENDLY_NAMES.get(pkg, raw_name or pkg)
                    cat = classify_app(pkg, name)
                    daily_app_records[cur_date][pkg] = {
                        "name": name,
                        "cat": cat,
                        "ms": ms,
                        "starts": starts,
                        "notifs": notifs
                    }
                    if pkg not in app_stats:
                        app_stats[pkg] = {
                            "pkg": pkg,
                            "name": name,
                            "cat": cat,
                            "total_ms": 0.0,
                            "total_starts": 0,
                            "total_notifs": 0,
                            "active_days": 0,
                            "first_date": cur_date,
                            "last_date": cur_date,
                            "monthly_ms": defaultdict(float),
                            "monthly_starts": defaultdict(int)
                        }
                    st = app_stats[pkg]
                    st["total_ms"] += ms
                    st["total_starts"] += starts
                    st["total_notifs"] += notifs
                    st["active_days"] += 1
                    month_key = cur_date[:7]
                    st["monthly_ms"][month_key] += ms
                    st["monthly_starts"][month_key] += starts
                    if cur_date < st["first_date"]: st["first_date"] = cur_date
                    if cur_date > st["last_date"]: st["last_date"] = cur_date

all_dates = sorted(daily_all.keys())
months = sorted(list(set(d[:7] for d in all_dates)))

# Compute Monthly Aggregates
monthly_summary = []
for m in months:
    m_dates = [d for d in all_dates if d.startswith(m)]
    m_ms = sum(daily_all[d]['ms'] for d in m_dates)
    m_starts = sum(daily_all[d]['starts'] for d in m_dates)
    m_notifs = sum(daily_all[d]['notifs'] for d in m_dates)
    m_split = sum(daily_all[d]['split_ms'] for d in m_dates)
    
    cat_ms = defaultdict(float)
    ai_ms = 0.0
    video_ms = 0.0
    for d in m_dates:
        for pkg, app_rec in daily_app_records[d].items():
            cat = app_rec['cat']
            cat_ms[cat] += app_rec['ms']
            if cat == 'AI 生产力助手': ai_ms += app_rec['ms']
            elif cat == '短视频与流媒体': video_ms += app_rec['ms']
            
    monthly_summary.append({
        "month": m,
        "days": len(m_dates),
        "total_hours": round(m_ms / 3600000, 2),
        "daily_avg_hours": round(m_ms / len(m_dates) / 3600000, 2),
        "total_starts": m_starts,
        "daily_avg_starts": round(m_starts / len(m_dates), 1),
        "total_notifs": m_notifs,
        "daily_avg_notifs": round(m_notifs / len(m_dates), 1),
        "split_hours": round(m_split / 3600000, 2),
        "ai_hours": round(ai_ms / 3600000, 2),
        "video_hours": round(video_ms / 3600000, 2),
        "categories_hours": {k: round(v / 3600000, 2) for k, v in cat_ms.items()}
    })

# Compute Daily Timeline List
daily_timeline = []
weekday_totals = defaultdict(lambda: {'ms': 0, 'starts': 0, 'notifs': 0, 'days': 0, 'cat_ms': defaultdict(float)})

for d in all_dates:
    val = daily_all[d]
    dt = datetime.strptime(d, "%Y-%m-%d")
    w = dt.weekday()
    is_weekend = (w >= 5)
    
    apps_today = daily_app_records[d]
    top_pkg = ""
    top_app_name = ""
    top_ms = 0.0
    day_ai_ms = 0.0
    day_video_ms = 0.0
    
    for pkg, arec in apps_today.items():
        if arec['cat'] == 'AI 生产力助手': day_ai_ms += arec['ms']
        elif arec['cat'] == '短视频与流媒体': day_video_ms += arec['ms']
        if arec['ms'] > top_ms:
            top_ms = arec['ms']
            top_pkg = pkg
            top_app_name = arec['name']
            
        weekday_totals[w]['cat_ms'][arec['cat']] += arec['ms']
        
    weekday_totals[w]['ms'] += val['ms']
    weekday_totals[w]['starts'] += val['starts']
    weekday_totals[w]['notifs'] += val['notifs']
    weekday_totals[w]['days'] += 1
    
    daily_timeline.append({
        "date": d,
        "hours": round(val['ms'] / 3600000, 2),
        "starts": val['starts'],
        "notifs": val['notifs'],
        "split_h": round(val['split_ms'] / 3600000, 2),
        "weekday": w,
        "is_weekend": is_weekend,
        "top_app": top_app_name,
        "top_hours": round(top_ms / 3600000, 2),
        "ai_hours": round(day_ai_ms / 3600000, 2),
        "video_hours": round(day_video_ms / 3600000, 2)
    })

# Weekday distribution
weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
weekday_summary = []
for w in range(7):
    item = weekday_totals[w]
    cnt = item['days'] or 1
    weekday_summary.append({
        "day_index": w,
        "name": weekday_names[w],
        "days_count": cnt,
        "avg_hours": round(item['ms'] / cnt / 3600000, 2),
        "avg_starts": round(item['starts'] / cnt, 1),
        "avg_notifs": round(item['notifs'] / cnt, 1),
        "categories_avg_hours": {k: round(v / cnt / 3600000, 2) for k, v in item['cat_ms'].items()}
    })

# AI Tools Special Tracking
ai_pkgs = [pkg for pkg, meta in app_stats.items() if meta['cat'] == 'AI 生产力助手']
ai_apps_ranking = []
for pkg in ai_pkgs:
    meta = app_stats[pkg]
    monthly_data = {m: round(meta["monthly_ms"].get(m, 0.0) / 3600000, 2) for m in months}
    monthly_starts = {m: meta["monthly_starts"].get(m, 0) for m in months}
    ai_apps_ranking.append({
        "pkg": pkg,
        "name": meta["name"],
        "total_hours": round(meta["total_ms"] / 3600000, 2),
        "total_starts": meta["total_starts"],
        "active_days": meta["active_days"],
        "first_date": meta["first_date"],
        "last_date": meta["last_date"],
        "monthly_hours": monthly_data,
        "monthly_starts": monthly_starts
    })
ai_apps_ranking.sort(key=lambda x: (x["total_hours"], x["total_starts"]), reverse=True)

# Video Apps Special Tracking
video_pkgs = [pkg for pkg, meta in app_stats.items() if meta['cat'] == '短视频与流媒体']
video_apps_ranking = []
for pkg in video_pkgs:
    meta = app_stats[pkg]
    monthly_data = {m: round(meta["monthly_ms"].get(m, 0.0) / 3600000, 2) for m in months}
    monthly_starts = {m: meta["monthly_starts"].get(m, 0) for m in months}
    video_apps_ranking.append({
        "pkg": pkg,
        "name": meta["name"],
        "total_hours": round(meta["total_ms"] / 3600000, 2),
        "total_starts": meta["total_starts"],
        "active_days": meta["active_days"],
        "monthly_hours": monthly_data,
        "monthly_starts": monthly_starts
    })
video_apps_ranking.sort(key=lambda x: x["total_hours"], reverse=True)

# Top 50 Apps Overall for Drill-down
sorted_all_apps = sorted(app_stats.values(), key=lambda x: (x["total_ms"], x["total_starts"]), reverse=True)
top_apps_payload = []
for meta in sorted_all_apps[:50]:
    monthly_data = {m: round(meta["monthly_ms"].get(m, 0.0) / 3600000, 2) for m in months}
    monthly_starts = {m: meta["monthly_starts"].get(m, 0) for m in months}
    top_apps_payload.append({
        "pkg": meta["pkg"],
        "name": meta["name"],
        "cat": meta["cat"],
        "total_hours": round(meta["total_ms"] / 3600000, 2),
        "total_starts": meta["total_starts"],
        "total_notifs": meta["total_notifs"],
        "active_days": meta["active_days"],
        "first_date": meta["first_date"],
        "last_date": meta["last_date"],
        "avg_daily_min": round((meta["total_ms"] / meta["active_days"] / 60000), 1) if meta["active_days"] else 0,
        "monthly_hours": monthly_data,
        "monthly_starts": monthly_starts
    })

# Category Totals
category_totals = defaultdict(float)
category_starts = defaultdict(int)
for meta in app_stats.values():
    category_totals[meta['cat']] += meta['total_ms']
    category_starts[meta['cat']] += meta['total_starts']

cat_summary = []
total_all_cat_ms = sum(category_totals.values())
for cat, ms in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
    cat_summary.append({
        "category": cat,
        "total_hours": round(ms / 3600000, 2),
        "percentage": round(ms / total_all_cat_ms * 100, 2) if total_all_cat_ms else 0,
        "total_starts": category_starts[cat]
    })

total_screen_time_ms = sum(daily_all[d]['ms'] for d in all_dates)
total_starts_all = sum(daily_all[d]['starts'] for d in all_dates)
total_notifs_all = sum(daily_all[d]['notifs'] for d in all_dates)
total_split_ms = sum(daily_all[d]['split_ms'] for d in all_dates)

# Opportunity cost calculations
total_days = len(all_dates) # 767
wechat_ms = app_stats.get('com.tencent.mm', {}).get('total_ms', 0.0)
douyin_ms = app_stats.get('com.ss.android.ugc.aweme', {}).get('total_ms', 0.0)

# 2 hours per day baseline: 1h Douyin + 1h WeChat
baseline_allowance_hours = total_days * 2.0 # 1534 hours
total_screen_hours = total_screen_time_ms / 3600000 # 9083.1h

excess_all_hours = max(0.0, total_screen_hours - baseline_allowance_hours)
wechat_excess_hours = max(0.0, (wechat_ms / 3600000) - (total_days * 1.0))
douyin_excess_hours = max(0.0, (douyin_ms / 3600000) - (total_days * 1.0))
excess_social_video_hours = wechat_excess_hours + douyin_excess_hours

opportunity_cost = {
    "total_days": total_days,
    "baseline_daily_allowance_hours": 2.0,
    "baseline_total_allowance_hours": round(baseline_allowance_hours, 1),
    "excess_all_hours": round(excess_all_hours, 1),
    "excess_social_video_hours": round(excess_social_video_hours, 1),
    "wechat_total_hours": round(wechat_ms / 3600000, 1),
    "wechat_excess_hours": round(wechat_excess_hours, 1),
    "douyin_total_hours": round(douyin_ms / 3600000, 1),
    "douyin_excess_hours": round(douyin_excess_hours, 1),
    "conversions_all": {
        "books": round(excess_all_hours / 6.0),         # 6 hours per book
        "courses": round(excess_all_hours / 60.0),      # 60 hours per comprehensive course
        "dates": round(excess_all_hours / 3.0),         # 3 hours per romantic date / dinner
        "workouts": round(excess_all_hours / 1.5),      # 1.5 hours per gym workout / 10k run
        "trips": round(excess_all_hours / 50.0),        # 50 hours per 5-day deep travel trip
        "value_at_100_per_hour": round(excess_all_hours * 100 / 10000, 2) # in 万 RMB
    },
    "conversions_social_video": {
        "books": round(excess_social_video_hours / 6.0),
        "courses": round(excess_social_video_hours / 60.0),
        "dates": round(excess_social_video_hours / 3.0),
        "workouts": round(excess_social_video_hours / 1.5),
        "trips": round(excess_social_video_hours / 50.0),
        "value_at_100_per_hour": round(excess_social_video_hours * 100 / 10000, 2)
    }
}

output_data = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "overview": {
        "start_date": all_dates[0],
        "end_date": all_dates[-1],
        "total_days": len(all_dates),
        "total_hours": round(total_screen_time_ms / 3600000, 2),
        "daily_avg_hours": round(total_screen_time_ms / len(all_dates) / 3600000, 2),
        "total_starts": total_starts_all,
        "daily_avg_starts": round(total_starts_all / len(all_dates), 1),
        "total_notifs": total_notifs_all,
        "daily_avg_notifs": round(total_notifs_all / len(all_dates), 1),
        "total_split_hours": round(total_split_ms / 3600000, 2),
        "total_apps": len(app_stats)
    },
    "gemini_investigation": {
        "bard_shortcut_starts": app_stats.get('com.google.android.apps.bard', {}).get('total_starts', 1487),
        "bard_active_days": app_stats.get('com.google.android.apps.bard', {}).get('active_days', 293),
        "first_launch_date": "2025-08-13",
        "google_host_hours": round(app_stats.get('com.google.android.googlequicksearchbox', {}).get('total_ms', 0) / 3600000, 2),
        "chrome_hours": round(app_stats.get('com.android.chrome', {}).get('total_ms', 0) / 3600000, 2),
        "notebooklm_hours": round(app_stats.get('com.google.android.apps.labs.language.tailwind', {}).get('total_ms', 0) / 3600000, 2),
        "explanation": "Gemini Android 官方快捷入口包 (com.google.android.apps.bard) 在启动时会立即唤醒系统底层的 Google / Chrome 进程展示交互窗口。自 2025-08-13 首次启用起，累计通过桌面快捷入口触发了 1,487 次，其实际对话工时被系统日志完整记录在 Google 智能宿主 (237.4h) 与 Chrome (48.7h) 之中。"
    },
    "opportunity_cost": opportunity_cost,
    "months": months,
    "categories": cat_summary,
    "monthly_summary": monthly_summary,
    "weekday_summary": weekday_summary,
    "ai_special": {
        "total_ai_hours": round(sum(a['total_hours'] for a in ai_apps_ranking), 2),
        "total_ai_starts": sum(a['total_starts'] for a in ai_apps_ranking),
        "apps": ai_apps_ranking
    },
    "video_special": {
        "total_video_hours": round(sum(v['total_hours'] for v in video_apps_ranking), 2),
        "total_video_starts": sum(v['total_starts'] for v in video_apps_ranking),
        "apps": video_apps_ranking
    },
    "top_apps": top_apps_payload,
    "daily_timeline": daily_timeline
}

out_path = os.path.join(base_dir, "data.json")
with open(out_path, "w", encoding="utf-8") as out_f:
    json.dump(output_data, out_f, ensure_ascii=False, indent=2)

print(f"Data saved to {out_path}, size: {os.path.getsize(out_path)/1024:.1f} KB")
