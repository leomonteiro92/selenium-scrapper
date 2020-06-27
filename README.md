### Download Firefox
```
wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/77.0.1/linux-x86_64/en-US/firefox-77.0.1.tar.bz2

tar xvjf firefox-77.0.1.tar.bz2

mv firefox /usr/local

ln -s /usr/local/firefox/firefox /usr/bin/firefox
```

### Download Geckodriver
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz

tar -xf geckodriver-v0.26.0-linux64.tar.gz

mv geckodriver /usr/bin
```

### Create a virtualenv
```
virtualenv venv
source venv/bin/activate
```

### Install requirements
```
pip install -r requirements.txt
```

### Run
```
scrapy runspider index.py -t csv -o output.csv
```