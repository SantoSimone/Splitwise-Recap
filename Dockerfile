FROM python:3.13

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
# CMD ["python" "-m", "streamlit", "run", "streamlit_dashboard/main.py", "--server.port", "8080"]
CMD python -m streamlit run streamlit_dashboard/main.py --server.port 8080