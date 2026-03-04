# -*- coding: utf-8 -*-
"""
代码统计工具 - 主程序

用于统计 Git/SVN 项目的代码改动行数，生成 Excel 和 HTML 报告
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

import config
import git_stats
import svn_stats
import excel_generator
import html_generator
import i18n


def print_header():
    """打印欢迎信息"""
    print("=" * 60)
    print(f"           {i18n.t('code_stats_tool')}")
    print("=" * 60)
    print(f"{i18n.t('time')} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def get_project_choices(projects):
    """
    交互式选择项目

    Args:
        projects: 项目配置列表

    Returns:
        选中的项目列表
    """
    # 按路径分组，合并同一项目的不同版本控制系统
    path_map = {}  # path -> [{name, type}, ...]
    for p in projects:
        path = p['path']
        if path not in path_map:
            path_map[path] = []
        path_map[path].append({'name': p['name'], 'type': p['type']})

    print("\n" + "=" * 60)
    print(i18n.t('select_projects'))
    print("=" * 60)

    # 构建选项列表
    options = []
    option_idx = 1

    for path, types in path_map.items():
        if len(types) == 1:
            # 单一版本控制
            p = types[0]
            options.append({
                'path': path,
                'name': p['name'],
                'type': p['type']
            })
            print(f"  [{option_idx}] {p['name']} ({p['type']})")
            print(f"      {i18n.t('path')} {path}")
            option_idx += 1
        else:
            # 同一项目多个版本控制
            for p in types:
                options.append({
                    'path': path,
                    'name': p['name'],
                    'type': p['type']
                })
                print(f"  [{option_idx}] {p['name']} ({p['type']})")
                print(f"      {i18n.t('path')} {path}")
                option_idx += 1

    print(f"\n  {i18n.t('select_all')}")
    print(f"  {i18n.t('quit')}")

    while True:
        choice = input(f"\n{i18n.t('enter_option')}").strip().lower()

        if choice == 'q':
            print(i18n.t('exited'))
            sys.exit(0)

        if choice == 'a':
            return options

        # 解析数字
        try:
            nums = [int(x.strip()) for x in choice.split(',')]
        except ValueError:
            print(i18n.t('invalid_input'))
            continue

        # 验证范围
        if any(n < 1 or n > len(options) for n in nums):
            print(i18n.t('invalid_range', max=len(options)))
            continue

        selected = [options[n - 1] for n in nums]
        return selected


def get_date_range_choice():
    """
    交互式选择日期范围

    Returns:
        日期范围字符串或 None
    """
    print("\n" + "=" * 60)
    print(i18n.t('select_date_range'))
    print("=" * 60)
    print(f"  {i18n.t('all_time')}")
    print(f"  {i18n.t('today')}")
    print(f"  {i18n.t('this_week')}")
    print(f"  {i18n.t('this_month')}")
    print(f"  {i18n.t('last_month')}")
    print(f"  {i18n.t('this_year')}")
    print(f"  {i18n.t('last_year')}")
    print(f"  {i18n.t('custom_range')}")

    today = datetime.now().date()

    while True:
        choice = input(f"\n{i18n.t('enter_option_num')}").strip()

        if choice == '1':
            return None  # 全部时间

        elif choice == '2':
            # 今天
            date_str = today.strftime("%Y-%m-%d")
            return f"{date_str}:{date_str}"

        elif choice == '3':
            # 本周 (周一到周日)
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            return f"{monday.strftime('%Y-%m-%d')}:{sunday.strftime('%Y-%m-%d')}"

        elif choice == '4':
            # 本月
            first_day = today.replace(day=1)
            # 下月第一天减一天
            if today.month == 12:
                last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            return f"{first_day.strftime('%Y-%m-%d')}:{last_day.strftime('%Y-%m-%d')}"

        elif choice == '5':
            # 上月
            first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            last_day = today.replace(day=1) - timedelta(days=1)
            return f"{first_day.strftime('%Y-%m-%d')}:{last_day.strftime('%Y-%m-%d')}"

        elif choice == '6':
            # 今年
            first_day = today.replace(month=1, day=1)
            return f"{first_day.strftime('%Y-%m-%d')}:{today.strftime('%Y-%m-%d')}"

        elif choice == '7':
            # 去年
            first_day = today.replace(year=today.year - 1, month=1, day=1)
            last_day = today.replace(year=today.year - 1, month=12, day=31)
            return f"{first_day.strftime('%Y-%m-%d')}:{last_day.strftime('%Y-%m-%d')}"

        elif choice == '8':
            # 自定义范围
            print(f"\n{i18n.t('enter_date_range_format')}")
            print(f"{i18n.t('eg')} 2026-01-01:2026-02-28")
            date_range = input(i18n.t('enter')).strip()

            # 简单验证
            try:
                parts = date_range.split(':')
                if len(parts) == 2:
                    start, end = parts
                    # 简单验证格式
                    datetime.strptime(start, "%Y-%m-%d")
                    datetime.strptime(end, "%Y-%m-%d")
                    return date_range
            except:
                pass

            print(i18n.t('invalid_date_format'))
            continue

        else:
            print(i18n.t('invalid_option'))


def collect_all_stats(projects, date_range=None):
    """
    收集所有项目的代码统计

    Args:
        projects: 项目配置列表
        date_range: 日期范围

    Returns:
        项目名称 -> 统计列表 的字典
    """
    all_stats = {}

    # 从配置文件读取自定义作者名，留空则使用 git/svn 的真实作者
    author_name = getattr(config, 'AUTHOR_NAME', None) or None
    if author_name:
        print("\n" + i18n.t('custom_author_configured', name=author_name))

    for project in projects:
        project_name = project['name']
        project_path = project['path']
        project_type = project['type']

        print(f"\n{'='*50}")
        print(i18n.t('analyzing_project', name=project_name, type=project_type))
        print(f"{i18n.t('path')} {project_path}")
        print(f"{'='*50}")

        if project_type == 'git':
            # 检查是否为 Git 仓库
            if not git_stats.is_git_repo(project_path):
                print(i18n.t('not_git_repo_warning', path=project_path))
                continue

            stats = git_stats.get_all_stats(project_path, date_range, author_name)
        elif project_type == 'svn':
            # 检查是否为 SVN 仓库
            if not svn_stats.is_svn_repo(project_path):
                print(i18n.t('not_svn_repo_warning', path=project_path))
                continue

            stats = svn_stats.get_all_stats(project_path, date_range, author_name)
        else:
            print(i18n.t('unknown_project_type', type=project_type))
            continue

        if stats:
            all_stats[project_name] = stats
            print(i18n.t('commits_retrieved', count=len(stats)))
        else:
            print(i18n.t('no_commits_retrieved'))

    return all_stats


def get_project_prefix(all_stats):
    """
    根据项目生成文件名前缀

    Args:
        all_stats: 项目统计数据

    Returns:
        前缀字符串
    """
    if not all_stats:
        return i18n.t('stats_report')

    names = list(all_stats.keys())
    if len(names) == 1:
        return names[0]
    elif len(names) <= 3:
        return "_".join(names)
    else:
        return f"{names[0]}{i18n.t('and_others', count=len(names))}"


def print_summary(all_stats):
    """打印统计汇总"""
    print("\n" + "=" * 60)
    print(i18n.t('stats_summary'))
    print("=" * 60)

    total_commits = 0
    total_insertions = 0
    total_deletions = 0

    for project_name, stats in all_stats.items():
        commits = len(stats)
        insertions = sum(s['insertions'] for s in stats)
        deletions = sum(s['deletions'] for s in stats)

        print(f"\n{project_name}:")
        print(f"  {i18n.t('commits')}: {commits}")
        print(f"  {i18n.t('insertions_lines')}: +{insertions}")
        print(f"  {i18n.t('deletions_lines')}: -{deletions}")
        print(f"  {i18n.t('net_lines')}: {insertions - deletions}")

        total_commits += commits
        total_insertions += insertions
        total_deletions += deletions

    print(f"\n{i18n.t('total')}:")
    print(f"  {i18n.t('projects_count')}: {len(all_stats)}")
    print(f"  {i18n.t('total_commits')}: {total_commits}")
    print(f"  {i18n.t('total_insertions')}: +{total_insertions}")
    print(f"  {i18n.t('total_deletions')}: -{total_deletions}")
    print(f"  {i18n.t('net_lines')}: {total_insertions - total_deletions}")


def interactive_mode():
    """交互式模式"""
    print_header()

    # 获取项目配置
    projects = config.PROJECTS

    if not projects:
        print(f"\n{i18n.t('empty_project_list_error')}")
        print(i18n.t('edit_config_hint'))
        return

    print("\n" + i18n.t('configured_projects_count', count=len(projects)))

    # 选择项目
    selected_projects = get_project_choices(projects)

    # 选择日期范围
    date_range = get_date_range_choice()

    if date_range:
        print("\n" + i18n.t('selected_date_range', range=date_range))

    # 创建输出目录
    output_dir = config.OUTPUT_DIR
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 收集统计
    all_stats = collect_all_stats(selected_projects, date_range)

    if not all_stats:
        print(f"\n{i18n.t('failed_to_get_stats')}")
        return

    # 打印汇总
    print_summary(all_stats)

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_prefix = get_project_prefix(all_stats)

    excel_path = os.path.join(output_dir, f"{project_prefix}_{timestamp}.xlsx")
    try:
        excel_generator.generate_excel(all_stats, excel_path)
        print("\n" + i18n.t('excel_generated', path=excel_path))
    except Exception as e:
        print("\n" + i18n.t('excel_generate_failed', error=e))

    html_path = os.path.join(output_dir, f"{project_prefix}_{timestamp}.html")
    try:
        html_generator.generate_html(all_stats, html_path)
        print(i18n.t('html_generated', path=html_path))
    except Exception as e:
        print(i18n.t('html_generate_failed', error=e))

    print("\n" + "=" * 60)
    print(i18n.t('stats_complete'))
    print("=" * 60)


def main():
    """
    主函数 - 命令行模式
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='代码统计工具 - 统计 Git/SVN 项目的代码改动行数',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python stats.py                    # 交互式模式
  python stats.py -i                 # 交互式模式 (同 -i)
  python stats.py -o output/         # 指定输出目录
  python stats.py -d 2024-01-01:2024-12-31  # 指定日期范围
  python stats.py --no-excel         # 不生成 Excel
  python stats.py --no-html           # 不生成 HTML
  python stats.py -p ISMS            # 只统计 ISMS 项目
  python stats.py -p "ISMS,项目A"    # 统计多个项目
        """
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='交互式模式'
    )

    parser.add_argument(
        '-o', '--output',
        default=config.OUTPUT_DIR,
        help=f'输出目录 (默认: {config.OUTPUT_DIR})'
    )

    parser.add_argument(
        '-d', '--date-range',
        default=config.DATE_RANGE,
        help='日期范围，格式: YYYY-MM-DD:YYYY-MM-DD'
    )

    parser.add_argument(
        '-p', '--projects',
        help='指定项目名称，多个用逗号分隔'
    )

    parser.add_argument(
        '--no-excel',
        action='store_true',
        help='不生成 Excel 报告'
    )

    parser.add_argument(
        '--no-html',
        action='store_true',
        help='不生成 HTML 报告'
    )

    args = parser.parse_args()

    # 如果没有参数或指定了交互模式，进入交互模式
    if len(sys.argv) == 1 or args.interactive:
        interactive_mode()
        return

    # 命令行模式
    print_header()

    # 获取项目配置
    projects = config.PROJECTS

    if not projects:
        print(f"\n{i18n.t('empty_project_list_error')}")
        print(i18n.t('edit_config_hint'))
        sys.exit(1)

    # 过滤指定的项目
    if args.projects:
        project_names = [p.strip() for p in args.projects.split(',')]
        projects = [p for p in projects if p['name'] in project_names]
        if not projects:
            print("\n" + i18n.t('no_matching_projects', projects=args.projects))
            sys.exit(1)

    print("\n" + i18n.t('configured_projects_count', count=len(projects)))
    for p in projects:
        print(f"  - {p['name']} ({p['type']}): {p['path']}")

    # 创建输出目录
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("\n" + i18n.t('output_dir_created', dir=output_dir))

    # 收集统计
    date_range = args.date_range if args.date_range else None
    all_stats = collect_all_stats(projects, date_range)

    if not all_stats:
        print(f"\n{i18n.t('failed_to_get_stats')}")
        sys.exit(1)

    # 打印汇总
    print_summary(all_stats)

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_prefix = get_project_prefix(all_stats)

    if not args.no_excel:
        excel_path = os.path.join(output_dir, f"{project_prefix}_{timestamp}.xlsx")
        try:
            excel_generator.generate_excel(all_stats, excel_path)
            print("\n" + i18n.t('excel_generated', path=excel_path))
        except Exception as e:
            print("\n" + i18n.t('excel_generate_failed', error=e))

    if not args.no_html:
        html_path = os.path.join(output_dir, f"{project_prefix}_{timestamp}.html")
        try:
            html_generator.generate_html(all_stats, html_path)
            print(i18n.t('html_generated', path=html_path))
        except Exception as e:
            print(i18n.t('html_generate_failed', error=e))

    print("\n" + "=" * 60)
    print(i18n.t('stats_complete'))
    print("=" * 60)


if __name__ == "__main__":
    main()
