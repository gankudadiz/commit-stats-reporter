# 代码统计工具 (Code Statistics Tool)

[简体中文](#简体中文) | [English](#english) | [日本語](#日本語)

---

<h2 id="简体中文">简体中文</h2>

用于统计 Git/SVN 项目的代码改动行数，生成 Excel 和 HTML 报告，方便记录日常工作内容。

### 功能特性
- **多语言支持**：原生支持中文、英文、日文三种语言（界面与生成报告均可配置）。
- **多版本控制**：支持 Git 和 SVN 两种版本控制系统。
- **灵活配置**：交互式选择项目和日期范围，同一项目支持 Git/SVN 分别统计。
- **详尽统计**：统计每个项目的提交次数、代码行数（新增/删除/净增）。
- **专业报告**：生成详细的 Excel 表格报告及可视化的 HTML 报告（可直接截图发给经理）。

### 项目结构
```text
代码统计工具/
├── stats.py              # 主程序
├── config.py             # 配置文件（项目路径列表）
├── i18n.py               # 国际化模块
├── git_stats.py          # Git统计模块
├── svn_stats.py          # SVN统计模块
├── excel_generator.py    # Excel生成模块
├── html_generator.py     # HTML报告生成模块
├── requirements.txt      # Python依赖
└── output/               # 输出目录
```

### 安装
1. 确保已安装 Python 3.7+
2. 安装依赖:
```bash
pip install -r requirements.txt
```

### 配置
编辑 `config.py` 文件（若无则依据 `config.example.py` 复制一份），添加需要统计的项目并配置期望的语言:

```python
# 语言配置: 'zh' (中文), 'en' (英文), 'ja' (日文)
LANGUAGE = "zh"

PROJECTS = [
    # Git 项目
    {"name": "ISMS", "path": "D:\\www\\ISMS", "type": "git"},
    # SVN 项目
    {"name": "项目A", "path": "D:\\www\\project_a", "type": "svn"},
]

# 自定义作者名配置 (统一报告中作者显示的名称，留空则为真实名字)
AUTHOR_NAME = "zhangsan"
```

### 快速启动（推荐）
直接双击项目根目录下的 `start.bat` 即可一键启动，脚本会自动检查并安装 Python 及依赖。

### 使用方法 (命令行模式)
```bash
python stats.py                           # 交互式模式
python stats.py -p "ISMS"                 # 统计指定项目
python stats.py -p "ISMS,项目A"           # 指定多个项目
python stats.py -d 2024-01-01:2024-12-31  # 指定日期范围
python stats.py -o output/                # 指定输出目录
python stats.py --no-html                 # 不生成 HTML
python stats.py --no-excel                # 不生成 Excel
```

### 注意事项
- 确保项目路径正确且版本控制系统可用
- Git 仓库需要 `.git` 目录存在
- SVN 仓库需要 `.svn` 目录存在
- 首次使用建议先用一个项目测试

---

<h2 id="english">English</h2>

A tool used to count the lines of code changes in Git/SVN projects, generating Excel and HTML reports, making it convenient to record daily work content.

### Features
- **Multi-language Support**: Native support for Chinese, English, and Japanese (configurable in UI & reports).
- **VCS Support**: Supports both Git and SVN version control systems.
- **Flexible Config**: Interactive selection of projects and date ranges. Supports Git/SVN statistics for the same project.
- **Detailed Stats**: Counts the number of commits and lines of code for each project (Insertions/Deletions/Net).
- **Professional Reports**: Generates detailed Excel tables and visual HTML reports (ready for screenshotting to managers).

### Project Structure
```text
Code Statistics Tool/
├── stats.py              # Main Program
├── config.py             # Config File (Array of paths)
├── i18n.py               # I18n Module
├── git_stats.py          # Git Stats Module
├── svn_stats.py          # SVN Stats Module
├── excel_generator.py    # Excel Generator
├── html_generator.py     # HTML Report Generator
├── requirements.txt      # Python Dependencies
└── output/               # Output Directory
```

### Installation
1. Ensure Python 3.7+ is installed.
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration
Edit the `config.py` file (copy from `config.example.py` if not exists), add the projects to be analyzed, and configure your preferred language:

```python
# Language settings: 'zh' (Chinese), 'en' (English), 'ja' (Japanese)
LANGUAGE = "en"

PROJECTS = [
    # Git Project
    {"name": "ISMS", "path": "D:\\www\\ISMS", "type": "git"},
    # SVN Project
    {"name": "ProjectA", "path": "D:\\www\\project_a", "type": "svn"},
]

# Custom Author Config (Overwrites the author's display name, leave blank for real names)
AUTHOR_NAME = "John Doe"
```

### Quick Start (Recommended)
Simply double-click `start.bat` in the root directory. The script will automatically check for and install Python and dependencies.

### Usage (Command Line)
```bash
python stats.py                           # Interactive mode
python stats.py -p "ISMS"                 # Analyze specific project
python stats.py -p "ISMS,ProjectA"        # Analyze multiple projects
python stats.py -d 2024-01-01:2024-12-31  # Specific date range
python stats.py -o output/                # Specific output directory
python stats.py --no-html                 # Skip HTML generation
python stats.py --no-excel                # Skip Excel generation
```

### Notes
- Ensure project paths are correct and VCS commands are available in your environment.
- Git repositories must contain a `.git` directory.
- SVN repositories must contain a `.svn` directory.
- Test with one project to verify functionality during your first run.

---

<h2 id="日本語">日本語</h2>

Git/SVN プロジェクトのコード変更行数をカウントし、Excel や HTML のレポートを生成して、日々の作業内容を記録するためのツールです。

### 特徴
- **多言語サポート**: 中国語、英語、日本語をネイティブサポート（UIおよびレポートで構成可能）。
- **複数バージョン管理**: Git と SVN の両方のバージョン管理システムをサポート。
- **柔軟な構成**: プロジェクトと日付範囲を対話式で選択可能。同じプロジェクトで Git/SVN の個別統計をサポート。
- **詳細な統計**: 各プロジェクトのコミット数とコード行数（追加/削除/純増）をカウントします。
- **プロフェッショナルなレポート**: 詳細な Excel テーブルと視覚的な HTML レポートを生成します（そのままマネージャーにスクリーンショットとして送信可能）。

### プロジェクト構造
```text
コード統計ツール/
├── stats.py              # メインプログラム
├── config.py             # 設定ファイル (プロジェクトパスリスト)
├── i18n.py               # 国際化モジュール
├── git_stats.py          # Git 統計モジュール
├── svn_stats.py          # SVN 統計モジュール
├── excel_generator.py    # Excel 生成モジュール
├── html_generator.py     # HTML レポート生成モジュール
├── requirements.txt      # Python 依存関係
└── output/               # 出力ディレクトリ
```

### インストール
1. Python 3.7+ がインストールされていることを確認します。
2. 依存関係をインストールします:
```bash
pip install -r requirements.txt
```

### 設定
`config.py` ファイルを編集し（存在しない場合は `config.example.py` をコピー）、統計するプロジェクトを追加して、希望する言語を設定します:

```python
# 言語設定: 'zh' (中国語), 'en' (英語), 'ja' (日本語)
LANGUAGE = "ja"

PROJECTS = [
    # Git プロジェクト
    {"name": "ISMS", "path": "D:\\www\\ISMS", "type": "git"},
    # SVN プロジェクト
    {"name": "ProjectA", "path": "D:\\www\\project_a", "type": "svn"},
]

# カスタム作成者名の構成 (レポートで一律の表示名、空白の場合は元の名前を使用)
AUTHOR_NAME = "山田太郎"
```

### クイックスタート（推奨）
ルートディレクトリにある `start.bat` をダブルクリックするだけです。スクリプトが Python と依存関係を自動的にチェックしてインストールします。

### 使用方法 (コマンドライン)
```bash
python stats.py                           # インタラクティブモード
python stats.py -p "ISMS"                 # 特定のプロジェクトの統計
python stats.py -p "ISMS,ProjectA"        # 複数プロジェクトの指定
python stats.py -d 2024-01-01:2024-12-31  # 特定の期間
python stats.py -o output/                # 出力ディレクトリの指定
python stats.py --no-html                 # HTML レポートなし
python stats.py --no-excel                # Excel レポートなし
```

### 注意事項
- プロジェクトのパスが正しく、バージョン管理システムが利用可能であることを確認してください。
- Git リポジトリには `.git` ディレクトリが存在する必要があります。
- SVN リポジトリには `.svn` ディレクトリが存在する必要があります。
- 初回使用時は、一つのプロジェクトでテストすることをお勧めします。

---

## 许可证 / License / ライセンス
MIT License
