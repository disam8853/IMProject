1. 先執行main.py，會生成link.csv、adjacency.csv
2. 再執行show_path.py，就會有json檔案生成在./path裡面

執行方法:
	python main.py [iter times] [start node ID] [destination node ID] [config file path]
	python show_path.py
範例:
	python main.py 100 0 15 ./origin_config.txt
	python show_path.py

3. show_path.py所output的capacity的值可以從capacity.csv裡面手動調整