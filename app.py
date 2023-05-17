from flask import Flask
from flask import request
from flask_cors import CORS
import pandas as pd
from utils.recommendation import get_the_most_similar_activities, create_user_activities_matrix

app = Flask(__name__)
CORS(app)

# 讀取所有活動資料
activity_df = pd.read_csv('data/preprocess/activity.csv')

# 設定使用者活動紀錄
userli = [[1, 2], [1, 4], [3]]


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/api/activity/recommend", methods=["GET", "POST"])
def recommend():
    # 獲得使用者 ID 和 推薦活動數量
    userId = request.args.get('userId')
    number = request.args.get('num')
    userId = int(userId)
    number = int(number)

    # 取得使用者的活動資料
    activity_history = userli[userId]

    # 找出歷史活動斷詞後的內容
    user_history = [
        ' '.join(activity_df.loc[userli[1], 'seg'].values.tolist())]

    # 所有活動資料除了使用者參加過了活動
    all_activity = activity_df[~activity_df.index.isin(
        activity_history)]['seg'].values

    # 活動 index
    all_activity_index = activity_df[~activity_df.index.isin(
        activity_history)].index

    # 建立使用者活動矩陣
    user_activity_matrix = create_user_activities_matrix(
        userId, all_activity, user_history, all_activity_index)

    # 找出前幾筆最相似的活動
    activity_ids = get_the_most_similar_activities(
        userId, user_activity_matrix, number)

    return activity_df.loc[activity_ids, ['id', 'title', 'content']].values.tolist()


if __name__ == '__main__':
    app.run()
