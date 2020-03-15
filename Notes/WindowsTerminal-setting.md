```json
{
    "$schema": "https://aka.ms/terminal-profiles-schema",
    "globals": {
        "alwaysShowTabs": true,
        "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
        "initialCols": 80,
        "initialRows": 25,
        "keybindings": [
            {
                "command": "closeTab",
                "keys": [
                    "ctrl+w"
                ]
            }
        ],
        "requestedTheme": "system",
        "showTabsInTitlebar": true,
        "showTerminalTitleInTitlebar": true
    },
    "profiles": [
        {
            "acrylicOpacity": 0.5,
            "closeOnExit": true,
            "colorScheme": "Campbell",
            "commandline": "powershell.exe",
            "cursorColor": "#FFFFFF",
            "cursorShape": "bar",
            "fontFace": "Hack",
            "fontSize": 13,
            "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
            "historySize": 9001,
            "icon": "ms-appx:///ProfileIcons/{61c54bbd-c2c6-5271-96e7-009a87ff44bf}.png",
            "name": "Windows PowerShell",
            "padding": "0, 0, 0, 0",
            "snapOnInput": true,
            "startingDirectory": "%Workspaces%",
            "useAcrylic": true
        },
        {
            "guid": "{b453ae62-4e3d-5e58-b989-0a998ec441b8}",
            "hidden": false,
            "name": "Azure Cloud Shell",
            "source": "Windows.Terminal.Azure"
        }
    ],
    "schemes": [
        {
            "background": "#0C0C0C",
            "black": "#0C0C0C",
            "blue": "#0037DA",
            "brightBlack": "#767676",
            "brightBlue": "#3B78FF",
            "brightCyan": "#61D6D6",
            "brightGreen": "#16C60C",
            "brightPurple": "#B4009E",
            "brightRed": "#E74856",
            "brightWhite": "#F2F2F2",
            "brightYellow": "#F9F1A5",
            "cyan": "#3A96DD",
            "foreground": "#CCCCCC",
            "green": "#13A10E",
            "name": "Campbell",
            "purple": "#881798",
            "red": "#C50F1F",
            "white": "#CCCCCC",
            "yellow": "#C19C00"
        }
    ]
}
```
PowerShell 中激活anaconda的虚拟python环境
```shell
conda install -n root -c pscondaenvs pscondaenvs
```
以管理员身份启动PowerShell，并执行
```shell
Set-ExecutionPolicy RemoteSigned
```
注意激活时不要加conda，直接activate env就ok