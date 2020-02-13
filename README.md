# SierraTwo
Simple encrypted reverse shell over Slack, Discord and Github. 



#TODO - Slack:
#Divide the script into smaller functions for readability.
#Have a working exit and upload mechanizm.
#Read slack tokens from a config file.
#Add support for Windows and Linux operating systems.
#Implement a simple process injection method for Windows and Linux.
#Implement an easy-to-use obfuscated(for evasion, not anti-debugging and etc.) binary generation for Windows and Linux operating systems.

#Bugs:
#Channels sometimes dont get created.
#Upload sends filename as bytes output converted to string(ex: file does not exist: b'filename.txt') - Looks like an issue on slack's side.
