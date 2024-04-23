# Python script to automate game setup (Playnite + Home assistant)

## Install (Windows Only)
```sh
pip install -r requirements.txt
```

## Start with windows
1. Create a shortcut to playnite.pyw
2. Open the startup folder
    * Win + R
    * shell:startup
3. Copy the shortcut to the startup folder
4. Restart the computer

## UP
```sh
pythonw.exe playnite.pyw
```
## DOWN
```sh
taskkill /IM pythonw.exe /F
```

## Sunshine
```sh
cmd /C python C:\Daniel\Code\desktop_gaming_automation\console.py --resolution %SUNSHINE_CLIENT_WIDTH% %SUNSHINE_CLIENT_HEIGHT% --command sunshine_do
cmd /C python C:\Daniel\Code\desktop_gaming_automation\console.py --command sunshine_undo
```
## TODO
* deal with exceptions
* log errors
* make automations generic
