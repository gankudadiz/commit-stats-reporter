# -*- coding: utf-8 -*-
"""
SVN 代码统计模块
"""

import subprocess
import os
import re
from datetime import datetime


def get_commits(project_path, date_range=None):
    """
    获取 SVN 提交记录

    Args:
        project_path: 项目路径
        date_range: 日期范围，格式 "start:end"

    Returns:
        提交列表
    """
    if not os.path.exists(project_path):
        print(f"项目路径不存在: {project_path}")
        return []

    # 构建 svn log 命令
    cmd = ["svn", "log", "--verbose"]

    # 添加日期范围过滤
    if date_range:
        try:
            start, end = date_range.split(":")
            cmd.extend(["-r", f"{{{start}}}:{{{end}}}"])
        except ValueError:
            print(f"日期范围格式错误，应为 'YYYY-MM-DD:YYYY-MM-DD'，实际: {date_range}")
    else:
        # 默认获取最近1000条记录
        cmd.extend(["-l", "1000"])

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
            print(f"SVN 命令执行失败: {result.stderr}")
            return []

        commits = []
        current_commit = None

        for line in result.stdout.split('\n'):
            line = line.strip()

            # 新提交开始
            if line.startswith('---'):
                if current_commit:
                    commits.append(current_commit)
                current_commit = None
                continue

            # 解析提交信息行
            if current_commit is None and line.startswith('r'):
                # 格式: r1234 | user | 2024-01-01 12:00:00 | 1 line
                match = re.match(r'r(\d+)\s+\|\s+(\S+)\s+\|\s+(\d{4}-\d{2}-\d{2})', line)
                if match:
                    current_commit = {
                        'revision': match.group(1),
                        'author': match.group(2),  # 从 svn log 读取真实作者
                        'date': match.group(3),
                        'message': '',
                        'files': []
                    }
            elif current_commit and line:
                # 跳过空行和文件列表
                if not line.startswith('Changed paths:'):
                    if current_commit['message'] == '':
                        current_commit['message'] = line
                    else:
                        current_commit['message'] += ' ' + line

        # 添加最后一个提交
        if current_commit:
            commits.append(current_commit)

        return commits
    except Exception as e:
        print(f"获取 SVN 提交记录失败: {e}")
        return []


def get_commit_stats(project_path, revision):
    """
    获取某次提交的代码改动统计

    Args:
        project_path: 项目路径
        revision: SVN 版本号

    Returns:
        改动统计字典
    """
    try:
        # 使用 svn diff 获取改动统计
        result = subprocess.run(
            ["svn", "diff", "-c", revision, "--summaries"],
            cwd=project_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode != 0:
            # 尝试另一种方式获取
            result = subprocess.run(
                ["svn", "diff", "-c", revision],
                cwd=project_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

        output = result.stdout

        # 统计改动行数
        insertions = 0
        deletions = 0
        files_changed = 0

        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('+') and not line.startswith('+++'):
                insertions += 1
            elif line.startswith('-') and not line.startswith('---'):
                deletions += 1
            elif line.startswith('==='):
                files_changed += 1

        # 如果上面的方法不准确，尝试统计文件数
        if files_changed == 0:
            result = subprocess.run(
                ["svn", "diff", "-c", revision, "--summaries"],
                cwd=project_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                files_changed = len([l for l in result.stdout.split('\n') if l.strip()])

        return {
            'insertions': insertions,
            'deletions': deletions,
            'net': insertions - deletions,
            'files': files_changed
        }
    except Exception as e:
        print(f"获取提交 r{revision} 统计失败: {e}")
        return {'insertions': 0, 'deletions': 0, 'net': 0, 'files': 0}


def get_all_stats(project_path, date_range=None, author_name=None):
    """
    获取项目的所有代码统计

    Args:
        project_path: 项目路径
        date_range: 日期范围
        author_name: 自定义作者显示名（字符串）。
                     若不为空，报告中所有记录的作者均使用该名称；
                     若为空，则保留 svn log 中的真实作者名。

    Returns:
        统计结果列表
    """
    commits = get_commits(project_path, date_range)

    results = []
    for commit in commits:
        stats = get_commit_stats(project_path, commit['revision'])
        results.append({
            'revision': commit['revision'],
            'author': author_name if author_name else commit['author'],  # 自定义名优先，否则用真实作者
            'date': commit['date'],
            'message': commit['message'],
            'insertions': stats['insertions'],
            'deletions': stats['deletions'],
            'net': stats['net'],
            'files': stats['files']
        })

    return results


def is_svn_repo(path):
    """
    检查路径是否为 SVN 仓库

    Args:
        path: 路径

    Returns:
        bool
    """
    if not os.path.exists(path):
        return False

    try:
        result = subprocess.run(
            ["svn", "info"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False
