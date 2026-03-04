@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 代码统计工具

:: 默认语言 / Default language / デフォルト言語
set APP_LANG=zh

:: 尝试从配置文件读取语言 / Try to read language from config
if exist "%~dp0config.py" (
    for /f "tokens=2 delims==" %%i in ('findstr /r "^[ ]*LANGUAGE[ ]*=" "%~dp0config.py"') do (
        set "val=%%i"
        set "val=!val: =!"
        set "val=!val:"=!"
        set "val=!val:'=!"
        if /i "!val!"=="en" set APP_LANG=en
        if /i "!val!"=="ja" set APP_LANG=ja
    )
)

:: 设置多语言文案 / Set multi-language strings
if "!APP_LANG!"=="en" (
    set "MSG_TITLE=Code Statistics Tool - Environment Check & Startup"
    set "MSG_STEP1=[1/4] Checking Python environment..."
    set "MSG_NO_PY=[!] Python not detected, attempting to install via Microsoft Store..."
    set "MSG_INSTALLING_PY=Installing Python 3.12 via winget..."
    set "MSG_INSTALL_PY_FAIL1=[ERROR] Auto-install failed. Please manually install Python 3.7+:"
    set "MSG_INSTALL_PY_FAIL2=https://www.python.org/downloads/"
    set "MSG_INSTALL_PY_SUCCESS=[OK] Python installation completed. Please restart this script to apply environment variables."
    set "MSG_PY_VER_ERROR1=[ERROR] Current Python version is {PY_VER}, requires 3.7 or above."
    set "MSG_PY_VER_ERROR2=Please visit https://www.python.org/downloads/ to download a newer version."
    set "MSG_PY_INSTALLED=[OK] Python {PY_VER} is installed"
    
    set "MSG_STEP2=[2/4] Checking pip..."
    set "MSG_NO_PIP=[!] pip is not available, attempting auto-repair..."
    set "MSG_PIP_FAIL=[ERROR] pip initialization failed, please reinstall Python."
    set "MSG_PIP_OK=[OK] pip is available"
    
    set "MSG_STEP3=[3/4] Checking and installing project dependencies (requirements.txt)..."
    set "MSG_NO_REQ=[!] requirements.txt not found, skipping dependency check."
    set "MSG_DEPENDENCY_FAIL1=[ERROR] Dependency installation failed. Check network connection and try again."
    set "MSG_DEPENDENCY_FAIL2=Alternatively, run manually: pip install -r requirements.txt"
    set "MSG_DEPENDENCY_OK=[OK] Dependency check completed"
    
    set "MSG_STEP4=[4/4] Checking configuration file..."
    set "MSG_NO_CONFIG=[!] config.py not found."
    set "MSG_CREATING_CONFIG=Auto-creating from config.example.py..."
    set "MSG_CONFIG_CREATED1=[OK] config.py created. Please edit before running!"
    set "MSG_CONFIG_CREATED2=File path: %~dp0config.py"
    set "MSG_CONFIG_HINT1=Main configurations to modify:"
    set "MSG_CONFIG_HINT2=  PROJECTS   - Fill in your project paths"
    set "MSG_CONFIG_HINT3=  AUTHOR_NAME - Custom author name (optional)"
    set "MSG_NO_EXAMPLE=[ERROR] config.example.py not found."
    set "MSG_CONFIG_EXISTS=[OK] config.py exists"
    
    set "MSG_STARTING=Environment check passed, starting program..."
    set "MSG_EXITED=Program exited. Press any key to close window..."
) else if "!APP_LANG!"=="ja" (
    set "MSG_TITLE=コード統計ツール - 環境チェックと起動"
    set "MSG_STEP1=[1/4] Python 環境の確認..."
    set "MSG_NO_PY=[!] Python が検出されません。Microsoft Store からのインストールを試みます..."
    set "MSG_INSTALLING_PY=winget を介して Python 3.12 をインストールしています..."
    set "MSG_INSTALL_PY_FAIL1=[エラー] 自動インストールに失敗しました。Python 3.7+ を手動でインストールしてください："
    set "MSG_INSTALL_PY_FAIL2=https://www.python.org/downloads/"
    set "MSG_INSTALL_PY_SUCCESS=[OK] Python のインストールが完了しました。環境変数を適用するためにこのスクリプトを再起動してください。"
    set "MSG_PY_VER_ERROR1=[エラー] 現在の Python バージョンは {PY_VER} ですが、3.7 以上が必要です。"
    set "MSG_PY_VER_ERROR2=新しいバージョンをダウンロードするには https://www.python.org/downloads/ にアクセスしてください。"
    set "MSG_PY_INSTALLED=[OK] Python {PY_VER} がインストールされています"
    
    set "MSG_STEP2=[2/4] pip の確認..."
    set "MSG_NO_PIP=[!] pip が利用できません。自動修復を試みます..."
    set "MSG_PIP_FAIL=[エラー] pip の初期化に失敗しました。Python を再インストールしてください。"
    set "MSG_PIP_OK=[OK] pip は利用可能です"
    
    set "MSG_STEP3=[3/4] プロジェクトの依存関係 (requirements.txt) の確認..."
    set "MSG_NO_REQ=[!] requirements.txt が見つかりません。依存関係の確認をスキップします。"
    set "MSG_DEPENDENCY_FAIL1=[エラー] 依存関係のインストールに失敗しました。ネットワーク接続を確認して再試行してください。"
    set "MSG_DEPENDENCY_FAIL2=または手動で実行してください： pip install -r requirements.txt"
    set "MSG_DEPENDENCY_OK=[OK] 依存関係の確認が完了しました"
    
    set "MSG_STEP4=[4/4] 設定ファイルの確認..."
    set "MSG_NO_CONFIG=[!] config.py が見つかりません。"
    set "MSG_CREATING_CONFIG=config.example.py から自動作成中..."
    set "MSG_CONFIG_CREATED1=[OK] config.py が作成されました。実行前に編集してください！"
    set "MSG_CONFIG_CREATED2=ファイルパス: %~dp0config.py"
    set "MSG_CONFIG_HINT1=変更が必要な主な設定："
    set "MSG_CONFIG_HINT2=  PROJECTS    - プロジェクトのパスを入力します"
    set "MSG_CONFIG_HINT3=  AUTHOR_NAME - カスタム作成者名（任意）"
    set "MSG_NO_EXAMPLE=[エラー] config.example.py が見つかりません。"
    set "MSG_CONFIG_EXISTS=[OK] config.py が存在します"
    
    set "MSG_STARTING=環境チェックに合格しました。プログラムを起動しています..."
    set "MSG_EXITED=プログラムが終了しました。任意のキーを押してウィンドウを閉じてください..."
) else (
    set "MSG_TITLE=代码统计工具 - 环境检查与启动"
    set "MSG_STEP1=[1/4] 检查 Python 环境..."
    set "MSG_NO_PY=[!] 未检测到 Python，尝试从 Microsoft Store 安装..."
    set "MSG_INSTALLING_PY=正在通过 winget 安装 Python 3.12 ..."
    set "MSG_INSTALL_PY_FAIL1=[错误] 自动安装失败，请手动安装 Python 3.7+："
    set "MSG_INSTALL_PY_FAIL2=https://www.python.org/downloads/"
    set "MSG_INSTALL_PY_SUCCESS=[√] Python 安装完成，请重新运行本脚本以使环境变量生效。"
    set "MSG_PY_VER_ERROR1=[错误] 当前 Python 版本为 {PY_VER}，需要 3.7 或以上版本。"
    set "MSG_PY_VER_ERROR2=请前往 https://www.python.org/downloads/ 下载新版本。"
    set "MSG_PY_INSTALLED=[√] Python {PY_VER} 已安装"
    
    set "MSG_STEP2=[2/4] 检查 pip ..."
    set "MSG_NO_PIP=[!] pip 不可用，尝试自动修复..."
    set "MSG_PIP_FAIL=[错误] pip 初始化失败，请重新安装 Python。"
    set "MSG_PIP_OK=[√] pip 可用"
    
    set "MSG_STEP3=[3/4] 检查并安装项目依赖 (requirements.txt) ..."
    set "MSG_NO_REQ=[!] 未找到 requirements.txt，跳过依赖检查。"
    set "MSG_DEPENDENCY_FAIL1=[错误] 依赖安装失败，请检查网络连接后重试。"
    set "MSG_DEPENDENCY_FAIL2=也可以手动执行：pip install -r requirements.txt"
    set "MSG_DEPENDENCY_OK=[√] 依赖检查完毕"
    
    set "MSG_STEP4=[4/4] 检查配置文件 ..."
    set "MSG_NO_CONFIG=[!] 未找到 config.py。"
    set "MSG_CREATING_CONFIG=正在从 config.example.py 自动创建..."
    set "MSG_CONFIG_CREATED1=[√] config.py 已创建，请先编辑配置文件再运行！"
    set "MSG_CONFIG_CREATED2=文件路径: %~dp0config.py"
    set "MSG_CONFIG_HINT1=主要需要修改的配置："
    set "MSG_CONFIG_HINT2=  PROJECTS   - 填写你的项目路径"
    set "MSG_CONFIG_HINT3=  AUTHOR_NAME - 自定义作者名（可留空）"
    set "MSG_NO_EXAMPLE=[错误] 未找到 config.example.py，请确认文件完整。"
    set "MSG_CONFIG_EXISTS=[√] config.py 存在"
    
    set "MSG_STARTING=环境检查通过，正在启动程序..."
    set "MSG_EXITED=程序已退出。按任意键关闭窗口..."
)

