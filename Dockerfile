# Loop — HuggingFace Spaces (Docker SDK) runtime.
# HF's API does not accept the "streamlit" SDK for this account, so the app runs
# as a Docker Space. Docker runs the exact same Streamlit app; nothing else
# changes. Port 8501 is declared as `app_port` in README.md's front-matter.
FROM python:3.11-slim

WORKDIR /app

# Writable, headless Streamlit config (HF containers may run non-root).
ENV HOME=/app \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    XDG_CACHE_HOME=/tmp/.cache \
    XDG_CONFIG_HOME=/tmp/.config \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]
