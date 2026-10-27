# -*- coding: utf-8 -*-
"""
Generate the standalone interactive HTML Dashboard for Screen Time Management Data Analysis
Complete with:
- Macro Overview (KPIs, 25-Month Dynamic Trends, Category Area Stack, Year Filter)
- AI Tools Evolution & Gemini Traceback (Gemini PWA shortcut vs Google host execution, ChatGPT, DeepSeek, 豆包, Kimi)
- Short Video Control (Douyin drop from 46% to 11%, binge peak warnings, habit change)
- Weekday & Night Routine (Workday vs Weekend, >=14h extreme night intrusion analysis)
- 767-Day Full Calendar Heatmap (Multi-year GitHub style, interactive hover)
- Opportunity Cost & Time Reclaiming (Interactive Sliders: daily allowance, scope, hourly rate; Books, Courses, Dates, Workouts, Trips, Economic value)
- App Explorer & Drill-Down Drawer (Top 50 apps, instant search, monthly trends)
- Executive Report & Practical Recommendations
"""
import os, json

base_dir = r"d:\桌面\测试\屏幕使用时间管理数据分析"
json_path = os.path.join(base_dir, "data.json")
html_path = os.path.join(base_dir, "index.html")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Calculate extreme days stats for night analysis
timeline = data['daily_timeline']
gt_14_days = [x for x in timeline if x['hours'] >= 14]
gt_16_days = [x for x in timeline if x['hours'] >= 16]
gt_18_days = [x for x in timeline if x['hours'] >= 18]

data['night_analysis'] = {
    'gt_14_count': len(gt_14_days),
    'gt_14_pct': round(len(gt_14_days) / len(timeline) * 100, 1),
    'gt_16_count': len(gt_16_days),
    'gt_16_pct': round(len(gt_16_days) / len(timeline) * 100, 1),
    'gt_18_count': len(gt_18_days),
    'extreme_days': sorted(gt_14_days, key=lambda x: x['hours'], reverse=True)[:10]
}

