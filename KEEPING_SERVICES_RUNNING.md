# Keeping Services Running

## Problem

Frontend/backend services stop running after the terminal disconnects.

## Solutions

### Solution 1: Use Background Startup Scripts (Recommended)

#### Start Services

```bash
# Start backend (background mode)
cd backend
bash start-daemon.sh

# Start frontend (background mode)
cd frontend
bash start-daemon.sh

# Or start all services at once
cd /path/to/iseek
bash start-all.sh
```

#### Stop Services

```bash
# Stop backend
cd backend
bash stop.sh

# Stop frontend
cd frontend
bash stop.sh

# Or stop all services at once
cd /path/to/iseek
bash stop-all.sh
```

#### View Logs

```bash
# Backend logs
tail -f backend/logs/backend.log

# Frontend logs
tail -f frontend/logs/frontend.log
```

### Solution 2: Use screen (Suitable for temporary sessions)

```bash
# Install screen (if not installed)
# yum install screen  # CentOS/RHEL
# apt-get install screen  # Ubuntu/Debian

# Create screen session
screen -S iseek-frontend
cd frontend
npm start
# Press Ctrl+A then D to detach (service continues running)

# Reattach
screen -r iseek-frontend

# List all sessions
screen -ls
```

### Solution 3: Use tmux (Recommended for servers)

```bash
# Install tmux (if not installed)
# yum install tmux  # CentOS/RHEL
# apt-get install tmux  # Ubuntu/Debian

# Create tmux session
tmux new -s iseek-frontend
cd frontend
npm start
# Press Ctrl+B then D to detach (service continues running)

# Reattach
tmux attach -t iseek-frontend

# List all sessions
tmux ls
```

### Solution 4: Use PM2 (Node.js Process Manager, Recommended for production)

```bash
# Install PM2
npm install -g pm2

# Start frontend
cd frontend
pm2 start npm --name "iseek-frontend" -- start

# Start backend (need to create startup script)
cd backend
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name "iseek-backend"

# Check status
pm2 status

# View logs
pm2 logs

# Stop services
pm2 stop iseek-frontend
pm2 stop iseek-backend

# Restart services
pm2 restart iseek-frontend

# Set auto-start on boot
pm2 startup
pm2 save
```

### Solution 5: Use systemd (Linux system service, Recommended for production)

Create systemd service files:

```bash
# Create frontend service
sudo nano /etc/systemd/system/iseek-frontend.service
```

Content:
```ini
[Unit]
Description=iSeek Frontend Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/iseek/frontend
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create backend service
sudo nano /etc/systemd/system/iseek-backend.service
```

Content:
```ini
[Unit]
Description=iSeek Backend Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/iseek/backend
ExecStart=/path/to/iseek/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start services:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start services
sudo systemctl start iseek-frontend
sudo systemctl start iseek-backend

# Enable auto-start on boot
sudo systemctl enable iseek-frontend
sudo systemctl enable iseek-backend

# Check status
sudo systemctl status iseek-frontend
sudo systemctl status iseek-backend

# View logs
sudo journalctl -u iseek-frontend -f
sudo journalctl -u iseek-backend -f
```

## Recommended Solutions

- **Development Environment**: Use `start-daemon.sh` scripts (Solution 1)
- **Testing Environment**: Use screen or tmux (Solution 2/3)
- **Production Environment**: Use PM2 or systemd (Solution 4/5)

## Notes

1. When using background scripts, logs are saved in the `logs/` directory
2. PID files are saved in `logs/*.pid` for stopping services
3. Ensure the logs directory has write permissions
4. Regularly clean log files to avoid excessive disk usage