echo ============================================================
echo            !MSG_TITLE!
echo ============================================================
echo.

:: -------------------------------------------------------------
:: 第一步：检查 Python 是否安装
:: -------------------------------------------------------------
echo !MSG_STEP1!

python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo     !MSG_NO_PY!
    echo.
    echo     !MSG_INSTALLING_PY!
    winget install --id Python.Python.3.12 -e --source winget --silent
    if !errorlevel! neq 0 (
        echo.
        echo     !MSG_INSTALL_PY_FAIL1!
        echo           !MSG_INSTALL_PY_FAIL2!
        echo.
        pause
        exit /b 1
    )
    echo.
    echo     !MSG_INSTALL_PY_SUCCESS!
    pause
    exit /b 0
)

:: 获取 Python 版本并校验（要求 3.7+）
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

if !PY_MAJOR! lss 3 (
    set "MSG_PY_VER_ERROR1_FINAL=!MSG_PY_VER_ERROR1:{PY_VER}=%PY_VER%!"
    echo     !MSG_PY_VER_ERROR1_FINAL!
    echo           !MSG_PY_VER_ERROR2!
    pause
    exit /b 1
)
if !PY_MAJOR! equ 3 if !PY_MINOR! lss 7 (
    set "MSG_PY_VER_ERROR1_FINAL=!MSG_PY_VER_ERROR1:{PY_VER}=%PY_VER%!"
    echo     !MSG_PY_VER_ERROR1_FINAL!
    echo           !MSG_PY_VER_ERROR2!
    pause
    exit /b 1
)

