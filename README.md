# SierraTwo
`SierraTwo` is a simple reverse shell over Slack.

## Usage
`SierraTwo` only supports Python 3.x. 

### Direct Usage
#### Windows
Not available. Instead, refer to [building](#building) to build an `.exe` for Windows.

#### Linux
```
$ sudo apt install python3-pip
$ pip3 install -r requirements.txt
$ python3 SierraTwo.py
```

### Building
To build an executable:

```
$ sudo apt install python3-pip winbind wine winetricks
$ wget https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe
$ wine python-3.8.2-amd64.exe
$ pip3 install -r requirements.txt
$ wine pip install -r wine_requirements.txt
$ python3 builder.py -o <TARGET SYSTEM>
```

#### **BE SURE TO ADD PYTHON TO PATH WHEN INSTALLING WITH WINE**

The following commands will setup Wine with 64 bit Python 3.8.2 on your system. `<TARGET SYSTEM>` can be either 
`Windows` or `Linux`. After building the executable, check the `dist` folder for your exectuable.

For example, running `python3 builder.py -o Linux` on a 64 bit Linux will generate a 64 bit executable. Same logic 
applies for `-o Windows`. If you want to generate a 32 bit executable, you'd have to install 32 bit Python instead of 
64 bit (on your Linux and/or Wine).

If built for Windows:
- The executable's name will be `msdtc.exe`
- Executable will automatically minimize and hide itself

If built for Linux:
- The executable's name will by `system`

## Configuration
To use `SierraTwo`, create or be a part of a Slack workspace where you an admin. Afterwards go to 
[Slack API][Slack API] and create an app. From there, under the `Features` tab, go to `OAuth & Permissions` and add the 
following scopes:

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

After setting the token scopes, copy and paste your `Member ID` (and others that will have access to the app), 
`OAuth Access Token` and `Bot User OAuth Token` to `config.py`. Finally, install the app on the workspace.

## Notes
- The shells (or rooms in other words) will be created under the predetermined prefix. You can change this prefix in 
`config.py`.
- Upon launch, `SierraTwo` will connect to the workspace and look for channels matching the prefix. If there are no 
channels matching the prefix, `prefix-1` will be created. By default, this is `sierra-hotel-1`. However, if there is a 
channel (or channels) matching the prefix, `SierraTwo` will get the largest number amongst the matching channels and 
add onto the largest number amongst the channels. That means if `sierra-hotel-5` is the with the largest number amongst 
all present channels, the next channel will be `sierra-hotel-6`.
- You can only run one instance of `SierraTwo` at a given time. This is due to Slack's API. 
- To close your current shell, type `sh_exit` in the channel.

## Disclaimers
- This project is for educational purposes only. The developers and contributors are not responsible for any damage 
that may be caused by this program nor any consequences that may arise.
- By using this program you accept that the developers and contributors are not responsible if you violate 
[Slack's Terms of Service][Slack ToS] and [Slack's API Terms of Service][Slack API ToS].
- With the current permissions of the app, `SierraTwo` will have an admin access over your workspace.

## TODO:
- Divide the script into smaller functions for readability.
- Add support for Windows and Linux operating systems.
- Implement a simple process injection method for Windows and Linux.
- Implement an easy-to-use obfuscated (for evasion. No anti-debugging.) binary generation for Windows and Linux 
operating systems.

## Known Bugs:
- Launching more than one instance of the bot causes the Slack API to kick the bot offline (The server responds with 
`{'ok': False, 'error': 'ratelimited'}`).

[Slack API]:      https://api.slack.com
[Slack ToS]:      https://slack.com/terms-of-service
[Slack API ToS]:  https://slack.com/terms-of-service/api
