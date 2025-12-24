@echo off
echo ========================================
echo Omok-Lab Git Commit and Push Script
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Or use GitHub Desktop: https://desktop.github.com/
    echo.
    pause
    exit /b 1
)

echo Checking repository status...
git status
echo.

echo Staging all changes...
git add .
echo.

echo Committing changes...
git commit -m "feat: Implement Omok-Lab v2.4.0 - AI-powered Gomoku game" -m "- Add complete MVC architecture with core game engine" -m "- Implement Renju rule enforcement (3-3, 4-4, overline detection)" -m "- Add Minimax AI with Alpha-Beta pruning" -m "- Create PyQt6 UI with beautiful dark theme" -m "- Add player selection dialog and real-time AI analysis" -m "- Include win probability chart and move history" -m "- Add comprehensive PRD documentation"
echo.

echo Pushing to remote repository...
git push
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Changes pushed to GitHub
    echo ========================================
) else (
    echo ========================================
    echo ERROR: Push failed
    echo Please check your credentials and try again
    echo ========================================
)

echo.
pause
