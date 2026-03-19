@echo off
echo Starting WashGo Partner App...
cd /d %~dp0
streamlit run apps/partner/app.py --server.port 8502 --server.headless false
