# Kuroshio `.cog` 模組 (Cog) 檔案規格說明書

本文件說明 Kuroshio Discord Bot (Discord-py-bot-K) 中 **Cog** (即 `.cog` 模組) 的檔案規格、目錄結構、命名規範、內部代碼實作要求以及依賴檢查機制。

---

## 1. 概念與定位
在 `discord.py` 框架中，**Cog** 是一種將多個指令、監聽事件及狀態管理進行模組化分類的機制。Kuroshio 採用了自動載入機制，會在啟動時自動掃描並載入特定資料夾內的所有 Cog 模組。

---

## 2. 檔案目錄與命名規範

### 2.1 儲存路徑
所有 Cog 檔案必須存放在專案根目錄下的 `Cogs` 資料夾中：
- 專案開發目錄：`Cogs/` (見 [Cogs 目錄](file:///E:/Project/Discord-py-bot-K/Cogs))
- 打包為執行檔 (`.exe`) 後的執行路徑：將依據運行環境動態決定（主要透過 `sys._MEIPASS` 解析）。

### 2.2 命名規則
自動載入器 [main.py](file:///E:/Project/Discord-py-bot-K/main.py) 會透過 `Filename.startswith('cog')` 進行過濾，因此 Cog 檔案必須符合以下規則：
1. **前綴要求**：檔名必須以 `cog` 開頭（例如：`cog_info.py`, `cog_voice.py`）。
2. **副檔名要求**：必須為 `.py` 檔案。
3. **英文大小寫**：建議一律採用小寫英文字母及底線組合（Snake Case）。

---

## 3. 程式碼基本架構

每一個 Cog 檔案本質上是一個 Python 模組，必須符合以下結構設計：

### 3.1 繼承 `commands.Cog`
必須定義一個類別並繼承 `discord.ext.commands.Cog`。

### 3.2 必須實作異步 `setup` 進入點
檔案末尾必須包含一個全局異步函式 `setup`，以便載入器載入該擴充：
```python
async def setup(client: commands.Bot) -> None:
    await client.add_cog(CogClassName(client))
```

---

## 4. 模組依賴檢查機制 (`__dependencies__`)

為了確保模組在運行時不會因為缺少外部依賴而崩潰，Kuroshio 設計了靜態依賴檢查系統。

### 4.1 宣告依賴
Cog 檔案可以在模組級別（Module Level）定義 `__dependencies__` 列表，用來列出該模組正常運行所需的外部二進位檔案或資源檔案：
```python
__dependencies__ = [
    "tools/ffmpeg.exe",
    "libopus/libopus-0.x64.dll"
]
```

### 4.2 檢查機制
當 `main.py` 在 `setup_hook` 中載入 Cog 時：
1. 檢查模組是否包含 `__dependencies__` 屬性。
2. 若有，則對列表中每個檔案路徑（相對於專案根目錄或運行根目錄）進行存在性檢查 (`os.path.exists`)。
3. 若檔案齊備，控制台將印出 `[OK]`；若缺少依賴，則會提示 `[ERROR]` 或 `[WARNING]` 以告知管理員可能會發生執行期錯誤。

---

## 5. 模組的動態控制

Kuroshio 支援在 Bot 運行時動態管理 Cog 模組。透過擁有者權限（Owner ID 檢查），可在 Discord 頻道中輸入以下指令來控制 Cog 的狀態：
* **載入模組**：`!load <cog>` - 載入指定的 `Cogs.<cog>` 模組。
* **重載模組**：`!reload <cog>` - 重新讀取並更新 `Cogs.<cog>` 程式碼。
* **卸載模組**：`!unload <cog>` - 停用並解除安裝 `Cogs.<cog>` 模組。

這些指令的實作詳見 [cog_setup.py](file:///E:/Project/Discord-py-bot-K/Cogs/cog_setup.py)。

---

## 6. 標準 Cog 模組範本

以下是一個標準的 Kuroshio Cog 範本，開發新功能時可複製此格式進行修改：

```python
import datetime
import discord
from discord import app_commands
from discord.ext import commands

from tools.color import Color as C
from tools.set import ConfigInfo

# 1. 宣告模組相依的外部檔案（非必須，若無則可省略）
__dependencies__ = [
    # "path/to/required/file"
]

# 2. 定義 Cog 類別
class CogExample(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # 定義斜線指令 (Slash Command)
    @app_commands.command(
        name="ping",
        description="測試 Bot 回應速度"
    )
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"Pong! 延遲：{latency}ms")

    # 定義監聽事件 (Event Listener)
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        # 監聽邏輯...
        pass

# 3. 模組載入進入點
async def setup(client: commands.Bot) -> None:
    await client.add_cog(CogExample(client))
    dt = str(datetime.datetime.now())[:-7]
    print(f'{dt} {C.blue}[Cog]{C.reset} -> {C.lightblue}load cog_example{C.reset}')
```