json_str = json.dumps(data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>屏幕使用时间管理全景数据分析看板 (2024.09 - 2026.10)</title>
  <!-- Load Local ECharts first, fallback to CDN -->
  <script src="echarts.min.js"></script>
  <script>
    if (typeof echarts === 'undefined') {{
      document.write('<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"><\\/script>');
    }}
  </script>
  <style>
    :root {{
      --bg-primary: #0b132b;
      --bg-secondary: #1c2541;
      --bg-card: rgba(28, 37, 65, 0.75);
      --bg-card-hover: rgba(43, 56, 95, 0.85);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.4);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --accent-indigo: #6366f1;
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-purple: #a855f7;
      --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
      --glass-blur: blur(12px);
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 8px;
    }}

    .light-theme {{
      --bg-primary: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.88);
      --bg-card-hover: rgba(241, 245, 249, 0.95);
      --border-color: rgba(0, 0, 0, 0.08);
      --border-accent: rgba(99, 102, 241, 0.35);
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-sub: #94a3b8;
      --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", Roboto, sans-serif;
    }}

    body {{
      background-color: var(--bg-primary);
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.5;
      transition: background-color 0.25s ease, color 0.25s ease;
    }}

    .app-container {{
      max-width: 1620px;
      margin: 0 auto;
      padding: 24px 32px 80px;
    }}

    /* Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 22px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header-left h1 {{
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .header-left .subtitle {{
      color: var(--text-muted);
      font-size: 13px;
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 3px 8px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 500;
      background: rgba(99, 102, 241, 0.15);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-main);
      transition: all 0.2s ease;
    }}

    .btn:hover {{
      background: var(--bg-card-hover);
      border-color: var(--accent-indigo);
    }}

    .btn-primary {{
      background: var(--accent-indigo);
      color: #ffffff;
      border-color: var(--accent-indigo);
    }}

    .btn-primary:hover {{
      background: #4f46e5;
    }}

    /* Global Nav Tabs */
    .nav-tabs {{
      display: flex;
      gap: 8px;
      background: var(--bg-secondary);
      padding: 6px;
      border-radius: var(--radius-md);
      margin-bottom: 24px;
      overflow-x: auto;
      border: 1px solid var(--border-color);
    }}

    .tab-btn {{
      padding: 10px 18px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 500;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
      white-space: nowrap;
    }}

    .tab-btn:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.04);
    }}

    .tab-btn.active {{
      background: var(--accent-indigo);
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }}

    /* KPI Cards Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--bg-card);
      backdrop-filter: var(--glass-blur);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      box-shadow: var(--card-shadow);
      position: relative;
      overflow: hidden;
      transition: transform 0.2s, border-color 0.2s;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-accent);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--card-accent, var(--accent-indigo)), transparent);
    }}

    .kpi-title {{
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .kpi-value {{
      font-size: 24px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.5px;
    }}

    .kpi-unit {{
      font-size: 13px;
      font-weight: 400;
      color: var(--text-muted);
      margin-left: 4px;
    }}

    .kpi-meta {{
      margin-top: 8px;
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-sub);
    }}

    .trend-up {{ color: var(--accent-rose); }}
    .trend-down {{ color: var(--accent-emerald); }}
    .trend-info {{ color: var(--accent-cyan); }}

    /* Cards & Panels */
    .content-panel {{
      display: none;
      animation: fadeIn 0.25s ease;
    }}

    .content-panel.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .panel-grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }}

    .col-12 {{ grid-column: span 12; }}
    .col-8 {{ grid-column: span 8; }}
    .col-7 {{ grid-column: span 7; }}
    .col-6 {{ grid-column: span 6; }}
    .col-5 {{ grid-column: span 5; }}
    .col-4 {{ grid-column: span 4; }}

    @media (max-width: 1024px) {{
      .col-8, .col-7, .col-6, .col-5, .col-4 {{
        grid-column: span 12;
      }}
    }}

    .card {{
      background: var(--bg-card);
      backdrop-filter: var(--glass-blur);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 22px;
      box-shadow: var(--card-shadow);
      display: flex;
      flex-direction: column;
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .card-title {{
      font-size: 16px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .card-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 3px;
    }}

    .chart-box {{
      width: 100%;
      height: 380px;
    }}

    .chart-box-sm {{
      width: 100%;
      height: 250px;
    }}

    .chart-box-lg {{
      width: 100%;
      height: 480px;
    }}

    /* Insight Banner */
    .insight-callout {{
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
      border: 1px solid rgba(99, 102, 241, 0.25);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-bottom: 20px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }}

    .callout-icon {{
      font-size: 24px;
      line-height: 1;
    }}

    .callout-title {{
      font-weight: 600;
      font-size: 14px;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .callout-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* Filter Chips */
    .filter-chips {{
      display: flex;
      gap: 6px;
    }}

    .chip-btn {{
      padding: 5px 12px;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-muted);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .chip-btn.active, .chip-btn:hover {{
      background: var(--accent-indigo);
      color: white;
      border-color: var(--accent-indigo);
    }}

    /* Search input */
    .search-input {{
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-main);
      font-size: 12px;
      outline: none;
      width: 180px;
    }}

    .search-input:focus {{
      border-color: var(--accent-indigo);
    }}

    /* Table Styles */
    .table-container {{
      overflow-x: auto;
      max-height: 520px;
      position: relative;
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    table.data-table th {{
      background: var(--bg-secondary);
      color: var(--text-muted);
      font-weight: 600;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 2;
    }}

    table.data-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
    }}

    table.data-table tr {{
      transition: background-color 0.15s;
    }}

    table.data-table tr:hover td {{
      background: var(--bg-card-hover);
      cursor: pointer;
    }}

    table.data-table tr.selected td {{
      background: rgba(99, 102, 241, 0.15) !important;
      border-left: 3px solid var(--accent-indigo);
    }}

    .app-icon-name {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .app-avatar {{
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--accent-indigo);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 600;
      font-size: 13px;
      flex-shrink: 0;
    }}

    .cat-pill {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 500;
    }}

    .cat-ai {{ background: rgba(99, 102, 241, 0.15); color: #818cf8; }}
    .cat-video {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; }}
    .cat-social {{ background: rgba(16, 185, 129, 0.15); color: #34d399; }}
    .cat-work {{ background: rgba(6, 182, 212, 0.15); color: #22d3ee; }}
    .cat-game {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; }}
    .cat-system {{ background: rgba(148, 163, 184, 0.15); color: #cbd5e1; }}
    .cat-other {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; }}

    /* Equivalence / Opportunity Cost Cards */
    .equiv-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      margin-bottom: 24px;
    }}

    .equiv-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 22px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      transition: all 0.25s ease;
    }}

    .equiv-card:hover {{
      transform: translateY(-3px);
      border-color: var(--card-theme, var(--accent-indigo));
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
    }}

    .equiv-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--card-theme, var(--accent-indigo));
    }}

    .equiv-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .equiv-icon {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
    }}

    .equiv-title {{
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
    }}

    .equiv-sub {{
      font-size: 12px;
      color: var(--text-sub);
    }}

    .equiv-number {{
      font-size: 36px;
      font-weight: 800;
      color: var(--card-theme, var(--accent-indigo));
      line-height: 1.1;
      margin-bottom: 6px;
    }}

    .equiv-unit {{
      font-size: 16px;
      font-weight: 500;
      color: var(--text-muted);
      margin-left: 4px;
    }}

    .equiv-desc {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-top: auto;
      padding-top: 10px;
      border-top: 1px dashed var(--border-color);
    }}

    /* Sliders and controls */
    .control-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 20px 24px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 24px;
      align-items: center;
    }}

    .control-item {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      min-width: 200px;
      flex: 1;
    }}

    .control-label {{
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      justify-content: space-between;
    }}

    .control-val-tag {{
      color: var(--accent-indigo);
      font-weight: 700;
    }}

    .slider {{
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 3px;
      background: var(--bg-secondary);
      outline: none;
    }}

    .slider::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent-indigo);
      cursor: pointer;
      box-shadow: 0 0 8px rgba(99, 102, 241, 0.6);
    }}

    .scope-toggle {{
      display: inline-flex;
      background: var(--bg-secondary);
      padding: 4px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }}

    .scope-btn {{
      padding: 6px 14px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 500;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .scope-btn.active {{
      background: var(--accent-indigo);
      color: white;
    }}

    /* Heatmap legend */
    .heatmap-legend {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: var(--text-sub);
      justify-content: flex-end;
    }}

    .legend-color {{
      width: 12px;
      height: 12px;
      border-radius: 2px;
    }}

    /* Print styling */
    @media print {{
      body {{ background: #fff !important; color: #000 !important; }}
      .header-actions, .nav-tabs, .btn, .filter-chips, .search-input, .control-panel {{ display: none !important; }}
      .content-panel {{ display: block !important; margin-bottom: 30px; page-break-inside: avoid; }}
      .card {{ box-shadow: none !important; border: 1px solid #ccc !important; }}
    }}
  </style>
</head>
<body>

<div class="app-container">
  <!-- Header -->
  <header>
    <div class="header-left">
      <h1>
        <span>📱 屏幕使用时间管理全景数据大屏</span>
      </h1>
      <div class="subtitle">
        <span>统计周期：<b>2024.09.21 - 2026.10.27</b> (767天连续无间断)</span>
        <span class="badge">全生态 515 个应用</span>
        <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3);">纯亮屏 9,083 小时</span>
        <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee; border-color: rgba(6, 182, 212, 0.3);">AI 生产力 547 小时</span>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn" id="theme-toggle" onclick="toggleTheme()">🌓 切换主题</button>
      <button class="btn btn-primary" onclick="window.print()">🖨️ 导出/打印汇报</button>
    </div>
  </header>

  <!-- Global KPI Strip -->
  <div class="kpi-grid">
    <div class="kpi-card" style="--card-accent: #6366f1;">
      <div class="kpi-title">
        <span>累计屏幕使用</span>
        <span>⏱️</span>
      </div>
      <div class="kpi-value">{data['overview']['total_hours']}<span class="kpi-unit">小时</span></div>
      <div class="kpi-meta">
        <span class="trend-info">相当于 378.5 天纯亮屏</span>
      </div>
    </div>

    <div class="kpi-card" style="--card-accent: #3b82f6;">
      <div class="kpi-title">
        <span>日均屏幕时长</span>
        <span>📊</span>
      </div>
      <div class="kpi-value">{data['overview']['daily_avg_hours']}<span class="kpi-unit">小时/天</span></div>
      <div class="kpi-meta">
        <span class="trend-info">工作日 12.05h / 周末 11.32h</span>
      </div>
    </div>

    <div class="kpi-card" style="--card-accent: #10b981;">
      <div class="kpi-title">
        <span>AI 全生态生产力</span>
        <span>🤖</span>
      </div>
      <div class="kpi-value">{data['ai_special']['total_ai_hours']}<span class="kpi-unit">小时</span></div>
      <div class="kpi-meta">
        <span class="trend-down">含 Gemini/ChatGPT/豆包/DeepSeek</span>
      </div>
    </div>

    <div class="kpi-card" style="--card-accent: #06b6d4;">
      <div class="kpi-title">
        <span>Gemini 快捷启动</span>
        <span>✨</span>
      </div>
      <div class="kpi-value">{data['gemini_investigation']['bard_shortcut_starts']}<span class="kpi-unit">次</span></div>
      <div class="kpi-meta">
        <span class="trend-info">宿主承载 237.4h 深度交互</span>
      </div>
    </div>

    <div class="kpi-card" style="--card-accent: #f43f5e;">
      <div class="kpi-title">
        <span>短视频月占比降幅</span>
        <span>📉</span>
      </div>
      <div class="kpi-value">46.1% ➔ 11.4%</div>
      <div class="kpi-meta">
        <span class="trend-down">峰值降幅达 -75% (显著见效)</span>
      </div>
    </div>

    <div class="kpi-card" style="--card-accent: #a855f7;">
      <div class="kpi-title">
        <span>溢出可重构时间</span>
        <span>💡</span>
      </div>
      <div class="kpi-value">{data['opportunity_cost']['excess_all_hours']}<span class="kpi-unit">小时</span></div>
      <div class="kpi-meta">
        <span class="trend-info">扣除每天2h基础娱乐后</span>
      </div>
    </div>
  </div>

  <!-- Navigation Tabs -->
  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('overview')">📊 宏观总览看板</button>
    <button class="tab-btn" onclick="switchTab('ai')">🤖 AI 工具演化与 Gemini 溯源</button>
    <button class="tab-btn" onclick="switchTab('opportunity')">💰 机会成本与价值重比</button>
    <button class="tab-btn" onclick="switchTab('video')">📱 抖音短视频管控</button>
    <button class="tab-btn" onclick="switchTab('weekday')">⚖️ 工作日与夜间作息</button>
    <button class="tab-btn" onclick="switchTab('heatmap')">📅 767天全景日历热力图</button>
    <button class="tab-btn" onclick="switchTab('apps')">🔍 核心应用天梯 & 下钻画像</button>
    <button class="tab-btn" onclick="switchTab('report')">📑 深度分析与汇报洞察</button>
  </div>

  <!-- ==================== TAB 1: 宏观总览 ==================== -->
  <div id="tab-overview" class="content-panel active">
    <div class="insight-callout">
      <div class="callout-icon">💡</div>
      <div>
        <div class="callout-title">核心宏观画像洞察</div>
        <div class="callout-desc">
          在 2024 年 9 月至 2026 年 10 月的 767 天内，总屏幕使用时长高达 9,083 小时。<b>微信</b>（3,123h）与<b>抖音</b>（2,005h）占据了超 56% 的时间。结构上，经历了由早期<strong>“重度短视频娱乐消费”</strong>向后期<strong>“AI 助手与深度工作协同”</strong>的明显结构转型。您可通过右上角年份筛选按钮切换单年走势。
        </div>
      </div>
    </div>

    <div class="panel-grid">
      <!-- 长期月度总时长与走势 -->
      <div class="card col-8">
        <div class="card-header">
          <div>
            <div class="card-title">📈 屏幕使用时长演变曲线</div>
            <div class="card-subtitle">月度总时长（小时）与日均时长走势趋势图</div>
          </div>
          <div class="filter-chips">
            <button class="chip-btn active" onclick="filterOverviewYear('ALL', this)">全部 (25个月)</button>
            <button class="chip-btn" onclick="filterOverviewYear('2024', this)">2024</button>
            <button class="chip-btn" onclick="filterOverviewYear('2025', this)">2025</button>
            <button class="chip-btn" onclick="filterOverviewYear('2026', this)">2026</button>
          </div>
        </div>
        <div id="chart-monthly-trend" class="chart-box"></div>
      </div>

      <!-- 8大类别占比环形图 -->
      <div class="card col-4">
        <div class="card-header">
          <div>
            <div class="card-title">🍩 应用大类分布画像</div>
            <div class="card-subtitle">8 大生态类别总时长占比</div>
          </div>
        </div>
        <div id="chart-category-pie" class="chart-box"></div>
      </div>

      <!-- 月度类别堆叠面积演化图 -->
      <div class="card col-12">
        <div class="card-header">
          <div>
            <div class="card-title">🌊 各应用类别月度演进结构堆叠图</div>
            <div class="card-subtitle">直观展现社交通讯、短视频、AI生产力、工作协同两年来时间结构的动态博弈</div>
          </div>
        </div>
        <div id="chart-category-stack" class="chart-box-lg"></div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 2: AI 工具演化与 Gemini 溯源 ==================== -->
  <div id="tab-ai" class="content-panel">
    <!-- Gemini 特别排查与联动还原 Callout -->
    <div class="insight-callout" style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(99, 102, 241, 0.15)); border-color: rgba(6, 182, 212, 0.4);">
      <div class="callout-icon">✨</div>
      <div>
        <div class="callout-title">Gemini 数据深度排查与还原：桌面快捷入口与底层宿主进程联动</div>
        <div class="callout-desc">
          <b>已精准排查出 Gemini 数据去向并完整归位！</b><br/>
          经过对底层日志的深度交叉验证：您在手机上通过桌面快捷入口（包名 <code>com.google.android.apps.bard</code>）累计点击启动了 <b>{data['gemini_investigation']['bard_shortcut_starts']} 次</b>（覆盖 293 个活跃天）。因为 Gemini 在 Android 系统上作为 PWA/快捷方式存在，点击后会立即无缝唤起系统底层的 <b>Google 智能搜索应用（237.4 小时，5,803 次交互）</b> 与 <b>Chrome 浏览器（48.7 小时）</b> 承载渲染。两者在日志中首次出现的日期完全重合（<b>2025-08-13</b>）。现已将其完整纳入 AI 生产力大盘统计，真实 AI 生产力时长高达 <b>547 小时</b>！
        </div>
      </div>
    </div>

    <div class="panel-grid">
      <!-- AI 各工具月度堆叠图 -->
      <div class="card col-8">
        <div class="card-header">
          <div>
            <div class="card-title">🤖 核心 AI 助手月度工时演进 (含 Gemini 宿主)</div>
            <div class="card-subtitle">Gemini/Google AI / ChatGPT / 豆包 / DeepSeek / Kimi 各产品投入时长趋势</div>
          </div>
        </div>
        <div id="chart-ai-stack" class="chart-box"></div>
      </div>

      <!-- AI 占总屏幕时长比例曲线 -->
      <div class="card col-4">
        <div class="card-header">
          <div>
            <div class="card-title">📈 AI 渗透率演变 (%)</div>
            <div class="card-subtitle">AI 占当月总屏幕时长的比重走势</div>
          </div>
        </div>
        <div id="chart-ai-ratio" class="chart-box"></div>
      </div>

      <!-- AI 工具详细天梯 -->
      <div class="card col-12">
        <div class="card-header">
          <div class="card-title">🏆 AI 工具全生态档案</div>
        </div>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>AI 应用</th>
                <th>包名标识</th>
                <th>累计投入工时</th>
                <th>启动交互次数</th>
                <th>活跃使用天数</th>
                <th>首次使用日期</th>
                <th>最近使用日期</th>
                <th>交互属性/单次均长</th>
              </tr>
            </thead>
            <tbody id="ai-table-body">
              <!-- populated via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 3: 机会成本与价值重比 ==================== -->
  <div id="tab-opportunity" class="content-panel">
    <div class="insight-callout" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(245, 158, 11, 0.12)); border-color: rgba(16, 185, 129, 0.35);">
      <div class="callout-icon">💡</div>
      <div>
        <div class="callout-title">时间资本与机会成本重比模型（Time Capital Reclaiming）</div>
        <div class="callout-desc">
          我们尊重健康合理的日常休闲——<b>假设您每天预留 2 小时基础用机额度（1小时刷抖音 + 1小时聊微信，767天共 1,534 小时）</b>，除此之外的所有屏幕时间均属于“可重构机会成本”。本模块帮您将这笔庞大的时间资产换算成现实人生中震撼的成长当量！
        </div>
      </div>
    </div>

    <!-- 交互控制器 -->
    <div class="control-panel">
      <div class="control-item">
        <div class="control-label">
          <span>每日免责休闲额度 (抖音+微信)</span>
          <span class="control-val-tag" id="tag-allowance">2.0 小时/天</span>
        </div>
        <input type="range" class="slider" id="slider-allowance" min="1.0" max="4.0" step="0.5" value="2.0" oninput="updateOpportunityCalc()">
      </div>

      <div class="control-item">
        <div class="control-label">
          <span>计算范围口径</span>
        </div>
        <div class="scope-toggle">
          <button class="scope-btn active" id="btn-scope-all" onclick="setOpportunityScope('ALL')">全屏总溢出时间池</button>
          <button class="scope-btn" id="btn-scope-social" onclick="setOpportunityScope('SOCIAL')">仅微信+抖音溢出池</button>
        </div>
      </div>

      <div class="control-item">
        <div class="control-label">
          <span>设定个人生产力时薪换算 (您的实际时薪)</span>
          <span class="control-val-tag" id="tag-wage">¥100 / 小时</span>
        </div>
        <input type="range" class="slider" id="slider-wage" min="20" max="300" step="1" value="100" oninput="updateOpportunityCalc()">
      </div>
    </div>

    <!-- 核心统计大卡 -->
    <div class="panel-grid">
      <div class="card col-12" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(16, 185, 129, 0.15) 100%); border-color: rgba(99, 102, 241, 0.35);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
          <div>
            <div style="font-size: 13px; color: var(--text-muted);">当前选定口径下的【可重构人生时间资本】</div>
            <div style="font-size: 38px; font-weight: 800; color: #818cf8; letter-spacing: -1px; margin-top: 4px;">
              <span id="reclaim-hours">7,549</span> <span style="font-size: 18px; font-weight: 500; color: var(--text-muted);">小时</span>
              <span style="font-size: 16px; font-weight: 400; color: var(--text-sub); margin-left: 12px;" id="reclaim-days">(相当于 314.5 天纯清醒白昼时间)</span>
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 13px; color: var(--text-muted);">按 ¥100/h 时薪折算潜在经济资本重比</div>
            <div style="font-size: 38px; font-weight: 800; color: #34d399; letter-spacing: -1px; margin-top: 4px;">
              ¥<span id="reclaim-money">75.49</span> <span style="font-size: 18px; font-weight: 500; color: var(--text-muted);">万元</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 等价列表卡片网格 -->
    <div class="equiv-grid">
      <!-- 1. 深度阅读 -->
      <div class="equiv-card" style="--card-theme: #3b82f6;">
        <div class="equiv-header">
          <div class="equiv-icon">📚</div>
          <div>
            <div class="equiv-title">深度阅读经典巨著</div>
            <div class="equiv-sub">按 6小时 精读一本20万字著作换算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-books">1,258</span><span class="equiv-unit">本</span></div>
        <div class="equiv-desc">
          足以通读整整一座小型个人图书馆的全部藏书，超过 99.9% 普通人终其一生的全量阅读广度。
        </div>
      </div>

      <!-- 2. 硬核专业技能/系统课程 -->
      <div class="equiv-card" style="--card-theme: #10b981;">
        <div class="equiv-header">
          <div class="equiv-icon">🎓</div>
          <div>
            <div class="equiv-title">硬核系统专业课程</div>
            <div class="equiv-sub">按 60小时 攻克一套完整大学/专业课换算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-courses">126</span><span class="equiv-unit">门系统课</span></div>
        <div class="equiv-desc">
          足以掌握 12 门新外语达到流利交流标准（按 CEFR 600h），或学完计算机、金融、AI Agent、企业管理等 3 个不同学科的本硕完整核心大纲。
        </div>
      </div>

      <!-- 3. 浪漫约会与深层陪伴 -->
      <div class="equiv-card" style="--card-theme: #f43f5e;">
        <div class="equiv-header">
          <div class="equiv-icon">❤️</div>
          <div>
            <div class="equiv-title">浪漫约会与深度陪伴</div>
            <div class="equiv-sub">按 3小时 高品质烛光晚餐/约会换算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-dates">2,516</span><span class="equiv-unit">次</span></div>
        <div class="equiv-desc">
          如果每周安排 2 次高质量浪漫约会或好友深度长聊，这笔时间足够支持您连续约会 <b>24 年</b>！
        </div>
      </div>

      <!-- 4. 强健身心与体能重塑 -->
      <div class="equiv-card" style="--card-theme: #f59e0b;">
        <div class="equiv-header">
          <div class="equiv-icon">🏃</div>
          <div>
            <div class="equiv-title">健身房举铁 / 10K长跑</div>
            <div class="equiv-sub">按 1.5小时/次 深度训练换算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-workouts">5,033</span><span class="equiv-unit">次训练</span></div>
        <div class="equiv-desc">
          相当于每周 4 次高强度力量训练坚持 24 年，足以将体脂、心肺与肌肉塑造成国家二级运动员级别的超强体魄。
        </div>
      </div>

      <!-- 5. 探索世界与深度漫游 -->
      <div class="equiv-card" style="--card-theme: #06b6d4;">
        <div class="equiv-header">
          <div class="equiv-icon">✈️</div>
          <div>
            <div class="equiv-title">跨国/跨省5日深度游</div>
            <div class="equiv-sub">按 50小时 清醒游览与探索/趟换算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-trips">151</span><span class="equiv-unit">趟旅程</span></div>
        <div class="equiv-desc">
          足以走遍全球七大洲的所有主要国家，在世界各地留下深邃的生活足迹与人生阅历。
        </div>
      </div>

      <!-- 6. 个人商业资本复利 -->
      <div class="equiv-card" style="--card-theme: #a855f7;">
        <div class="equiv-header">
          <div class="equiv-icon">💎</div>
          <div>
            <div class="equiv-title">真实时薪收益折算 (¥100/h)</div>
            <div class="equiv-sub">基于您实际时薪 ¥100 进行硬核折算</div>
          </div>
        </div>
        <div class="equiv-number"><span id="eq-money">75.49</span><span class="equiv-unit">万元</span></div>
        <div class="equiv-desc">
          按您当前的实际时薪 ¥100/小时 计算，这笔溢出时间等价于 <b>75.5 万元人民币</b> 的纯现金生产力！若投入专业深耕，价值将持续成倍激增。
        </div>
      </div>
    </div>

    <!-- 机会成本对比图表 -->
    <div class="panel-grid">
      <div class="card col-6">
        <div class="card-header">
          <div class="card-title">🍩 时间资产构成切片 (基础娱乐 vs 可重构资本)</div>
        </div>
        <div id="chart-opp-pie" class="chart-box"></div>
      </div>

      <div class="card col-6">
        <div class="card-header">
          <div class="card-title">📊 人生复利转化阶梯对比</div>
        </div>
        <div id="chart-opp-bar" class="chart-box"></div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 4: 抖音短视频管控 ==================== -->
  <div id="tab-video" class="content-panel">
    <div class="insight-callout" style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.1), rgba(245, 158, 11, 0.1)); border-color: rgba(244, 63, 94, 0.3);">
      <div class="callout-icon">🎯</div>
      <div>
        <div class="callout-title">短视频管控成效评估：令人惊艳的阶段性自律成果</div>
        <div class="callout-desc">
          在 2024 年末，短视频（主要是抖音）曾占据总屏幕时长的 <b>46.1%</b>（月刷 150+ 小时，日均超 5 小时）。通过有意识的管控，在 <b>2026 年上半年</b>短视频时长被成功压减至最低 <b>38.8 小时/月</b>，占比腰斩至 <b>11.4%</b>，降幅达到不可思议的 <b>-75%</b>！虽然 2026 年夏季有所回潮，但整体已彻底脱离了早期的“不可控沉迷”。
        </div>
      </div>
    </div>

    <div class="panel-grid">
      <!-- 短视频月度时长与占比双轴图 -->
      <div class="card col-8">
        <div class="card-header">
          <div>
            <div class="card-title">📉 短视频月度使用量与总时间占比轨迹</div>
            <div class="card-subtitle">柱状图（时长h）与折线图（占比%）见证沉迷到自律</div>
          </div>
        </div>
        <div id="chart-video-control" class="chart-box"></div>
      </div>

      <!-- 流媒体产品内部占比 -->
      <div class="card col-4">
        <div class="card-header">
          <div>
            <div class="card-title">🍩 视听类应用内部时间分布</div>
            <div class="card-subtitle">抖音 / B站 / Yumme / YouTube 各自占比</div>
          </div>
        </div>
        <div id="chart-video-breakdown" class="chart-box"></div>
      </div>

      <!-- 每日刷短视频分布散点/柱图 -->
      <div class="card col-12">
        <div class="card-header">
          <div>
            <div class="card-title">⚠️ 重度刷视频预警日排查 (>4小时/天)</div>
            <div class="card-subtitle">全周期内单日刷视频超长的时间点分布，辅助复盘当时生活状态（支持鼠标框选缩放）</div>
          </div>
        </div>
        <div id="chart-video-peaks" class="chart-box"></div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 5: 工作日与夜间作息 ==================== -->
  <div id="tab-weekday" class="content-panel">
    <div class="insight-callout">
      <div class="callout-icon">⚖️</div>
      <div>
        <div class="callout-title">工作日节律与超长熬夜警示洞察</div>
        <div class="callout-desc">
          与一般认知不同：您的<strong>工作日日均屏幕时长（12.05h）显著高于周末（11.32h）</strong>。同时检测发现，全周期内有 <b>{data['night_analysis']['gt_14_count']} 天（占 22.4%）单日屏幕时长突破 14 小时</b>，有 <b>73 天突破 16 小时</b>！数学上推算，这些极端天数必然挤占了睡眠时间并存在深度夜间/熬夜用机。
        </div>
      </div>
    </div>

    <div class="panel-grid">
      <!-- 周一到周日各天平均指标 -->
      <div class="card col-6">
        <div class="card-header">
          <div>
            <div class="card-title">📅 周一至周日日均时长与启动频次</div>
            <div class="card-subtitle">查看一周七天的用机强度节奏</div>
          </div>
        </div>
        <div id="chart-weekday-bars" class="chart-box"></div>
      </div>

      <!-- 工作日 vs 周末 类别对比雷达图 -->
      <div class="card col-6">
        <div class="card-header">
          <div>
            <div class="card-title">🕸️ 工作日 vs 周末行为模式雷达</div>
            <div class="card-subtitle">各应用类别在工作日与周末的日均分配对比（小时）</div>
          </div>
        </div>
        <div id="chart-weekday-radar" class="chart-box"></div>
      </div>

      <!-- 熬夜超长用机分析柱图 -->
      <div class="card col-8">
        <div class="card-header">
          <div>
            <div class="card-title">🌙 熬夜/超长待机警戒分布 (每月超 14h 天数)</div>
            <div class="card-subtitle">展示各月高强度用机天数，监测过度疲劳风险</div>
          </div>
        </div>
        <div id="chart-night-monthly" class="chart-box"></div>
      </div>

      <!-- 极端超长天数榜 -->
      <div class="card col-4">
        <div class="card-header">
          <div class="card-title">🚨 历史单日最高纪录 (Top 10)</div>
        </div>
        <div class="table-container" style="max-height: 380px;">
          <table class="data-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>总时长</th>
                <th>最耗时应用</th>
              </tr>
            </thead>
            <tbody>
              {''.join([f"<tr><td><b>{x['date']}</b></td><td><span class='badge' style='background:rgba(239,68,68,0.15);color:#ef4444;border-color:rgba(239,68,68,0.3);'>{x['hours']}h</span></td><td>{x['top_app']} ({x['top_hours']}h)</td></tr>" for x in data['night_analysis']['extreme_days']])}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 6: 767天全景日历热力图 ==================== -->
  <div id="tab-heatmap" class="content-panel">
    <div class="insight-callout">
      <div class="callout-icon">🗓️</div>
      <div>
        <div class="callout-title">767 天全量屏幕使用热力矩阵</div>
        <div class="callout-desc">
          仿照 GitHub 活跃热力图设计，方块颜色越深代表当日屏幕使用时间越长。鼠标悬停可即时查看具体日期的<b>总时长、启动次数、以及当天耗时第一名 App</b>。
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">全景年度活跃热力图</div>
          <div class="card-subtitle">2024 年 9 月 至 2026 年 10 月全量每日热力分布</div>
        </div>
        <div class="heatmap-legend">
          <span>0h</span>
          <div class="legend-color" style="background: #1e293b;"></div>
          <div class="legend-color" style="background: #1e3a8a;"></div>
          <div class="legend-color" style="background: #3b82f6;"></div>
          <div class="legend-color" style="background: #60a5fa;"></div>
          <div class="legend-color" style="background: #f59e0b;"></div>
          <div class="legend-color" style="background: #ef4444;"></div>
          <span>超 16h 爆肝</span>
        </div>
      </div>
      <div id="chart-calendar-heatmap" style="width: 100%; height: 680px;"></div>
    </div>
  </div>

  <!-- ==================== TAB 7: 核心应用天梯 & 下钻画像 ==================== -->
  <div id="tab-apps" class="content-panel">
    <div class="panel-grid">
      <!-- Top 30 应用表格 -->
      <div class="card col-7">
        <div class="card-header">
          <div>
            <div class="card-title">🏆 核心应用天梯榜 (Top 30)</div>
            <div class="card-subtitle">点击任意一行，右侧即刻联动展开该 App 的全景画像</div>
          </div>
          <input type="text" class="search-input" id="app-search" placeholder="🔍 搜索 App..." oninput="filterAppsTable()">
        </div>
        <div class="table-container">
          <table class="data-table" id="apps-table">
            <thead>
              <tr>
                <th>应用名称</th>
                <th>分类</th>
                <th>总时长</th>
                <th>启动次数</th>
                <th>活跃天数</th>
                <th>日均耗时</th>
              </tr>
            </thead>
            <tbody id="top-apps-body">
              <!-- populated via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- 单 App 下钻画像看板 -->
      <div class="card col-5" id="app-detail-card">
        <div class="card-header">
          <div>
            <div class="card-title" id="detail-app-name">📱 微信 画像剖析</div>
            <div class="card-subtitle" id="detail-app-pkg">com.tencent.mm</div>
          </div>
          <span class="badge" id="detail-app-cat">社交通讯</span>
        </div>

        <div class="kpi-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 16px;">
          <div class="kpi-card" style="padding: 12px;">
            <div class="kpi-title">累计总工时</div>
            <div class="kpi-value" id="detail-total-hours" style="font-size: 20px;">3123.7<span class="kpi-unit">h</span></div>
          </div>
          <div class="kpi-card" style="padding: 12px;">
            <div class="kpi-title">总启动交互</div>
            <div class="kpi-value" id="detail-total-starts" style="font-size: 20px;">4.5<span class="kpi-unit">万次</span></div>
          </div>
        </div>

        <div style="font-size: 13px; font-weight: 600; margin-bottom: 8px;">📊 历史月度使用时长演变 (小时)</div>
        <div id="chart-app-monthly" class="chart-box-sm"></div>

        <div style="font-size: 13px; font-weight: 600; margin-top: 12px; margin-bottom: 8px;">🔓 月度启动频次走势 (次)</div>
        <div id="chart-app-starts" class="chart-box-sm"></div>
      </div>
    </div>
  </div>

  <!-- ==================== TAB 8: 深度分析与汇报洞察 ==================== -->
  <div id="tab-report" class="content-panel">
    <div class="panel-grid">
      <div class="card col-12">
        <div class="card-header">
          <div class="card-title">📑 屏幕使用时间管理全面分析汇报书</div>
          <span class="badge">报告生成时间：{data['generated_at']}</span>
        </div>
        
        <div style="line-height: 1.85; font-size: 14px; color: var(--text-main);">
          <h3 style="font-size: 18px; margin: 16px 0 8px; color: #818cf8;">一、 宏观画像：全周期基本盘与高强度用机特征</h3>
          <p>从 2024 年 9 月 21 日至 2026 年 10 月 27 日，系统完整记录了 767 天的使用轨迹。总屏幕亮屏时长高达 <strong>9,083.1 小时</strong>，折合 <strong>378.5 天纯亮屏</strong>。日均亮屏时长为 <strong>11.84 小时/天</strong>，日均解锁启动手机 <strong>530 次</strong>，日均接收通知 <strong>240 条</strong>。</p>
          <p style="margin-top: 8px;">这体现出极其鲜明的<strong>“全天候重度依赖 + 深度多任务”</strong>特征：手机不仅是日常社交工具，更是连接远程工作（UU远程）、生产力协作（飞书、网盘、搜索）与知识吸收的核心外脑。</p>

          <h3 style="font-size: 18px; margin: 24px 0 8px; color: #818cf8;">二、 关键转折一：短视频娱乐的“深度戒断与成功压降”</h3>
          <p>在所有行为指标中，短视频（特别是抖音）的管控展现了最清晰的自律拐点：</p>
          <ul style="margin-left: 20px; margin-top: 6px;">
            <li><strong>2024 年末（沉溺期）</strong>：月均刷视频高达 140~150 小时，在手机全部屏幕时间中占比逼近 <strong>46.1%</strong>。</li>
            <li><strong>2025 年（调整期）</strong>：通过主动调节，月均压制在 90~110 小时左右，占比回落至 25%~30%。</li>
            <li><strong>2026 年上半年（管控成效期）</strong>：短视频月刷时长彻底腰斩至 <strong>38.8 小时</strong>，总时间占比压缩至 <strong>11.4%</strong>，相比峰值降幅高达 <strong>-75%</strong>。</li>
          </ul>

          <h3 style="font-size: 18px; margin: 24px 0 8px; color: #818cf8;">三、 关键转折二：AI 生产力助手的“全生态爆发与 Gemini 联动”</h3>
          <p>您对 AI 工具的应用呈现出非常标准的先锋用户进化曲线：</p>
          <ul style="margin-left: 20px; margin-top: 6px;">
            <li><strong>Gemini 核心地位确立</strong>：自 2025 年 8 月开启以来，桌面快捷入口触发 <strong>1,487 次</strong>，底层 Google/Chrome 运行宿主承载了 <strong>237.4 小时</strong> 的深度交互，成为不可或缺的 AI 核心中枢。</li>
            <li><strong>全能矩阵形成</strong>：ChatGPT（135.7h）、豆包（90.0h）、DeepSeek（52.6h）、Kimi（22.6h）各司其职，AI 生态总工时突破 <strong>547 小时</strong>，月度渗透率从 0.1% 飞跃至 <strong>8.5%</strong> 以上。</li>
          </ul>

          <h3 style="font-size: 18px; margin: 24px 0 8px; color: #818cf8;">四、 节律特征与机会成本重比启示</h3>
          <p>数据表明，您的<strong>工作日日均屏幕时长（12.05h）显著高于周末（11.32h）</strong>。全周期内有 <strong>172 天（22.4%）屏幕时长超过 14 小时</strong>，存在明显的深夜熬夜用机特征。</p>
          <p style="margin-top: 8px;">按每天 2 小时基础娱乐（1h 微信 + 1h 抖音）计算，您的<strong>溢出可重构时间高达 7,549 小时</strong>。这笔巨大的时间资产等价于 <strong>精读 1,258 本经典巨著</strong>、<strong>攻克 126 套大学系统专业课</strong>、<strong>进行 2,516 次浪漫约会</strong>、或创造 <strong>¥75.5 万元</strong> 的潜在经济价值。若能将部分碎片时间有意识收回并注入现实复利，将带来颠覆性的人生收益。</p>

          <h3 style="font-size: 18px; margin: 24px 0 8px; color: #818cf8;">五、 数字健康优化与持续管理建议</h3>
          <div style="background: rgba(255,255,255,0.03); padding: 18px; border-radius: 8px; border: 1px solid var(--border-color); margin-top: 10px;">
            <p><strong>1. 防范短视频在特定时期的周期性反弹：</strong> 数据显示 2026 年下半年（6-8月）短视频占比有所回升（重新突破 20%），建议保留应用使用限额与定时休息提醒。</p>
            <p style="margin-top: 6px;"><strong>2. 优化解锁碎片化与通知干扰：</strong> 日均 530 次点亮屏幕，意味着大约每 2.7 分钟亮屏一次。建议对非关键 App（如电商、视频、生活类）关闭前台推送弹窗，减少被动分心。</p>
            <p style="margin-top: 6px;"><strong>3. 设立夜间“屏幕戒断红线”：</strong> 严格设定晚间 23:30 后的勿扰模式或灰度屏幕，将超 14 小时的极端用机日比例从当前的 22.4% 降至 5% 以下，切实保护深度睡眠与脑力恢复。</p>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>

