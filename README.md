# SierraTwo
Project Sierra is a simple encrypted reverse shell over Github, Slack, and Discord.

`SierraTwo` refers to the Slack shell, whereas `SierraOne` refers to the `Github` shell and `SierraThree` refers to the Discord shell.

## Usage
`SierraTwo` only supports Python 3.x.

### Windows
```
$ pip install -r requirements.txt
$ python SierraTwo.py
```

### Linux
```
$ sudo apt install python3-pip
$ pip3 install -r requirements.txt
$ python3 SierraTwo.py
```


## Configuration
To use `SierraTwo`, create a Slack workspace where you are the admin. Afterwards go to [Slack Apps][Slack Apps] and create a bot. From there, under the `Features` tab, go to `OAuth & Permissions` and add the following scopes:

### Bot Token Scopes
| Permission             | Description                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------|
| **channels:history**   | View messages and other content in public channels that BravoOmegaTango has been added to       |
| **channels:join**      | Join public channels in the workspace                                                           |
| **channels:manage**    | Manage public channels that BravoOmegaTango has been added to and create new ones               |
| **channels:read**      | View basic information about public channels in the workspace                                   |
| **chat:write**         | Send messages as @bravoomegatango                                                               |
| **commands**           | Add actions and/or slash commands that people can use                                           |
| **files:write**        | Upload, edit, and delete files as BravoOmegaTango                                               |
| **groups:history**     | View messages and other content in private channels that BravoOmegaTango has been added to      |
| **groups:read**        | View basic information about private channels that BravoOmegaTango has been added to            |
| **groups:write**       | Manage private channels that BravoOmegaTango has been added to and create new ones              |
| **im:history**         | View messages and other content in direct messages that BravoOmegaTango has been added to       |
| **im:read**            | View basic information about direct messages that BravoOmegaTango has been added to             |
| **im:write**           | Start direct messages with people                                                               |
| **mpim:history**       | View messages and other content in group direct messages that BravoOmegaTango has been added to |
| **mpim:read**          | View basic information about group direct messages that BravoOmegaTango has been added to       |
| **mpim:write**         | Start group direct messages with people                                                         |
| **remote_files:write** | Add, edit, and delete remote files on the user’s behalf                                         |


### User Token Scopes
| Permission | Description              |
|------------|--------------------------|
| **admin**  | Administer the workspace |


After setting the token scopes, paste your `Member ID` (your Slack ID), `OAuth Access Token` and `Bot User OAuth Token` to `config.yaml` file. Finally, install the app on the workspace.

## TODO:
- Divide the script into smaller functions for readability.
- Have a working exit and upload mechanism.
- Read Slack tokens from a config file.
- Add support for Windows and Linux operating systems.
- Implement a simple process injection method for Windows and Linux.
- Implement an easy-to-use obfuscated (for evasion, not anti-debugging, etc.) binary generation for Windows and Linux operating systems.

## Known Bugs:
- Sometimes channels don't get created.
- Upload sends filename as bytes output converted to string (ex: file does not exist: b'filename.txt') - Looks like an issue on Slack's side.

[Slack Apps]: https://api.slack.com