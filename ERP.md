# ERP

## Note

```mermaid
graph TD;
    Start([開始載入設定\nload_bot_config]) --> ReadYAML[讀取 bot_data.yaml];
    ReadYAML --> CheckList{bot_objects 是否為空?};
    
    CheckList -- 是 (Empty) --> Error[拋出 LoginError];
    CheckList -- 否 --> CheckLen{檢查檔案數量\nlen(bot_objects)};
    
    CheckLen -- 數量 == 1 --> ReturnZero[回傳 bot_objects 0];
    CheckLen -- 數量 > 1 --> CheckParam{有傳入指定的\ncurrent_data_id 嗎?};
    
    CheckParam -- 否 (current_data_id == -1) --> PrintList[印出選項列表];
    PrintList --> AwaitInput[等待使用者輸入 (Timeout = 15s)];
    
    AwaitInput -- 使用者輸入內容 --> TryInt{嘗試轉換為整數 int()};
    TryInt -- 成功 (數值格式正確) --> CheckBounds{索引是否在有效範圍內?\n0 <= idx < len};
    
    TryInt -- 失敗 (ValueError) --> SetDefault[設定為預設值 0];
    AwaitInput -- 逾時 (TimeoutOccurred) --> SetDefault;
    CheckBounds -- 否 (Out of Range) --> SetDefault;
    
    CheckBounds -- 是 (Valid Index) --> ReturnValid([回傳對應的 bot_objects 指標]);
    SetDefault --> ReturnZero;
    
    CheckParam -- 是 (指定了 ID) --> ParamBounds{指定的 ID 是否有效?};
    ParamBounds -- 是 --> ReturnValidParam([回傳指定的 bot_objects 指標]);
    ParamBounds -- 否 --> Error2[拋出 LoginError];
```
