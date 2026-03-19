@echo off
echo Starting WashGo Admin App...
cd /d %~dp0
streamlit run apps/admin/app.py --server.port 8503 --server.headless false
