sudo apt-get update;
sudo apt-get -y upgrade;
sudo apt-get -y install htop wkhtmltopdf python-pip rabbitmq-server git;
cd modules/HTML.py-0.04/;
python setup.py install;
cd ..; cd..;
pip install -r requirements.txt;