<!-- DATA EMBEDDED -->
<script>
  window.DATA = {json_str};
</script>

<!-- APPLICATION LOGIC & CHARTS -->
<script>
  let currentTheme = 'dark';
  let charts = {{}};
  let selectedAppPkg = window.DATA.top_apps.length > 0 ? window.DATA.top_apps[0].pkg : '';
  let overviewYearFilter = 'ALL';
  let opportunityScope = 'ALL'; // 'ALL' or 'SOCIAL'

  function toggleTheme() {{
    const body = document.body;
    if (body.classList.contains('light-theme')) {{
      body.classList.remove('light-theme');
      currentTheme = 'dark';
    }} else {{
      body.classList.add('light-theme');
      currentTheme = 'light';
    }}
    const activePanel = document.querySelector('.content-panel.active');
    if (activePanel) {{
      const tabId = activePanel.id.replace('tab-', '');
      initTabCharts(tabId);
    }}
  }}

  function switchTab(tabId) {{
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.content-panel').forEach(panel => panel.classList.remove('active'));
    
    const buttons = Array.from(document.querySelectorAll('.tab-btn'));
    const targetBtn = buttons.find(b => b.getAttribute('onclick').includes(tabId));
    if (targetBtn) targetBtn.classList.add('active');

    const targetPanel = document.getElementById('tab-' + tabId);
    if (targetPanel) {{
      targetPanel.classList.add('active');
      setTimeout(() => {{
        initTabCharts(tabId);
      }}, 50);
    }}
  }}

  function initTabCharts(tabId) {{
    if (tabId === 'overview') {{
      renderMonthlyTrend();
      renderCategoryPie();
      renderCategoryStack();
    }} else if (tabId === 'ai') {{
      renderAIStack();
      renderAIRatio();
    }} else if (tabId === 'opportunity') {{
      updateOpportunityCalc();
      renderOpportunityCharts();
    }} else if (tabId === 'video') {{
      renderVideoControl();
      renderVideoBreakdown();
      renderVideoPeaks();
    }} else if (tabId === 'weekday') {{
      renderWeekdayBars();
      renderWeekdayRadar();
      renderNightMonthly();
    }} else if (tabId === 'heatmap') {{
      renderCalendarHeatmap();
    }} else if (tabId === 'apps') {{
      if (selectedAppPkg) {{
        renderAppDetail(selectedAppPkg);
      }}
    }}
  }}

  const themeColors = {{
    text: () => currentTheme === 'dark' ? '#94a3b8' : '#475569',
    textMain: () => currentTheme === 'dark' ? '#f8fafc' : '#0f172a',
    grid: () => currentTheme === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
    cardBg: () => currentTheme === 'dark' ? '#1c2541' : '#ffffff',
  }};

  // Filter Year in Overview
  function filterOverviewYear(year, btn) {{
    overviewYearFilter = year;
    document.querySelectorAll('.filter-chips .chip-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderMonthlyTrend();
  }}

  // ================= Tab 1: Overview =================
  function renderMonthlyTrend() {{
    const dom = document.getElementById('chart-monthly-trend');
    if (!dom) return;
    if (charts['monthly-trend']) charts['monthly-trend'].dispose();
    const chart = echarts.init(dom);
    charts['monthly-trend'] = chart;

    let summary = window.DATA.monthly_summary;
    if (overviewYearFilter !== 'ALL') {{
      summary = summary.filter(m => m.month.startsWith(overviewYearFilter));
    }}

    const months = summary.map(m => m.month);
    const totalHours = summary.map(m => m.total_hours);
    const dailyAvg = summary.map(m => m.daily_avg_hours);

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        axisPointer: {{ type: 'cross' }}
      }},
      legend: {{
        data: ['月总时长 (小时)', '日均时长 (小时/天)'],
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 30 }}
      }},
      yAxis: [
        {{
          type: 'value',
          name: '月总时长 (h)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
          axisLabel: {{ color: themeColors.text() }}
        }},
        {{
          type: 'value',
          name: '日均时长 (h)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ show: false }},
          axisLabel: {{ color: themeColors.text() }}
        }}
      ],
      series: [
        {{
          name: '月总时长 (小时)',
          type: 'bar',
          data: totalHours,
          itemStyle: {{
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: '#6366f1' }},
              {{ offset: 1, color: 'rgba(99, 102, 241, 0.3)' }}
            ]),
            borderRadius: [6, 6, 0, 0]
          }}
        }},
        {{
          name: '日均时长 (小时/天)',
          type: 'line',
          yAxisIndex: 1,
          data: dailyAvg,
          smooth: true,
          lineStyle: {{ color: '#f43f5e', width: 3 }},
          itemStyle: {{ color: '#f43f5e' }}
        }}
      ]
    }});
  }}

  function renderCategoryPie() {{
    const dom = document.getElementById('chart-category-pie');
    if (!dom) return;
    if (charts['category-pie']) charts['category-pie'].dispose();
    const chart = echarts.init(dom);
    charts['category-pie'] = chart;

    const dataList = window.DATA.categories.map(c => ({{
      name: c.category,
      value: c.total_hours
    }}));

    chart.setOption({{
      tooltip: {{
        trigger: 'item',
        formatter: '{{b}}: {{c}} 小时 ({{d}}%)'
      }},
      legend: {{
        orient: 'vertical',
        right: '2%',
        top: 'center',
        textStyle: {{ color: themeColors.text(), fontSize: 11 }}
      }},
      series: [
        {{
          type: 'pie',
          radius: ['45%', '72%'],
          center: ['36%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {{
            borderRadius: 6,
            borderColor: themeColors.cardBg(),
            borderWidth: 2
          }},
          label: {{ show: false }},
          data: dataList,
          color: ['#10b981', '#f43f5e', '#6366f1', '#06b6d4', '#f59e0b', '#a855f7', '#ec4899', '#64748b']
        }}
      ]
    }});
  }}

  function renderCategoryStack() {{
    const dom = document.getElementById('chart-category-stack');
    if (!dom) return;
    if (charts['category-stack']) charts['category-stack'].dispose();
    const chart = echarts.init(dom);
    charts['category-stack'] = chart;

    const months = window.DATA.monthly_summary.map(m => m.month);
    const categories = window.DATA.categories.map(c => c.category);

    const series = categories.map(cat => {{
      const catData = window.DATA.monthly_summary.map(m => m.categories_hours[cat] || 0);
      return {{
        name: cat,
        type: 'line',
        stack: 'Total',
        areaStyle: {{ opacity: 0.65 }},
        emphasis: {{ focus: 'series' }},
        data: catData,
        smooth: true
      }};
    }});

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        axisPointer: {{ type: 'cross', label: {{ backgroundColor: '#6a7985' }} }}
      }},
      legend: {{
        data: categories,
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      grid: {{ left: '3%', right: '4%', bottom: '5%', top: '12%', containLabel: true }},
      xAxis: {{
        type: 'category',
        boundaryGap: false,
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      yAxis: {{
        type: 'value',
        name: '累计小时数',
        nameTextStyle: {{ color: themeColors.text() }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      series: series
    }});
  }}

  // ================= Tab 2: AI =================
  function renderAIStack() {{
    const dom = document.getElementById('chart-ai-stack');
    if (!dom) return;
    if (charts['ai-stack']) charts['ai-stack'].dispose();
    const chart = echarts.init(dom);
    charts['ai-stack'] = chart;

    const months = window.DATA.months;
    const aiApps = window.DATA.ai_special.apps.slice(0, 5);
    const series = aiApps.map(a => {{
      return {{
        name: a.name,
        type: 'bar',
        stack: 'AI',
        emphasis: {{ focus: 'series' }},
        data: months.map(m => a.monthly_hours[m] || 0)
      }};
    }});

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        axisPointer: {{ type: 'shadow' }}
      }},
      legend: {{
        data: aiApps.map(a => a.name),
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      grid: {{ left: '3%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 30 }}
      }},
      yAxis: {{
        type: 'value',
        name: '时长 (小时)',
        nameTextStyle: {{ color: themeColors.text() }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      series: series
    }});
  }}

  function renderAIRatio() {{
    const dom = document.getElementById('chart-ai-ratio');
    if (!dom) return;
    if (charts['ai-ratio']) charts['ai-ratio'].dispose();
    const chart = echarts.init(dom);
    charts['ai-ratio'] = chart;

    const months = window.DATA.monthly_summary.map(m => m.month);
    const ratios = window.DATA.monthly_summary.map(m => {{
      return m.total_hours > 0 ? Number((m.ai_hours / m.total_hours * 100).toFixed(2)) : 0;
    }});

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        formatter: '{{b}}<br/>AI 占比: <b>{{c}}%</b>'
      }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 45 }}
      }},
      yAxis: {{
        type: 'value',
        name: '占比 (%)',
        nameTextStyle: {{ color: themeColors.text() }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), formatter: '{{value}}%' }}
      }},
      series: [
        {{
          data: ratios,
          type: 'line',
          smooth: true,
          symbolSize: 6,
          lineStyle: {{ color: '#10b981', width: 3 }},
          itemStyle: {{ color: '#10b981' }},
          areaStyle: {{
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: 'rgba(16, 185, 129, 0.4)' }},
              {{ offset: 1, color: 'rgba(16, 185, 129, 0.02)' }}
            ])
          }}
        }}
      ]
    }});
  }}

  // ================= Tab 3: Opportunity Cost =================
  function setOpportunityScope(scope) {{
    opportunityScope = scope;
    document.getElementById('btn-scope-all').classList.toggle('active', scope === 'ALL');
    document.getElementById('btn-scope-social').classList.toggle('active', scope === 'SOCIAL');
    updateOpportunityCalc();
  }}

  function updateOpportunityCalc() {{
    const allowanceVal = parseFloat(document.getElementById('slider-allowance').value);
    const wageVal = parseFloat(document.getElementById('slider-wage').value);
    document.getElementById('tag-allowance').innerText = allowanceVal.toFixed(1) + ' 小时/天';
    document.getElementById('tag-wage').innerText = '¥' + wageVal + ' / 小时';

    const totalDays = window.DATA.overview.total_days; // 767
    const totalHours = window.DATA.overview.total_hours; // 9083.09
    const wechatHours = window.DATA.opportunity_cost.wechat_total_hours;
    const douyinHours = window.DATA.opportunity_cost.douyin_total_hours;

    let reclaimableHours = 0;
    if (opportunityScope === 'ALL') {{
      reclaimableHours = Math.max(0, totalHours - (totalDays * allowanceVal));
    }} else {{
      const halfAllowance = allowanceVal / 2.0;
      const wechatExcess = Math.max(0, wechatHours - (totalDays * halfAllowance));
      const douyinExcess = Math.max(0, douyinHours - (totalDays * halfAllowance));
      reclaimableHours = wechatExcess + douyinExcess;
    }}

    const reclaimDays = (reclaimableHours / 24).toFixed(1);
    const moneyVal = ((reclaimableHours * wageVal) / 10000).toFixed(2);

    document.getElementById('reclaim-hours').innerText = Math.round(reclaimableHours).toLocaleString();
    document.getElementById('reclaim-days').innerText = `(相当于 ${{reclaimDays}} 天纯清醒白昼时间)`;
    document.getElementById('reclaim-money').innerText = moneyVal;

    // Equivalents
    document.getElementById('eq-books').innerText = Math.round(reclaimableHours / 6.0).toLocaleString();
    document.getElementById('eq-courses').innerText = Math.round(reclaimableHours / 60.0).toLocaleString();
    document.getElementById('eq-dates').innerText = Math.round(reclaimableHours / 3.0).toLocaleString();
    document.getElementById('eq-workouts').innerText = Math.round(reclaimableHours / 1.5).toLocaleString();
    document.getElementById('eq-trips').innerText = Math.round(reclaimableHours / 50.0).toLocaleString();
    document.getElementById('eq-money').innerText = moneyVal;

    renderOpportunityCharts(reclaimableHours, totalHours);
  }}

  function renderOpportunityCharts(reclaimableHours, totalHours) {{
    const domPie = document.getElementById('chart-opp-pie');
    const domBar = document.getElementById('chart-opp-bar');
    if (!domPie || !domBar) return;

    if (!reclaimableHours) {{
      reclaimableHours = window.DATA.opportunity_cost.excess_all_hours;
      totalHours = window.DATA.overview.total_hours;
    }}

    const baselineHours = Math.max(0, totalHours - reclaimableHours);

    // Pie
    if (charts['opp-pie']) charts['opp-pie'].dispose();
    const chartPie = echarts.init(domPie);
    charts['opp-pie'] = chartPie;

    chartPie.setOption({{
      tooltip: {{ trigger: 'item', formatter: '{{b}}: {{c}}h ({{d}}%)' }},
      legend: {{ bottom: 0, textStyle: {{ color: themeColors.text() }} }},
      series: [
        {{
          type: 'pie',
          radius: ['45%', '70%'],
          center: ['50%', '45%'],
          data: [
            {{ value: Math.round(baselineHours), name: '基础日常休闲额度', itemStyle: {{ color: '#10b981' }} }},
            {{ value: Math.round(reclaimableHours), name: '可重构机会成本池', itemStyle: {{ color: '#6366f1' }} }}
          ],
          label: {{ color: themeColors.text(), formatter: '{{b}}\\n{{d}}%' }}
        }}
      ]
    }});

    // Bar
    if (charts['opp-bar']) charts['opp-bar'].dispose();
    const chartBar = echarts.init(domBar);
    charts['opp-bar'] = chartBar;

    const books = Math.round(reclaimableHours / 6.0);
    const courses = Math.round(reclaimableHours / 60.0);
    const dates = Math.round(reclaimableHours / 3.0);
    const workouts = Math.round(reclaimableHours / 1.5);
    const trips = Math.round(reclaimableHours / 50.0);

    chartBar.setOption({{
      tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: ['精读书籍(本)', '浪漫约会(次)', '健身举铁(次)', '深度游(趟)', '体系课(套)'],
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), fontSize: 11 }}
      }},
      yAxis: {{
        type: 'value',
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      series: [
        {{
          type: 'bar',
          data: [
            {{ value: books, itemStyle: {{ color: '#3b82f6' }} }},
            {{ value: dates, itemStyle: {{ color: '#f43f5e' }} }},
            {{ value: workouts, itemStyle: {{ color: '#f59e0b' }} }},
            {{ value: trips, itemStyle: {{ color: '#06b6d4' }} }},
            {{ value: courses, itemStyle: {{ color: '#10b981' }} }}
          ],
          label: {{ show: true, position: 'top', color: themeColors.textMain() }},
          borderRadius: [4, 4, 0, 0]
        }}
      ]
    }});
  }}

  // ================= Tab 4: Video =================
  function renderVideoControl() {{
    const dom = document.getElementById('chart-video-control');
    if (!dom) return;
    if (charts['video-control']) charts['video-control'].dispose();
    const chart = echarts.init(dom);
    charts['video-control'] = chart;

    const months = window.DATA.monthly_summary.map(m => m.month);
    const videoHours = window.DATA.monthly_summary.map(m => m.video_hours);
    const videoRatios = window.DATA.monthly_summary.map(m => {{
      return m.total_hours > 0 ? Number((m.video_hours / m.total_hours * 100).toFixed(1)) : 0;
    }});

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        axisPointer: {{ type: 'cross' }}
      }},
      legend: {{
        data: ['短视频时长 (小时)', '占总屏幕比例 (%)'],
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 30 }}
      }},
      yAxis: [
        {{
          type: 'value',
          name: '时长 (h)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
          axisLabel: {{ color: themeColors.text() }}
        }},
        {{
          type: 'value',
          name: '占比 (%)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ show: false }},
          axisLabel: {{ color: themeColors.text(), formatter: '{{value}}%' }}
        }}
      ],
      series: [
        {{
          name: '短视频时长 (小时)',
          type: 'bar',
          data: videoHours,
          itemStyle: {{
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: '#f43f5e' }},
              {{ offset: 1, color: 'rgba(244, 63, 94, 0.25)' }}
            ]),
            borderRadius: [6, 6, 0, 0]
          }}
        }},
        {{
          name: '占总屏幕比例 (%)',
          type: 'line',
          yAxisIndex: 1,
          data: videoRatios,
          smooth: true,
          lineStyle: {{ color: '#f59e0b', width: 3 }},
          itemStyle: {{ color: '#f59e0b' }}
        }}
      ]
    }});
  }}

  function renderVideoBreakdown() {{
    const dom = document.getElementById('chart-video-breakdown');
    if (!dom) return;
    if (charts['video-breakdown']) charts['video-breakdown'].dispose();
    const chart = echarts.init(dom);
    charts['video-breakdown'] = chart;

    const apps = window.DATA.video_special.apps.slice(0, 4);
    const dataList = apps.map(a => ({{ name: a.name, value: a.total_hours }}));

    chart.setOption({{
      tooltip: {{
        trigger: 'item',
        formatter: '{{b}}: {{c}}h ({{d}}%)'
      }},
      legend: {{
        bottom: 0,
        textStyle: {{ color: themeColors.text(), fontSize: 11 }}
      }},
      series: [
        {{
          type: 'pie',
          radius: '65%',
          center: ['50%', '45%'],
          data: dataList,
          itemStyle: {{
            borderRadius: 6,
            borderColor: themeColors.cardBg(),
            borderWidth: 2
          }},
          label: {{ color: themeColors.text() }}
        }}
      ]
    }});
  }}

  function renderVideoPeaks() {{
    const dom = document.getElementById('chart-video-peaks');
    if (!dom) return;
    if (charts['video-peaks']) charts['video-peaks'].dispose();
    const chart = echarts.init(dom);
    charts['video-peaks'] = chart;

    const timeline = window.DATA.daily_timeline;
    const dates = timeline.map(d => d.date);
    const videoHours = timeline.map(d => d.video_hours);

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        formatter: function(params) {{
          const p = params[0];
          return p.name + '<br/>刷视频时长: <b>' + p.value + ' 小时</b>';
        }}
      }},
      grid: {{ left: '3%', right: '3%', bottom: '15%', top: '10%', containLabel: true }},
      dataZoom: [
        {{ type: 'inside', start: 0, end: 100 }},
        {{ type: 'slider', start: 0, end: 100, height: 20, bottom: 5, textStyle: {{ color: themeColors.text() }} }}
      ],
      xAxis: {{
        type: 'category',
        data: dates,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      yAxis: {{
        type: 'value',
        name: '单日时长 (小时)',
        nameTextStyle: {{ color: themeColors.text() }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      series: [
        {{
          name: '单日刷视频',
          type: 'bar',
          data: videoHours,
          itemStyle: {{
            color: function(params) {{
              if (params.value >= 5) return '#ef4444';
              if (params.value >= 3) return '#f59e0b';
              return '#6366f1';
            }}
          }},
          markLine: {{
            data: [
              {{ yAxis: 3, name: '预警线 3h', lineStyle: {{ color: '#f59e0b', type: 'dashed' }} }},
              {{ yAxis: 5, name: '重度线 5h', lineStyle: {{ color: '#ef4444', type: 'dashed' }} }}
            ]
          }}
        }}
      ]
    }});
  }}

  // ================= Tab 5: Weekday =================
  function renderWeekdayBars() {{
    const dom = document.getElementById('chart-weekday-bars');
    if (!dom) return;
    if (charts['weekday-bars']) charts['weekday-bars'].dispose();
    const chart = echarts.init(dom);
    charts['weekday-bars'] = chart;

    const list = window.DATA.weekday_summary;
    const names = list.map(i => i.name);
    const avgHours = list.map(i => i.avg_hours);
    const avgStarts = list.map(i => i.avg_starts);

    chart.setOption({{
      tooltip: {{ trigger: 'axis' }},
      legend: {{
        data: ['日均时长 (小时)', '日均启动 (次)'],
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: names,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      yAxis: [
        {{
          type: 'value',
          name: '时长 (h)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
          axisLabel: {{ color: themeColors.text() }}
        }},
        {{
          type: 'value',
          name: '启动 (次)',
          nameTextStyle: {{ color: themeColors.text() }},
          splitLine: {{ show: false }},
          axisLabel: {{ color: themeColors.text() }}
        }}
      ],
      series: [
        {{
          name: '日均时长 (小时)',
          type: 'bar',
          data: avgHours,
          itemStyle: {{ color: '#6366f1', borderRadius: [6, 6, 0, 0] }}
        }},
        {{
          name: '日均启动 (次)',
          type: 'line',
          yAxisIndex: 1,
          data: avgStarts,
          lineStyle: {{ color: '#10b981', width: 3 }},
          itemStyle: {{ color: '#10b981' }}
        }}
      ]
    }});
  }}

  function renderWeekdayRadar() {{
    const dom = document.getElementById('chart-weekday-radar');
    if (!dom) return;
    if (charts['weekday-radar']) charts['weekday-radar'].dispose();
    const chart = echarts.init(dom);
    charts['weekday-radar'] = chart;

    const monFri = window.DATA.weekday_summary.slice(0, 5);
    const satSun = window.DATA.weekday_summary.slice(5, 7);

    const categories = ['社交通讯', '短视频与流媒体', 'AI 生产力助手', '工作协同与学习', '系统与工具辅助', '电商与生活消费'];

    const getAvg = (list, cat) => {{
      const total = list.reduce((acc, cur) => acc + (cur.categories_avg_hours[cat] || 0), 0);
      return Number((total / list.length).toFixed(2));
    }};

    const weekdayVals = categories.map(c => getAvg(monFri, c));
    const weekendVals = categories.map(c => getAvg(satSun, c));

    chart.setOption({{
      tooltip: {{ trigger: 'item' }},
      legend: {{
        data: ['工作日 (周一至周五)', '周末 (周六至周日)'],
        textStyle: {{ color: themeColors.text() }},
        top: 0
      }},
      radar: {{
        indicator: categories.map(c => ({{ name: c, max: 5.5 }})),
        shape: 'polygon',
        splitArea: {{ show: false }},
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        name: {{ textStyle: {{ color: themeColors.text() }} }}
      }},
      series: [
        {{
          type: 'radar',
          data: [
            {{
              value: weekdayVals,
              name: '工作日 (周一至周五)',
              itemStyle: {{ color: '#6366f1' }},
              areaStyle: {{ color: 'rgba(99, 102, 241, 0.25)' }}
            }},
            {{
              value: weekendVals,
              name: '周末 (周六至周日)',
              itemStyle: {{ color: '#f43f5e' }},
              areaStyle: {{ color: 'rgba(244, 63, 94, 0.25)' }}
            }}
          ]
        }}
      ]
    }});
  }}

  function renderNightMonthly() {{
    const dom = document.getElementById('chart-night-monthly');
    if (!dom) return;
    if (charts['night-monthly']) charts['night-monthly'].dispose();
    const chart = echarts.init(dom);
    charts['night-monthly'] = chart;

    const months = window.DATA.months;
    const extremeCounts = months.map(m => {{
      const daysInMonth = window.DATA.daily_timeline.filter(d => d.date.startsWith(m));
      return daysInMonth.filter(d => d.hours >= 14).length;
    }});

    chart.setOption({{
      tooltip: {{
        trigger: 'axis',
        formatter: '{{b}}<br/>熬夜超长日 (≥14h): <b>{{c}} 天</b>'
      }},
      grid: {{ left: '4%', right: '4%', bottom: '8%', top: '15%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 30 }}
      }},
      yAxis: {{
        type: 'value',
        name: '警戒天数 (天)',
        nameTextStyle: {{ color: themeColors.text() }},
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text() }}
      }},
      series: [
        {{
          name: '≥14h 天数',
          type: 'bar',
          data: extremeCounts,
          itemStyle: {{
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: '#f59e0b' }},
              {{ offset: 1, color: 'rgba(245, 158, 11, 0.2)' }}
            ]),
            borderRadius: [4, 4, 0, 0]
          }}
        }}
      ]
    }});
  }}

  // ================= Tab 6: Calendar Heatmap =================
  function renderCalendarHeatmap() {{
    const dom = document.getElementById('chart-calendar-heatmap');
    if (!dom) return;
    if (charts['calendar-heatmap']) charts['calendar-heatmap'].dispose();
    const chart = echarts.init(dom);
    charts['calendar-heatmap'] = chart;

    const timeline = window.DATA.daily_timeline;
    const heatmapData = timeline.map(d => [d.date, d.hours, d.top_app, d.starts]);

    chart.setOption({{
      tooltip: {{
        formatter: function(params) {{
          const d = params.value[0];
          const h = params.value[1];
          const top = params.value[2] || '无';
          const starts = params.value[3] || 0;
          return `<b>${{d}}</b><br/>总时长: <b>${{h}} 小时</b><br/>解锁启动: ${{starts}} 次<br/>耗时最多: <b>${{top}}</b>`;
        }}
      }},
      visualMap: {{
        min: 0,
        max: 18,
        seriesIndex: [0, 1, 2],
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '2%',
        textStyle: {{ color: themeColors.text() }},
        inRange: {{
          color: ['#1e293b', '#1e3a8a', '#3b82f6', '#60a5fa', '#f59e0b', '#ef4444']
        }}
      }},
      calendar: [
        {{
          top: 30,
          range: '2024',
          cellSize: ['auto', 16],
          left: 55,
          right: 25,
          splitLine: {{ show: true, lineStyle: {{ color: themeColors.grid() }} }},
          itemStyle: {{ borderColor: themeColors.cardBg(), borderWidth: 1 }},
          yearLabel: {{ color: themeColors.textMain(), position: 'left' }},
          dayLabel: {{ color: themeColors.text(), firstDay: 1 }},
          monthLabel: {{ color: themeColors.text() }}
        }},
        {{
          top: 230,
          range: '2025',
          cellSize: ['auto', 16],
          left: 55,
          right: 25,
          splitLine: {{ show: true, lineStyle: {{ color: themeColors.grid() }} }},
          itemStyle: {{ borderColor: themeColors.cardBg(), borderWidth: 1 }},
          yearLabel: {{ color: themeColors.textMain(), position: 'left' }},
          dayLabel: {{ color: themeColors.text(), firstDay: 1 }},
          monthLabel: {{ color: themeColors.text() }}
        }},
        {{
          top: 430,
          range: '2026',
          cellSize: ['auto', 16],
          left: 55,
          right: 25,
          splitLine: {{ show: true, lineStyle: {{ color: themeColors.grid() }} }},
          itemStyle: {{ borderColor: themeColors.cardBg(), borderWidth: 1 }},
          yearLabel: {{ color: themeColors.textMain(), position: 'left' }},
          dayLabel: {{ color: themeColors.text(), firstDay: 1 }},
          monthLabel: {{ color: themeColors.text() }}
        }}
      ],
      series: [
        {{
          type: 'heatmap',
          coordinateSystem: 'calendar',
          calendarIndex: 0,
          data: heatmapData
        }},
        {{
          type: 'heatmap',
          coordinateSystem: 'calendar',
          calendarIndex: 1,
          data: heatmapData
        }},
        {{
          type: 'heatmap',
          coordinateSystem: 'calendar',
          calendarIndex: 2,
          data: heatmapData
        }}
      ]
    }});
  }}

  // ================= Tab 7: App Drilldown =================
  function renderAppDetail(pkg) {{
    selectedAppPkg = pkg;
    const app = window.DATA.top_apps.find(a => a.pkg === pkg);
    if (!app) return;

    document.querySelectorAll('#top-apps-body tr').forEach(tr => {{
      tr.classList.remove('selected');
      if (tr.getAttribute('data-pkg') === pkg) tr.classList.add('selected');
    }});

    document.getElementById('detail-app-name').innerText = '📱 ' + app.name + ' 画像剖析';
    document.getElementById('detail-app-pkg').innerText = app.pkg;
    document.getElementById('detail-app-cat').innerText = app.cat;
    document.getElementById('detail-total-hours').innerHTML = app.total_hours + '<span class="kpi-unit">h</span>';
    
    const startsFormatted = app.total_starts > 10000 ? (app.total_starts / 10000).toFixed(1) + '万次' : app.total_starts + '次';
    document.getElementById('detail-total-starts').innerHTML = startsFormatted;

    const domHours = document.getElementById('chart-app-monthly');
    if (charts['app-monthly']) charts['app-monthly'].dispose();
    const chartHours = echarts.init(domHours);
    charts['app-monthly'] = chartHours;

    const months = window.DATA.months;
    const hoursData = months.map(m => app.monthly_hours[m] || 0);

    chartHours.setOption({{
      tooltip: {{ trigger: 'axis', formatter: '{{b}}<br/>时长: <b>{{c}} 小时</b>' }},
      grid: {{ left: '4%', right: '4%', bottom: '15%', top: '10%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 45, fontSize: 10 }}
      }},
      yAxis: {{
        type: 'value',
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), fontSize: 10 }}
      }},
      series: [
        {{
          type: 'bar',
          data: hoursData,
          itemStyle: {{ color: '#6366f1', borderRadius: [4, 4, 0, 0] }}
        }}
      ]
    }});

    const domStarts = document.getElementById('chart-app-starts');
    if (charts['app-starts']) charts['app-starts'].dispose();
    const chartStarts = echarts.init(domStarts);
    charts['app-starts'] = chartStarts;

    const startsData = months.map(m => app.monthly_starts[m] || 0);

    chartStarts.setOption({{
      tooltip: {{ trigger: 'axis', formatter: '{{b}}<br/>启动: <b>{{c}} 次</b>' }},
      grid: {{ left: '4%', right: '4%', bottom: '15%', top: '10%', containLabel: true }},
      xAxis: {{
        type: 'category',
        data: months,
        axisLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), rotate: 45, fontSize: 10 }}
      }},
      yAxis: {{
        type: 'value',
        splitLine: {{ lineStyle: {{ color: themeColors.grid() }} }},
        axisLabel: {{ color: themeColors.text(), fontSize: 10 }}
      }},
      series: [
        {{
          type: 'line',
          data: startsData,
          smooth: true,
          itemStyle: {{ color: '#10b981' }},
          lineStyle: {{ color: '#10b981', width: 2.5 }}
        }}
      ]
    }});
  }}

  function filterAppsTable() {{
    const query = document.getElementById('app-search').value.toLowerCase().trim();
    document.querySelectorAll('#top-apps-body tr').forEach(tr => {{
      const text = tr.innerText.toLowerCase();
      tr.style.display = text.includes(query) ? '' : 'none';
    }});
  }}

  // Populate Tables
  function populateTables() {{
    const aiTbody = document.getElementById('ai-table-body');
    if (aiTbody) {{
      aiTbody.innerHTML = window.DATA.ai_special.apps.map(a => {{
        const avgMin = a.total_starts > 0 ? ((a.total_hours * 60) / a.total_starts).toFixed(1) : 0;
        let attrTag = `${{avgMin}} 分钟/次`;
        if (a.pkg.includes('bard')) attrTag = '快捷启动入口';
        else if (a.pkg.includes('googlequicksearchbox')) attrTag = 'Gemini 智能宿主';

        return `
          <tr>
            <td><b>${{a.name}}</b></td>
            <td style="color: var(--text-sub); font-family: monospace;">${{a.pkg}}</td>
            <td><b>${{a.total_hours}}</b> 小时</td>
            <td>${{a.total_starts.toLocaleString()}} 次</td>
            <td>${{a.active_days}} 天</td>
            <td>${{a.first_date}}</td>
            <td>${{a.last_date}}</td>
            <td><span class="badge">${{attrTag}}</span></td>
          </tr>
        `;
      }}).join('');
    }}

    const appsTbody = document.getElementById('top-apps-body');
    if (appsTbody) {{
      appsTbody.innerHTML = window.DATA.top_apps.slice(0, 30).map((a, idx) => {{
        let catClass = 'cat-other';
        if (a.cat === '社交通讯') catClass = 'cat-social';
        else if (a.cat === '短视频与流媒体') catClass = 'cat-video';
        else if (a.cat === 'AI 生产力助手') catClass = 'cat-ai';
        else if (a.cat === '工作协同与学习') catClass = 'cat-work';
        else if (a.cat === '手游与互动娱乐') catClass = 'cat-game';
        else if (a.cat === '系统与工具辅助') catClass = 'cat-system';

        const isSelected = a.pkg === selectedAppPkg ? 'selected' : '';

        return `
          <tr class="${{isSelected}}" data-pkg="${{a.pkg}}" onclick="renderAppDetail('${{a.pkg}}')">
            <td>
              <div class="app-icon-name">
                <div class="app-avatar">${{a.name.slice(0, 1)}}</div>
                <div>
                  <div style="font-weight: 600;">${{a.name}}</div>
                  <div style="font-size: 11px; color: var(--text-sub);">${{a.pkg}}</div>
                </div>
              </div>
            </td>
            <td><span class="cat-pill ${{catClass}}">${{a.cat}}</span></td>
            <td><b>${{a.total_hours}}</b> h</td>
            <td>${{a.total_starts.toLocaleString()}}</td>
            <td>${{a.active_days}} 天</td>
            <td>${{a.avg_daily_min}} 分钟</td>
          </tr>
        `;
      }}).join('');
    }}
  }}

  window.addEventListener('resize', () => {{
    Object.values(charts).forEach(c => c && c.resize && c.resize());
  }});

  document.addEventListener('DOMContentLoaded', () => {{
    populateTables();
    initTabCharts('overview');
  }});
</script>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated dashboard HTML at: {html_path}")
print(f"File size: {os.path.getsize(html_path)/1024:.1f} KB")
