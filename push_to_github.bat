@echo off
REM Helper script to push to GitHub
REM Edit this file first to add your GitHub username/repo

echo Pushing to GitHub...
echo.

REM TODO: Edit these variables with your GitHub info
set GITHUB_USER=YOUR_USERNAME
set REPO_NAME=hosts-file-guardian

if "%GITHUB_USER%"=="YOUR_USERNAME" (
    echo ERROR: Please edit this file and set your GitHub username!
    echo.
    echo Open push_to_github.bat in a text editor and change:
    echo   set GITHUB_USER=YOUR_USERNAME
    echo to your actual GitHub username.
    pause
    exit /b 1
)

cd /d "%~dp0"

echo Checking git status...
git status

echo.
echo Do you want to commit and push? (Y/N)
set /p confirm=
if /i not "%confirm%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Adding all changes...
git add .

echo.
echo Enter commit message (or press Enter for default):
set /p commit_msg=
if "%commit_msg%"=="" set commit_msg=Update files

echo.
echo Committing...
git commit -m "%commit_msg%"

echo.
echo Setting remote (if not already set)...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git 2>nul

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorLevel% equ 0 (
    echo.
    echo SUCCESS! Your code has been pushed to GitHub.
    echo Visit: https://github.com/%GITHUB_USER%/%REPO_NAME%
) else (
    echo.
    echo ERROR: Push failed. Check your GitHub credentials and repository name.
)

echo.
pause

