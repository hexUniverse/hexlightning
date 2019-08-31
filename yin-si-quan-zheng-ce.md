# 隱私權政策

### 隱私權政策

我們 hexPort 非常重視各群組的隱私，特別列出此篇講述我們蒐集了哪些資料，如何運用、處理這些資料。

### 資料蒐集目的

* 用於處理公共黑名單各項事務所用，在群主拉入本 bot 時視同同意本項服務蒐集目的。
* 識別對象是否為公共黑名單人員，如 UID、對話、使用者名稱、使用者頭像。

### 利用時間

在群組任何人對話期間，本 bot 將會比對資料庫，或是管理員使用指令進行全面封鎖。直至管理員將本 bot 踢出群組。 **這個行為將會將群組資料庫清空，且為不可回朔行為。**

### 群組資料

我們蒐集的群組資料樣本如下。

```text
{
  "chat" : {
    "title" : "Hex Judge.",
    "id" : -1001270981918,
    "config" : {
      "sub_ban_list" : [],
      "configuring" : false
    },
    "white_participate" : [ 
      12345678
    ]
  }
}
```

* `title` 為貴群的群組名稱，於回報時方便搜尋的依據之一。
* `id` 為貴群的唯一識別碼。
* `sub_ban_list` 用於記錄貴群訂閱了哪些黑名單列表。
* `configuring` 紀錄發送的鍵盤 \(message\_id\)，避免管理員間的設定衝突。
* `white_participate` 群組內自行設定的白名單請參考\([說明書](/s/r181mM-b4)\)。

### 個人資料

我們收集資料範本如下

```text
{
  "chat" : {
    "id" : 525239263,
    "first_name" : "DingChen",
    "is_bot" : false,
    "language_code" : "en",
    "last_name" : "Tsai (踢低吸) F17EEA95",
    "username" : "DingChen_Tsai",
    "is_white" : true,
    "participate" : [ 
      NumberLong(-1001113431102), 
      NumberLong(-1001134791598)
    ]
  },
  "current" : {
    "date" : 1545589430,
    "opid" : 12345678,
    "until" : 0,
    "reason" : "ads, spam, coin",
    "tags" : "ads",
    "evidence" : 10
  }
  "history" : [ 
    {
      "date" : 1545647589,
      "opid" : 12345678,
      "until" : 0,
      "reason" : "頭像太可愛引起我犯罪慾望",
      "tags" : "porn, ads"
    }
  ]
}
```

**tags: chat**

* `id` 為使用者唯一識別碼，用於分辨用戶
* `first_name` 為使用者名稱，用於處理黑名單的根據之一。
* `last_name` 為使用者名稱，用於處理黑名單的根據之一。
* `is_bot` 是否為bot，用於分辨是否為機器人。
* `language_code` 用戶使用的client語言。
* `username` 使用者名稱，可用於加用戶使用。
* `is_white` 全域白名單，避免人員操作失誤。
* `participate` 紀錄加入哪些群組，可以在第一時間掌握如何對方所在位置，並將其處置。

**tags: current**

* `date` 被封鎖日期。
* `opid` 對這份處置的操作人的UID，處理申訴時可以追溯。
* `until` 封鎖時長，0為永久，用timestamp表示
* `reason` 封鎖原因
* `tags` 封鎖標籤，依照群組訂閱進行封鎖。
* `evidence` 封鎖證據，如為2表示證據不全，若有疑慮請到 @hexjudge 處理申訴。

### 資料與機器學習

~~在這個世代裡，不用機器學習怎麼活下去？~~ :::success

* **資料不落地**
* 不儲存檔案、標記檔案
* 不用對話當作訓練資料

  :::

以上為這個項目中的核心原則。

### 其他說明書

* [hexPort](/s/HJh4WBkp7)
* [說明書](/s/r181mM-b4)
* [隱私權政策](/s/S1rfvMWW4)

