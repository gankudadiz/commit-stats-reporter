# -*- coding: utf-8 -*-
"""
Git 代码统计模块
"""

import subprocess
import os
from datetime import datetime


def get_commits(project_path, date_range=None):
    """
    获取 Git 提交记录

    Args:
        project_path: 项目路径
        date_range: 日期范围，格式 "start:end"

    Returns:
        提交列表
    """
    if not os.path.exists(project_path):
        print(f"项目路径不存在: {project_path}")
        return []

    # 构建 git log 命令
    cmd = [
        "git", "log",
        "--pretty=format:%H|%an|%ad|%s",
        "--date=short"
    ]

    # 添加日期范围过滤
    if date_range:
        try:
            start, end = date_range.split(":")
            cmd.extend([f"--after={start}", f"--before={end}"])
        except ValueError:
            print(f"日期范围格式错误，应为 'YYYY-MM-DD:YYYY-MM-DD'，实际: {date_range}")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            print(f"Git 命令执行失败: {result.stderr}")
            return []

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= 4:
                commits.append({
                    'hash': parts[0],
                    'author': parts[1],  # 从 git log 读取真实作者
                    'date': parts[2],
                    'message': '|'.join(parts[3:])  # 消息中可能包含 |
                })

        return commits
    except Exception as e:
        print(f"获取 Git 提交记录失败: {e}")
        return []


def get_commit_stats(project_path, commit_hash):
    """
    获取某次提交的代码改动统计

    Args:
        project_path: 项目路径
        commit_hash: 提交哈希值

    Returns:
        改动统计字典
    """
    try:
        # 使用 git show --stat 获取改动统计
        result = subprocess.run(
            ["git", "show", "--stat", "--format=", commit_hash],
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            return {'insertions': 0, 'deletions': 0, 'files': 0}

        # 解析输出
        output = result.stdout
        lines = output.strip().split('\n')

        total_insertions = 0
        total_deletions = 0
        files_changed = 0

        # 统计每个文件的改动
        for line in lines:
            line = line.strip()
            if not line or line.endswith('|') or 'files changed' in line:
                continue

            # 匹配类似 "src/main.py | 5 +++---" 的格式
            if '|' in line:
                files_changed += 1
                # 尝试提取数字
                import re
                # 匹配 + 和 - 的数量
                plus_matches = re.findall(r'\+(\d+)', line)
                minus_matches = re.findall(r'-(\d+)', line)

                for match in plus_matches:
                    total_insertions += int(match)
                for match in minus_matches:
                    total_deletions += int(match)

        # 如果没有匹配到详细统计，尝试从最后的汇总行获取
        if total_insertions == 0 and total_deletions == 0:
            for line in lines:
                if 'insertion' in line or 'deletion' in line:
                    import re
                    ins_match = re.search(r'(\d+) insertion', line)
                    del_match = re.search(r'(\d+) deletion', line)
                    if ins_match:
                        total_insertions = int(ins_match.group(1))
                    if del_match:
                        total_deletions = int(del_match.group(1))

        return {
            'insertions': total_insertions,
            'deletions': total_deletions,
            'net': total_insertions - total_deletions,
            'files': files_changed
        }
    except Exception as e:
        print(f"获取提交 {commit_hash} 统计失败: {e}")
        return {'insertions': 0, 'deletions': 0, 'net': 0, 'files': 0}


def get_all_stats(project_path, date_range=None, author_name=None):
    """
    获取项目的所有代码统计

    Args:
        project_path: 项目路径
        date_range: 日期范围
        author_name: 自定义作者显示名（字符串）。
                     若不为空，报告中所有记录的作者均使用该名称；
                     若为空，则保留 git log 中的真实作者名。

    Returns:
        统计结果列表
    """
    commits = get_commits(project_path, date_range)

    results = []
    for commit in commits:
        stats = get_commit_stats(project_path, commit['hash'])
        results.append({
            'hash': commit['hash'][:8],  # 简短哈希
            'author': author_name if author_name else commit['author'],  # 自定义名优先，否则用真实作者
            'date': commit['date'],
            'message': commit['message'],
            'insertions': stats['insertions'],
            'deletions': stats['deletions'],
            'net': stats['net'],
            'files': stats['files']
        })

    return results


def is_git_repo(path):
    """
    检查路径是否为 Git 仓库

    Args:
        path: 路径

    Returns:
        bool
    """
    if not os.path.exists(path):
        return False

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False
