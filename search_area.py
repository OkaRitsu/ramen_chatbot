import pandas as pd


def search_area(user_area, ranking):
    top5 = pd.DataFrame(
        columns=['ID', 'name', 'url', 'score', 'review_count', 'area']) #テスト用、変える必要あり
    cnt = 0
    for i, area in enumerate(ranking["area"]):
        if area == user_area and cnt <= 5:
            top5 = top5.append(ranking.loc[i])
            cnt += 1
    return top5


new_ramen_pd = pd.read_csv("./data/new_ramen_store.csv")

print(search_area("中央区", new_ramen_pd))

