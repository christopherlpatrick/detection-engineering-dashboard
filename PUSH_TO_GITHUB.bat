@echo off
echo ========================================
echo Push Detection Engineering Dashboard to GitHub
echo ========================================
echo.

echo Step 1: Create a repository on GitHub first!
echo Go to: https://github.com/new
echo.
echo Step 2: Set your repository name below
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: detection-engineering-dashboard): "

if "%REPO_NAME%"=="" set REPO_NAME=detection-engineering-dashboard

echo.
echo Adding remote: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Done! Check your repository at:
echo https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo ========================================
pause
