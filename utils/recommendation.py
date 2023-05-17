import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_the_most_similar_activities(user_id, user_movie_matrix, num):
    """找出與使用者最相似的前n個活動"""
    user_vec = user_movie_matrix.loc[user_id].values
    sorted_index = np.argsort(user_vec)[::-1][:num]
    return list(user_movie_matrix.columns[sorted_index])


def create_user_activities_matrix(userId, activity, user_history, activity_index):
    """建立使用者活動矩陣"""
    # 建立 TFIDF 向量
    vectorizer = TfidfVectorizer()

    # 目的是學習每個單詞在所有文本中的重要性，轉換的目的是將每個文本轉換成一個數值向量
    activity_vec = vectorizer.fit_transform(activity)

    # 已經有一個訓練好的向量化模型，並且想要將新的文本資料轉換成與這個模型相同的向量形式
    user_vec = vectorizer.transform(user_history)

    # 計算使用者向量和語料庫中所有活動向量之間的餘弦相似度
    user_activity_matrix = cosine_similarity(user_vec, activity_vec)

    return pd.DataFrame(user_activity_matrix, index=[userId], columns=activity_index)
