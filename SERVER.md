sudo nano /etc/nginx/sites-available/my-assistant
sudo nginx -t
sudo systemctl reload nginx
sudo ln -sf /etc/nginx/sites-available/my-assistant /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-enabled/default