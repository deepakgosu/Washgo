@echo off
echo Starting WashGo Customer App...
cd /d %~dp0
streamlit run apps/customer/app.py --server.port 8501 --server.headless false
