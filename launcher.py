# This is a launcher for the bot, it will start the bot in multiple processes
# You can use this to start the bot in multiple processes
# make sure this file is in the same directory as main.exe



import subprocess
import time
import os
import sys

shard_count = 3
processes = []

# check if (-c or /c)
open_new_console = "-c" in sys.argv or "/c" in sys.argv

if open_new_console:
    print("Mode: Opening a new console window for each shard...")
    creation_flags = subprocess.CREATE_NEW_CONSOLE
else:
    print("Mode: Integrating all shards into the current window (if you need to separate the window, please add -c or /c parameters to start)...")
    creation_flags = 0

print(f"Preparing to start {shard_count} shards...")

for i in range(shard_count):
    env = os.environ.copy()
    env["SHARD_ID"] = str(i)
    
    print(f"Starting Shard {i}...")
    
    # use dynamic path to lock the same directory main.exe, ensure that the execution after packaging does not report errors
    exe_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]), "main.exe")
    p = subprocess.Popen(
        [exe_path], 
        env=env, 
        creationflags=creation_flags
    )
    processes.append(p)
    
    time.sleep(5) 

print("All shards have been started!")

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Closing all shards...")
    for p in processes:
        p.terminate()
