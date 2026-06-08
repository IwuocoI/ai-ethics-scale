@echo off
setlocal enabledelayedexpansion

echo === 1/3 安装依赖 ===
pip install -q -r requirements.txt
if %errorlevel% neq 0 (pause & exit /b 1)

echo.
echo === 2/3 配置 API Key ===
echo [1] 输入 Key
echo [2] 跳过（已有key或不需要）
choice /c 12 /n /m "请选择: "
if errorlevel 2 goto skip_key
set /p KEY="粘贴 DeepSeek API Key: "
if "!KEY!"=="" (
    echo Key 为空，跳过。
) else (
    echo api_key = "!KEY!" > ".streamlit\secrets.toml"
    echo 已保存。
)
:skip_key

echo.
echo === 3/3 启动 ===
echo 浏览器打开 http://localhost:8501
streamlit run app.py
pause
