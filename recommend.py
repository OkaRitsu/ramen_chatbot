import pickle
import random

from gensim.models import word2vec
import numpy as np
import pandas as pd

# word2vecのモデルを読み込み
word2vec_ramen_model = word2vec.Word2Vec.load("model/word2vec_ramen_model.model")

# 全店舗のTF-IDF値上位20個の情報を取得する
with open('data/df_ramen_texts_tfidf_sorted_top20', 'rb') as f:
    existing_stores = pickle.load(f)

# 全店舗の情報を読み込む
existing_stores_info = pd.read_csv('data/ramen_store.csv')


def calc_score(word1, word2):
    v1 = word2vec_ramen_model.wv[word1]
    v2 = word2vec_ramen_model.wv[word2]
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def search_area(user_area, ranking):
    new_ranking = pd.DataFrame()
    for i, area in enumerate(ranking["area"]):
        if area == user_area:
            new_ranking = new_ranking.append(ranking.iloc[i])
    print(f"{user_area}の店舗数：{len(new_ranking)}")
    new_ranking = new_ranking.reset_index()
    return new_ranking


def search_similar_stores(virtual_store):
    avg_scores = []
    # 実在する店舗
    for existiong_store in existing_stores['texts_tfidf_sorted_top20']:
        word_scores = []
        for word_a in existiong_store:
            # 仮想店舗
            for word_b in virtual_store:
                score = calc_score(word_a, word_b)
                word_scores.append(score)
        # 仮想店舗の単語と実店舗の20単語のスコアの平均
        avg_scores.append(np.mean(word_scores))

    existing_stores['avg_cos_sim_rate'] = avg_scores
    # ランキングにして店舗の情報を追加
    ranking = existing_stores.sort_values('avg_cos_sim_rate', ascending=False).merge(existing_stores_info)


    # 実在する店の数
    stores_count = len(ranking)

    recommend_stores = pd.DataFrame()

    # 一押し
    recommend_stores = recommend_stores.append(ranking.loc[0])

    # おすすめ（上位5％からランダムに）
    recommend_num = int(stores_count * 0.05)
    recommend_rand_num = random.randint(1, recommend_num)
    recommend_stores = recommend_stores.append(ranking.loc[recommend_rand_num])

    # 新たな発見（上位10％からランダムに）
    discovery_num = int(stores_count * 0.1)
    discovery_rand_num = random.randint(recommend_num+1, discovery_num)
    recommend_stores = recommend_stores.append(ranking.loc[discovery_rand_num])

    return recommend_stores, ranking

