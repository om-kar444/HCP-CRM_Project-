@echo off
echo Initializing git repository...
git init

echo Adding all files...
git add .

echo Creating commit...
git commit -m "HCP CRM: AI-powered interaction logging with LangGraph and Groq LLM - Dual interface (React Vite + FastAPI) with 5 LangGraph tools for pharmaceutical sales"

echo Adding GitHub remote...
git remote add origin https://github.com/om-kar444/HCP-CRM_Project.git

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo Done! Project pushed to GitHub successfully!
pause