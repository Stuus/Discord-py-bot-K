# Discord Python Bot [K]

---
I am practice Python using `discord.py`, and this Bot named ***Kuroshio*** 

![Static Badge](https://img.shields.io/badge/BK-v--0.00.1b-green)



## Core

```python

class CogRead:
    cogs = []
    try:
        # If the file package to `.exe` , than sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    cogs_path = os.path.join(base_path, "Cogs")

    if os.path.exists(cogs_path):
        for Filename in os.listdir(cogs_path):
            if Filename.startswith('cog'):
                add = str(f'Cogs.{Filename[:-3]}')
                cogs.append(add)
    else:
        print(f"{C.red}Error: Cogs folder not found at {cogs_path}{C.reset}")

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=command_prefix, intents=discord.Intents().all())
        self.cogslist = CogRead.cogs

    async def on_ready(self):
        synced = await self.tree.sync()

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

client = Client()
client.run(token)
```
---
