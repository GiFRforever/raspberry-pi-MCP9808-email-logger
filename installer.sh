pip install -r requirements.txt
cp templogger.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/templogger.service
systemctl daemon-reload
systemctl enable templogger.service
systemctl start templogger.service
alias sendmail="python /home/pi/templogger/sendmail.py"