sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install htop wkhtmltopdf python-pip rabbitmq-server git xvfb supervisor
cd modules/HTML.py-0.04/
sudo python setup.py install
cd ..; cd ..;
sudo pip install -r requirements.txt
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar xf phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin
git clone http://github.com/vatsalparekh/highcharts-png-renderer
sudo cp highcharts-api-supervisor.conf supervisord.conf /etc/supervisor/conf.d/
