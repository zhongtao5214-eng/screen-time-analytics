# -*- coding: utf-8 -*-
"""
Build daily_history.json for Gemini Spark / GitHub Automation
Updated with 100 RMB/hour wage
"""
import os, json, re
from collections import defaultdict
from datetime import datetime

base_dir = r"d:\桌面\测试\屏幕使用时间管理数据分析"
day_csv = os.path.join(base_dir, "AppUsage_day.csv")

date_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})")

daily_records = defaultdict(lambda: {
    'total_ms': 0.0,
    'starts': 0,
    'notifs': 0,
    'wechat_ms': 0.0,
    'douyin_ms': 0.0,
    'ai_ms': 0.0,
    'top_app': '',
    'top_app_ms': 0.0
})

ai_pkgs = ['chatgpt', 'openai', 'deepseek', 'nova', '豆包', 'kimi', 'moonshot', 'bard', 'googlequicksearchbox', 'tailwind', 'copilot']

with open(day_csv, 'r', encoding='utf-8-sig', errors='replace') as f:
    cur_date = None
    for line in f:
        l = line.strip()
        if not l: continue
        m = date_pattern.match(l)
        if m:
            cur_date = m.group(1)
            continue
        parts = l.split(',')
        if len(parts) >= 6:
            app_name = parts[1].strip()
            pkg = parts[2].strip()
            try: ms = float(parts[4])
            except: ms = 0.0
            try: starts = int(parts[5])
            except: starts = 0
            
            rec = daily_records[cur_date]
            if pkg == 'ALL':
                rec['total_ms'] = ms
                rec['starts'] = starts
            else:
                p_l = pkg.lower()
                n_l = app_name.lower()
                if 'tencent.mm' in p_l or '微信' in n_l:
                    rec['wechat_ms'] += ms
                elif 'aweme' in p_l or '抖音' in n_l:
                    rec['douyin_ms'] += ms
                elif any(k in p_l or k in n_l for k in ai_pkgs):
                    rec['ai_ms'] += ms
                
                if ms > rec['top_app_ms']:
                    rec['top_app_ms'] = ms
                    rec['top_app'] = app_name or pkg

history_by_mmdd = defaultdict(lambda: {
    'month_day': '',
    'records': []
})

user_hourly_wage = 100.0 # Updated to 100 RMB/hour
baseline_daily_allowance = 2.0 # hours/day

for d_str in sorted(daily_records.keys()):
    dt = datetime.strptime(d_str, "%Y-%m-%d")
    mmdd = dt.strftime("%m-%d")
    year = dt.strftime("%Y")
    
    rec = daily_records[d_str]
    screen_hours = round(rec['total_ms'] / 3600000, 2)
    wechat_hours = round(rec['wechat_ms'] / 3600000, 2)
    douyin_hours = round(rec['douyin_ms'] / 3600000, 2)
    ai_hours = round(rec['ai_ms'] / 3600000, 2)
    top_hours = round(rec['top_app_ms'] / 3600000, 2)
    
    excess_hours = max(0.0, round(screen_hours - baseline_daily_allowance, 2))
    cost_yuan = round(excess_hours * user_hourly_wage, 2)
    
    history_by_mmdd[mmdd]['month_day'] = mmdd
    history_by_mmdd[mmdd]['records'].append({
        'year': year,
        'date': d_str,
        'weekday': dt.strftime('%A'),
        'screen_hours': screen_hours,
        'unlock_starts': rec['starts'],
        'wechat_hours': wechat_hours,
        'douyin_hours': douyin_hours,
        'ai_hours': ai_hours,
        'top_app': rec['top_app'],
        'top_app_hours': top_hours,
        'excess_hours': excess_hours,
        'opportunity_loss_yuan': cost_yuan
    })

out_path = os.path.join(base_dir, "daily_history.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(history_by_mmdd, f, ensure_ascii=False, indent=2)

print(f"Updated daily_history.json with wage 100 at: {out_path}")
