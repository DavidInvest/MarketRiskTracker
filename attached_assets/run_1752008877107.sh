#!/bin/bash
python main.py &
streamlit run dashboard/dashboard.py --server.port 8501 --server.enableCORS false
