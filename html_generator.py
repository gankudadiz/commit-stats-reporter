# -*- coding: utf-8 -*-
"""
HTML 报告生成模块
"""

import os
from datetime import datetime
from jinja2 import Template

import i18n


# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t('code_stats_report') }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f4f6f8;
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid #e1e4e8;
        }

        .header {
            background-color: #1e293b;
            color: white;
            padding: 30px;
            text-align: left;
            border-bottom: 3px solid #3b82f6;
        }

        .header h1 {
            font-size: 28px;
            font-weight: 500;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }

        .header .subtitle {
            font-size: 14px;
            opacity: 0.8;
            font-weight: 300;
        }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #fff;
            border-bottom: 1px solid #e1e4e8;
        }

        .card {
            background: #ffffff;
            padding: 20px;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            text-align: left;
            box-shadow: none;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .card .label {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card .value {
            font-size: 28px;
            font-weight: 600;
            color: #0f172a;
        }

        .card .value.positive {
            color: #10b981;
        }

        .card .value.negative {
            color: #ef4444;
        }

        .section {
            padding: 20px;
        }

        .section h2 {
            font-size: 20px;
            color: #1e293b;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e1e4e8;
            font-weight: 500;
        }

        .project-card {
            background: white;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            margin-bottom: 20px;
            box-shadow: none;
            overflow: hidden;
        }

        .project-header {
            background-color: #f8fafc;
            color: #1e293b;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e1e4e8;
        }

        .project-header h3 {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
        }

        .project-stats {
            display: flex;
            gap: 15px;
        }

        .project-stats span {
            background: #e2e8f0;
            color: #334155;
            padding: 4px 10px;
            border-radius: 2px;
            font-size: 13px;
            font-weight: 500;
        }

        .project-content {
            padding: 0;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th, td {
            padding: 12px 20px;
            text-align: left;
            border-bottom: 1px solid #e1e4e8;
        }

        th {
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }

        td {
            color: #334155;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover {
            background: #f1f5f9;
        }

        .commit-hash {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            background: #f1f5f9;
            color: #475569;
            padding: 3px 6px;
            border-radius: 2px;
            font-size: 12px;
            border: 1px solid #e2e8f0;
        }

        .message {
            max-width: 400px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .positive {
            color: #10b981;
        }

        .negative {
            color: #ef4444;
        }

        .chart-container {
            padding: 20px;
            background: #fff;
            border-top: 1px solid #e1e4e8;
        }

        .chart {
            background: white;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 0;
        }

        .chart h3 {
            margin-bottom: 20px;
            color: #1e293b;
            font-size: 16px;
            font-weight: 600;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 8px;
        }

        .bar-chart {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .bar-item {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .bar-label {
            width: 180px;
            font-size: 14px;
            color: #334155;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: right;
        }

        .bar-wrapper {
            flex: 1;
            height: 12px;
            background: #f1f5f9;
            border-radius: 2px;
            overflow: hidden;
        }

        .bar {
            height: 100%;
            border-radius: 2px;
            transition: width 0.3s ease;
        }

        .bar.insertions {
            background-color: #3b82f6;
        }

        .bar.deletions {
            background-color: #ef4444;
        }

        .bar-value {
            width: 70px;
            text-align: left;
            font-size: 14px;
            font-weight: 500;
        }

        .footer {
            background: #f8fafc;
            color: #64748b;
            padding: 15px 20px;
            text-align: center;
            font-size: 12px;
            border-top: 1px solid #e1e4e8;
        }

        @media (max-width: 768px) {
            .summary-cards {
                grid-template-columns: 1fr;
            }

            .project-stats {
                flex-direction: column;
                gap: 5px;
                align-items: flex-start;
            }

            table {
                font-size: 12px;
            }

            th, td {
                padding: 8px;
            }
            
            .message {
                max-width: 150px;
            }
            
            .bar-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }
            
            .bar-label {
                width: auto;
                text-align: left;
            }
            
            .bar-wrapper {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ t('code_stats_report') }}</h1>
            <div class="subtitle">{{ t('generated_at') }} {{ generate_time }}</div>
        </div>

        <div class="summary-cards">
            <div class="card">
                <div class="label">{{ t('projects_count') }}</div>
                <div class="value">{{ total_projects }}</div>
            </div>
            <div class="card">
                <div class="label">{{ t('total_commits') }}</div>
                <div class="value">{{ total_commits }}</div>
            </div>
            <div class="card">
                <div class="label">{{ t('total_insertions') }}</div>
                <div class="value positive">{{ total_insertions }}</div>
            </div>
            <div class="card">
                <div class="label">{{ t('total_deletions') }}</div>
                <div class="value negative">{{ total_deletions }}</div>
            </div>
            <div class="card">
                <div class="label">{{ t('net_lines') }}</div>
                <div class="value {% if total_net > 0 %}positive{% elif total_net < 0 %}negative{% endif %}">{{ total_net }}</div>
            </div>
        </div>

        <div class="section">
            <h2>{{ t('project_summary') }}</h2>
            {% for project in projects %}
            <div class="project-card">
                <div class="project-header">
                    <h3>{{ project.name }}</h3>
                    <div class="project-stats">
                        <span>{{ t('commits_label') }} {{ project.commits }}</span>
                        <span>+{{ project.insertions }}</span>
                        <span>-{{ project.deletions }}</span>
                    </div>
                </div>
                <div class="project-content">
                    <table>
                        <thead>
                            <tr>
                                <th>{{ t('commit_id') }}</th>
                                <th>{{ t('author') }}</th>
                                <th>{{ t('date') }}</th>
                                <th>{{ t('message') }}</th>
                                <th>{{ t('insertions') }}</th>
                                <th>{{ t('deletions') }}</th>
                                <th>{{ t('net') }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for commit in project.commits_list[:10] %}
                            <tr>
                                <td><span class="commit-hash">{{ commit.id }}</span></td>
                                <td>{{ commit.author }}</td>
                                <td>{{ commit.date }}</td>
                                <td class="message" title="{{ commit.message }}">{{ commit.message }}</td>
                                <td class="positive">+{{ commit.insertions }}</td>
                                <td class="negative">-{{ commit.deletions }}</td>
                                <td class="{% if commit.net > 0 %}positive{% elif commit.net < 0 %}negative{% endif %}">{{ commit.net }}</td>
                            </tr>
                            {% endfor %}
                            {% if project.commits_list|length > 10 %}
                            <tr>
                                <td colspan="7" style="text-align: center; color: #666;">
                                    {{ t('more_records', count=project.commits_list|length - 10) }}
                                </td>
                            </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="chart-container">
            <div class="chart">
                <h3>{{ t('chart_title') }}</h3>
                <div class="bar-chart">
                    {% for project in projects %}
                    <div class="bar-item">
                        <div class="bar-label">{{ project.name }}</div>
                        <div class="bar-wrapper">
                            <div class="bar insertions" style="width: {{ project.insertions / max_insertions * 100 }}%"></div>
                        </div>
                        <div class="bar-value positive">+{{ project.insertions }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <div class="footer">
            <p>{{ t('footer_text') }}</p>
        </div>
    </div>
</body>
</html>
"""


def generate_html(all_stats, output_path):
    """
    生成 HTML 报告

    Args:
        all_stats: 所有项目的统计数据
        output_path: 输出文件路径

    Returns:
        输出文件路径
    """
    # 计算汇总数据
    total_projects = len(all_stats)
    total_commits = sum(len(stats) for stats in all_stats.values())
    total_insertions = sum(sum(s['insertions'] for s in stats) for stats in all_stats.values())
    total_deletions = sum(sum(s['deletions'] for s in stats) for stats in all_stats.values())
    total_net = total_insertions - total_deletions

    # 准备项目数据
    projects = []
    max_insertions = 0

    for project_name, stats in all_stats.items():
        project_insertions = sum(s['insertions'] for s in stats)
        project_deletions = sum(s['deletions'] for s in stats)
        project_commits = len(stats)

        if project_insertions > max_insertions:
            max_insertions = project_insertions

        # 准备提交列表
        commits_list = []
        for s in stats:
            commits_list.append({
                'id': s.get('hash', s.get('revision', ''))[:8],
                'author': s['author'],
                'date': s['date'],
                'message': s['message'],
                'insertions': s['insertions'],
                'deletions': s['deletions'],
                'net': s['net']
            })

        # 按日期排序
        commits_list.sort(key=lambda x: x['date'], reverse=True)

        projects.append({
            'name': project_name,
            'commits': project_commits,
            'insertions': project_insertions,
            'deletions': project_deletions,
            'net': project_insertions - project_deletions,
            'commits_list': commits_list
        })

    # 渲染模板
    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        t=i18n.t,
        lang=i18n.CURRENT_LANG,
        generate_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_projects=total_projects,
        total_commits=total_commits,
        total_insertions=total_insertions,
        total_deletions=total_deletions,
        total_net=total_net,
        projects=projects,
        max_insertions=max_insertions
    )

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path
