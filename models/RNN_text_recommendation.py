import tensorflow as tf
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 假设您已经有一个包含所有活动的文本列表
activity_text_list = [...]

# 假设您已经有一个包含用户历史记录的文本列表
user_history_text_list = [...]

# 建立词向量模型
tokenizer = Tokenizer()
tokenizer.fit_on_texts(activity_text_list + user_history_text_list)

# 将文本转换为序列，并进行填充
activity_sequences = tokenizer.texts_to_sequences(activity_text_list)
activity_data = pad_sequences(activity_sequences, padding='post')

user_history_sequences = tokenizer.texts_to_sequences(user_history_text_list)
user_history_data = pad_sequences(user_history_sequences, padding='post')

# 定义循环神经网络模型
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(len(tokenizer.word_index) + 1, 64),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 训练模型
model.fit(activity_data, np.ones((len(activity_text_list),)), epochs=10, batch_size=16)

# 生成推荐结果
activity_embeddings = model.predict(activity_data)
user_history_embeddings = model.predict(user_history_data)

similarities = cosine_similarity(activity_embeddings, user_history_embeddings.T)

# 对于每个用户，找到相似度最高的活动
for i in range(len(user_history_text_list)):
    most_similar_activity = np.argmax(similarities[:, i])
    print(f"推荐给用户{i+1}的活动是：{activity_text_list[most_similar_activity]}")
