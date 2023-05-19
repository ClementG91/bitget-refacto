## Installation

1. Download this repository or clone it
```
git clone https://github.com/ClementG91/bitget-refacto
```

2. Use virtual environment
```
python -m pip install --user virtualenv
python -m venv my_env
my_env\Scripts\activate
```


3. Install requirements
```
pip install -r requirments.txt
```
4. Create a secret.json file like this
```
{
    "bitget_exemple": {
        "apiKey":"your apikey",
        "secret":"your secret",
        "password":"your password"
    },
    "discord_exemple": {
        "token":"your bot token",
        "channel":"your channel(id)"
    }
}
```

5. Launch the bot every hour on a server using a crontab

```
crontab -e
0 * * * * python3 /path/to/main.py >> /path/to/logs/main.log 2>&1
```
