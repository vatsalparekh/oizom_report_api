sudo apt-get update;
sudo apt-get -y upgrade;
sudo apt-get -y install htop wkhtmltopdf python-pip rabbitmq-server git xvfb;
cd modules/HTML.py-0.04/;
python setup.py install;
cd ..; cd ..;
pip install -r requirements.txt;
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz;
tar xf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz;
cp wkhtmltox/bin/wkhtmltopdf /usr/bin/;
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2;
tar xf phantomjs-2.1.1-linux-x86_64.tar.bz2;
cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin;
git clone http://github.com/vatsalparekh/highcharts-png-renderer;
phantomjs highcharts-png-renderer/run.js &