set "MSG_PY_INSTALLED_FINAL=!MSG_PY_INSTALLED:{PY_VER}=%PY_VER%!"
echo     !MSG_PY_INSTALLED_FINAL!

:: ─────────────────────────────────────────────────────────────
:: 第二步：检查 pip 是否可用
:: ─────────────────────────────────────────────────────────────
echo.
echo !MSG_STEP2!

pip --version >nul 2>&1
if !errorlevel! neq 0 (
    echo     !MSG_NO_PIP!
    python -m ensurepip --upgrade >nul 2>&1
    pip --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo     !MSG_PIP_FAIL!
        pause
        exit /b 1
    )
)

echo     !MSG_PIP_OK!

:: ─────────────────────────────────────────────────────────────
:: 第三步：安装 / 更新依赖
:: ─────────────────────────────────────────────────────────────
echo.
echo !MSG_STEP3!

:: 检查 requirements.txt 是否存在
if not exist "%~dp0requirements.txt" (
    echo     !MSG_NO_REQ!
    goto :check_config
)

:: 尝试安静地检查依赖是否全部满足（pip check 会报错若有未满足的）
pip install -r "%~dp0requirements.txt" --quiet --disable-pip-version-check
if !errorlevel! neq 0 (
    echo.
    echo     !MSG_DEPENDENCY_FAIL1!
    echo           !MSG_DEPENDENCY_FAIL2!
    pause
    exit /b 1
)

echo     !MSG_DEPENDENCY_OK!

:: ─────────────────────────────────────────────────────────────
:: 第四步：检查 config.py 是否存在
:: ─────────────────────────────────────────────────────────────
:check_config
echo.
echo !MSG_STEP4!

if not exist "%~dp0config.py" (
    echo     !MSG_NO_CONFIG!
    echo         !MSG_CREATING_CONFIG!
    if exist "%~dp0config.example.py" (
        copy "%~dp0config.example.py" "%~dp0config.py" >nul
        echo.
        echo     !MSG_CONFIG_CREATED1!
        echo         !MSG_CONFIG_CREATED2!
        echo.
        echo     !MSG_CONFIG_HINT1!
        echo       !MSG_CONFIG_HINT2!
        echo       !MSG_CONFIG_HINT3!
        echo.
        start "" notepad "%~dp0config.py"
        pause
        exit /b 0
    ) else (
        echo     !MSG_NO_EXAMPLE!
        pause
        exit /b 1
    )
)

echo     !MSG_CONFIG_EXISTS!

:: ─────────────────────────────────────────────────────────────
:: 启动主程序
:: ─────────────────────────────────────────────────────────────
echo.
echo ============================================================
echo  !MSG_STARTING!
echo ============================================================
echo.

cd /d "%~dp0"
python stats.py

:: 程序退出后暂停，方便查看输出
echo.
echo ============================================================
echo  !MSG_EXITED!
echo ============================================================
pause >nul
