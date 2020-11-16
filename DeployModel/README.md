# Python flask server and client

## Installation

```bash
$ cd code/
$ pip install -r requirement.txt
```

## Run

1. 先執行 `main.py`，會生成 `link.csv`、`adjacency.csv`
2. 再執行 `show_path.py`，就會有 json 檔案生成在`./path` 裡面

```bash
$ python main.py [iter times] [start node ID] [destination node ID] [config file path]
$ python show_path.py
```

### 範例

```bash
$ python main.py 100 0 15 ./origin_config.txt
$ python show_path.py
```

3. `show_path.py` 所 output 的 capacity 的值可以從 `capacity.csv` 裡面手動調整
