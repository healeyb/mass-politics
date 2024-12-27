# mass-politics

create: /etc/systemd/system/mapol_api.service

[Unit]
Description=MA Politics API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/app
ExecStart=sudo /app/venv/bin/python /app/mass-politics/api.py
Restart=always

[Install]
WantedBy=multi-user.target

# install packages

pip3 install openai requests markdown2 markdown-it-py python-dotenv pymysql flask

python3 cli.py --suite support --method create-senate-stats

# reload

sudo systemctl daemon-reload

sudo systemctl stop macon_api.service

sudo systemctl start macon_api.service

journalctl -u macon_api.service -b -e