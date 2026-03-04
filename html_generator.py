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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }

        .header .subtitle {
            font-size: 16px;
            opacity: 0.9;
        }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .card .label {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }

        .card .value {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }

        .card .value.positive {
            color: #28a745;
        }

        .card .value.negative {
            color: #dc3545;
        }

        .section {
            padding: 30px;
        }

        .section h2 {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .project-card {
            background: white;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .project-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .project-header h3 {
            font-size: 20px;
        }

        .project-stats {
            display: flex;
            gap: 20px;
        }

        .project-stats span {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
        }

        .project-content {
            padding: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }

        td {
            font-size: 14px;
            color: #555;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .commit-hash {
            font-family: "Courier New", monospace;
            background: #f0f0f0;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
        }

        .message {
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .positive {
            color: #28a745;
        }

        .negative {
            color: #dc3545;
        }

        .chart-container {
            padding: 30px;
            background: #f8f9fa;
        }

        .chart {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .chart h3 {
            margin-bottom: 15px;
            color: #333;
        }

        .bar-chart {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .bar-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .bar-label {
            width: 150px;
            font-size: 14px;
            color: #555;
        }

        .bar-wrapper {
            flex: 1;
            height: 24px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
        }

        .bar {
            height: 100%;
            border-radius: 12px;
            transition: width 0.3s ease;
        }

        .bar.insertions {
            background: linear-gradient(90deg, #28a745, #34ce57);
        }

        .bar.deletions {
            background: linear-gradient(90deg, #dc3545, #e4606d);
        }

        .bar-value {
            width: 60px;
            text-align: right;
            font-size: 14px;
            font-weight: 600;
        }

        .footer {
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .summary-cards {
                grid-template-columns: 1fr;
            }

            .project-stats {
                flex-direction: column;
                gap: 5px;
            }

            table {
                font-size: 12px;
            }

            th, td {
                padding: 8px 4px;
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
