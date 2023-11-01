import json
import os
import platform
import socket
from pathlib import Path
#import asyncio
import multiprocessing

__VERSION__="1"
__AUTHOR__="FIREWOLF"
__COMMENT__="this is a pytest module"
import psutil
def info() -> str:
    return str('{"version": "' + __VERSION__ + '", "author": "' + __AUTHOR__ + '", "comment": "' + __COMMENT__ + '"}');


def get_server_path(pwd: str):
    pwd = pwd.split("/")
    pwd = pwd[:-2]
    return '/'.join(pwd)



# Return values like string!
def start(request: dict) -> dict:
    rep = dict()
    rep["body_text"] = "Hello i`m a test function on Python\n"
    rep["body_text"] += "System information:\n"
    system_name = platform.system()
    rep["body_text"] += f"\tName: {system_name}\n"
    kernel_version = platform.uname().release
    rep["body_text"] += f"\tKernel version: {kernel_version}\n"
    os_name = platform.platform()
    rep["body_text"] += f"\tName OS: {os_name}\n"
    cpu_percent = psutil.cpu_percent()
    rep["body_text"] += f"CPU usage: {cpu_percent} %\n"
    ram_percent = psutil.virtual_memory().percent
    rep["body_text"] += f"RAM usage: {ram_percent}%\n"
    net_info = psutil.net_io_counters()
    rep["body_text"] += f"Send bytes: {net_info.bytes_sent}\n"
    rep["body_text"] += f"Receive bytes: {net_info.bytes_recv}\n"
    disk_partitions = psutil.disk_partitions()
    rep["body_text"] +="\tDisks:\n"
    for partition in disk_partitions:
        rep["body_text"]+=f"\t\t{partition.device}\n"
    rep["body_text"] += "\n\tGiven: " + str(request) + "\n"
    f = open(get_server_path(json.loads(request["json_data"])["pwd"]) + "/config.json",'r')
    js = json.load(f)
    try:
        ip = js["SERVER"]["CONFIG"]["IP"]
        host_name, _, _ = socket.gethostbyaddr(ip)
        rep["body_text"] +=f"hostname: {ip}: {host_name}"

        # Получение информации о сокете
        socket_info = socket.getaddrinfo(ip, js["SERVER"]["CONFIG"]["PORT"])
        rep["body_text"] +="Host info:"
        for info in socket_info:
            rep["body_text"] +=f"  {info}\n"
    except socket.gaierror as e:
        rep["body_text"] += f"Error find socket: {e}\n"
    rep["header_body"] = "test: allowed\r\nContent-Type: text/*; charset=utf-8\r\n"
    return rep