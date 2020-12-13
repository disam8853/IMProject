# Introduction

這是前端網頁的 server，目前包含設 nodes、計算 path 的網頁以及顯示 flow 的圖

# Install

```{bash}
npm install
```

# Start server

```{bash}
npm start
```

server 會開在 `http://localhost:3000`。
若無法連到 NAPA 的 API，有可能是`.env`裡的環境變數沒有更改，請將值改成正確的 NAPA API endpoint。

路由：

1. `/`: 首頁，設定 config 後計算 path
2. `/flow`: 從 NAPA API 抓來的資料顯示在這裡
3. `/api/all-data`: 用來抓 NAPA API 的 API
