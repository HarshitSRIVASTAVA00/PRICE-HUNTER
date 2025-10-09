# gunicorn_config.py

# Bind to 0.0.0.0:8000 for external access
bind = "0.0.0.0:8000"

# Number of worker processes (adjust per CPU cores)
workers = 3

# Worker class (sync is fine for I/O-bound scraping)
worker_class = "sync"

# Timeout (in seconds) before a worker is killed
timeout = 120

# Enable access log and error log
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
