sudo usermod -a -G www-data admin

sudo chgrp -R www-data *
sudo chown -R admin *.py *.md *.txt src media config backup cache .gitignore
sudo chown -R www-data data
sudo chgrp -R admin backup

find src -type f | sudo xargs chmod 640
find src -type d | sudo xargs chmod 750
find media -type f | sudo xargs chmod 640
find media -type d | sudo xargs chmod 750

find cache -type f | sudo xargs chmod 640
find cache -type d | sudo xargs chmod 750
find backup -type f | sudo xargs chmod 600
find backup -type d | sudo xargs chmod 700
find data -type f | sudo xargs chmod 660
find data -type d | sudo xargs chmod 770

find config -type f | sudo xargs chmod 640
find config -type d | sudo xargs chmod 750
sudo chown www-data config/cron.conf config/bot.conf
sudo chown admin:root config/uwsgi.ini
sudo chown www-data:admin cache/*.log

sudo chown admin:admin *.sh .git
sudo chmod 700 *.sh
sudo chmod 640 robots.txt .gitignore util_restore.sh.example
sudo chown admin:admin *.py* *.md requirements.txt
sudo chmod 600 *.py* *.md requirements.txt
find .git -type f | sudo xargs chmod 640
find .git -type d | sudo xargs chmod 750
sudo chown admin:www-data .

sudo chown admin:www-data ../yuicompressor.jar
sudo chmod 640 ../yuicompressor.jar
