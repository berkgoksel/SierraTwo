# SierraTwo
Simple encrypted reverse shell over Slack, Discord and Github. 
SierraTwo refers to the Slack shell, whereas SierraThree refers to the Discord shell.

# Dependencies
SierraTwo only supports python3. You can install the dependencies as follows.

>pip install -r requirements.txt

# Configuration

Create a Slack workspace where you are the admin.

Go to apps.slack.com and create a Bot.

Under features, go to OAuth & Permissions and click on Permissions.



Add the following OAuth permissons for the Bot Token


| Permission | Description |
| --- | --- |
| **channels:history** | View messages and other content in public channels that BravoOmegaTango has been added to |
| **channels:join** | Join public channels in the workspace |
| **channels:manage** | Manage public channels that BravoOmegaTango has been added to and create new ones |
| **channels:read** | View basic information about public channels in the workspace |
| **chat:write** | Send messages as @bravoomegatango |
| **commands** | Add actions and/or slash commands that people can use |
| **files:write** | Upload, edit, and delete files as BravoOmegaTango |
| **groups:history** | View messages and other content in private channels that BravoOmegaTango has been added to |
| **groups:read** | View basic information about private channels that BravoOmegaTango has been added to |
| **groups:write** | Manage private channels that BravoOmegaTango has been added to and create new ones |
| **im:history** | View messages and other content in direct messages that BravoOmegaTango has been added to |
| **im:read** | View basic information about direct messages that BravoOmegaTango has been added to |
| **im:write** | Start direct messages with people |
| **mpim:history** | View messages and other content in group direct messages that BravoOmegaTango has been added to |
| **mpim:read** | View basic information about group direct messages that BravoOmegaTango has been added to |
| **mpim:write** | Start group direct messages with people |
| **remote_files:write** | Add, edit, and delete remote files on the user’s behalf |


Install the app on the workspace


Enter the newly generated Bot User OAuth Token into config.ini

Add the following permission to the User Token Scopes.

| Permission | Description |
| --- | --- |
| **admin** | Administer the workspace |




# TODO - Slack:
-Divide the script into smaller functions for readability.

-Have a working exit and upload mechanizm.

-Read slack tokens from a config file.

-Add support for Windows and Linux operating systems.

-Implement a simple process injection method for Windows and Linux.

-Implement an easy-to-use obfuscated(for evasion, not anti-debugging and etc.) binary generation for Windows and Linux operating systems.

# Bugs:

-Channels sometimes dont get created.

-Upload sends filename as bytes output converted to string(ex: file does not exist: b'filename.txt') - Looks like an issue on slack's side.
