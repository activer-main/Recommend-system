import requests
import json
import csv

# 設定 API 的路徑和參數

url = "http://220.132.244.41:5044/api/Activity/trend"
params = {
    "countPerSegment": 100,
    "currentSegment": 1
}

# 使用 requests 模組向 API 發送請求
response = requests.post(url, json=params)

# 未接收到 API
if response.status_code != 200:
    print("Failed to get data from API.")
    exit(0)

# 將回傳的 JSON 資料解析成 Python 的字典
data = json.loads(response.content)["searchResultData"]

# 將字典寫入到 CSV 檔案中
# with open("data/raw/activity.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(data[0].keys())
#     for row in data:
#         writer.writerow(row.values())

with open("data/raw/activity.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'trend', 'title', 'content', 'subTitle',
                    'connection', 'holder', 'objective', 'sources', 'branches', 'tags'])
    for item in data:
        id = item.get('id', '')
        trend = item.get('trend', '')
        title = item.get('title', '')
        content = item.get('content', '')
        subTitle = item.get('subTitle', '')
        connection = '|'.join(item.get('connection', []))
        holder = '|'.join(item.get('holder', []))
        objective = item.get('objective', '')
        sources = '|'.join(item.get('sources', []))
        branches = '|'.join(
            [f"{b['id']}-{b['branchName']}" for b in item.get('branches', [])])

        tags = '|'.join([t.get('text', '') for t in item.get('tags', [])])

        writer.writerow([id, trend, title, content, subTitle,
                        connection, holder, objective, sources, branches, tags])

# print("Done!")
