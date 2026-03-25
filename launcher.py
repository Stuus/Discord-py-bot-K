# This is a launcher for the bot, it will start the bot in multiple processes
# You can use this to start the bot in multiple processes
# make sure this file is in the same directory as main.exe



import subprocess
import time
import os
import sys
import threading

shard_count = 3

# check if (-c or /c)
open_new_console = "-c" in sys.argv or "/c" in sys.argv

if open_new_console:
    print("Mode: Opening a new console window for each shard...")
    creation_flags = subprocess.CREATE_NEW_CONSOLE
else:
    print("Mode: Integrating all shards into the current window (if you need to separate the window, please add -c or /c parameters to start)...")
    creation_flags = 0

print(f"Preparing to start {shard_count} shards...")

# use dynamic path to lock the same directory main.exe, ensure that the execution after packaging does not report errors
exe_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]), "main.exe")

processes = []
shutting_down = False

def monitor_shard(shard_id):
    env = os.environ.copy()
    env["SHARD_ID"] = str(shard_id)
    
    while not shutting_down:
        print(f"Starting Shard {shard_id}...")
        p = subprocess.Popen(
            [exe_path], 
            env=env, 
            creationflags=creation_flags
        )   
        processes.append(p)
        p.wait()
        
        if p in processes:
            processes.remove(p)
            
        if shutting_down:
            break
            
        print(f"Shard {shard_id} exited with code {p.returncode}! Restarting in 5 seconds...")
        time.sleep(5)

threads = []
for i in range(shard_count):
    t = threading.Thread(target=monitor_shard, args=(i,), daemon=True)
    t.start()
    threads.append(t)
    time.sleep(5) 

print("All shards have been started!")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClosing all shards...")
    shutting_down = True
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
