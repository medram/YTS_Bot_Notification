# YTS_Bot_Notification
it's a simple bot that Notify me when a new movie has been posted :-)

And this is how notifications look like in linux :D

![](https://raw.githubusercontent.com/medram/YTS_Bot_Notification/master/wiki/imgs/YTSThread.PNG)

## Installation
```bash
git clone --single-branch --branch master https://github.com/medram/YTS_Bot_Notification.git
cd YTS_Bot_Notification
sudo apt install build-essential libpython3-dev libdbus-1-dev libglib2.0-dev
python3 -m venv venv
venv/bin/pip install -r requirements_linux.txt
```

## Start
```bash
./run.sh
```

## Cron Job
Note: Change <code>your/directory/path/here</code> with your directory path that contains the files.
```bash
cat <(crontab -l) <(echo "*/30 * * * * cd your/directory/path/here && bash ./run.sh") | crontab -
```

## License
Under MIT License :D
