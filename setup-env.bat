@echo off
echo TorTrack Environment Setup
echo ==========================
echo.

REM Check if .env already exists
if exist ".env" (
    echo WARNING: .env file already exists in root directory.
    set /p overwrite="Do you want to overwrite it? (y/N): "
    if /i "%overwrite%"=="y" (
        copy env.example .env >nul
        echo Created new .env from template
    ) else (
        echo Keeping existing .env file.
    )
) else (
    copy env.example .env >nul
    echo Created .env from template
)

REM Check backend .env
if exist "backend\.env" (
    echo WARNING: .env file already exists in backend directory.
    set /p overwrite_backend="Do you want to overwrite it? (y/N): "
    if /i "%overwrite_backend%"=="y" (
        copy backend\env.example backend\.env >nul
        echo Created new backend\.env from template
    ) else (
        echo Keeping existing backend\.env file.
    )
) else (
    copy backend\env.example backend\.env >nul
    echo Created backend\.env from template
)

echo.
echo Next steps:
echo 1. Edit .env and add your API keys
echo 2. Edit backend\.env for local development
echo 3. See API_KEYS.md for instructions on getting API keys
echo.
echo Then run: docker-compose up -d
pause 