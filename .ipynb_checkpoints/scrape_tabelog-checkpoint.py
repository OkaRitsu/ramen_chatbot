"""食べログからラーメン屋の情報を取得する"""


from bs4 import BeautifulSoup
import csv
import logging
import os
import pandas as pd
import re
import requests
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ramen_store_file = 'output/latest_data/ramen_store.csv'
ramen_review_file = 'output/latest_data/ramen_review.csv'


class Tabelog:
    def __init__(self, base_url, begin_page=1, end_page=30):
        # 店のIDを設定
        if os.path.exists(ramen_store_file):
            # ファイルが既にあれば，最後の行のID+1
            df = pd.read_csv(ramen_store_file)
            self.store_id = df.iloc[-1]['ID'] + 1
        else:
            # ファイルがなければ，1にしてファイルを作成
            self.store_id = 1
            with open(ramen_store_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ID', 'name', 'url', 'score', 'review_count'])
            with open(ramen_review_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ID', 'review'])

        # 店の情報
        self.store_name = ''
        self.store_url = ''
        self.score = 0
        self.review_count = 0
        self.review = ''

        # データフレーム
        self.columns = [
            'ID', 'name', 'url', 'score', 'review_count', 'review']
        self.df = pd.DataFrame(columns=self.columns)

        # \nは改行、\sは空白
        self.__regexcomp = re.compile(r'\n|\s')

        self.scrape_stores(base_url, begin_page, end_page)

    def scrape_stores(self, base_url, begin_page, end_page):
        """
        食べログをスクレイピングする
        Args:
            base_url: 食べログのURL　例：https://tabelog.com/tokyo/rstLst/ramen/
            bigin_page: スクレイピングを始めるページ番号
            end_page: スクレイピングを終わらせるページ番号
        """
        # 現在調べているページ番号
        self.page_num = begin_page

        while True:
            # 食べログの点数ランキングでソートしたリストのurl
            stores_url = f'{base_url}{self.page_num}/?Srt=D&SrtT=rt&sort_mode=1'
            stores_soup = self.get_contents(stores_url)

            # 店舗のURLを取得
            stores = stores_soup.find_all('a', class_='list-rst__rst-name-target')

            # 1店舗もなければ止める
            if len(stores) == 0:
                break

            for store in stores:
                # 店舗の名前を取得する
                self.store_name = store.string
                # 店の個別URLを取得
                self.store_url = store.get('href')
                self.scrape_store(self.store_url)
                self.store_id += 1

            # 店舗一覧を取得できなかったか，最後のページにたどり着いたらループを抜ける
            if self.page_num >= end_page:
                break
            self.page_num += 1

    def scrape_store(self, store_url):
        """
        店の詳細情報を取得する
        Args:
            url: 店の詳細情報のURL
        """
        soup = self.get_contents(store_url)

        # 評価点数
        score = soup.find(class_='rdheader-rating__score-val-dtl').string
        # 評価点数が3.5未満の場合は対象外とする
        if score == '-' or float(score) < 3.5:
            logger.error({
                'name': self.store_name, 'status': '評価点数が3.5未満のため対象外'})
            self.store_id -= 1
        else:
            self.score = float(score)

        # レビューURL
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')

        # レビュー件数
        self.review_count = review_tag_id.find(
            'span', class_='rstdtl-navi__total-count').em.string

        logger.info({
            '内容': '店舗情報',
            'ID': self.store_id, '店名': self.store_name,
            'レビュー件数': self.review_count})

        # 店舗情報を出力する
        with open(ramen_store_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.store_id, self.store_name, self.store_url,
                self.score, self.review_count])

        self.scrape_reviews(review_tag)

    def scrape_reviews(self, review_tag, end_page=1):
        """
        指定したURLのレビューを取得する
        Args:
            review_tag: 店舗の詳細ページにある口コミのURL
            end_page: 検索するページ数（20件/ページ）
        """
        review_page_num = 1
        while True:
            review_list_url = f'{review_tag}COND-0/smp1/?lc=0&rvw_part=all&PG={review_page_num}'
            soup = self.get_contents(review_list_url)
            # クチコミの詳細ページURL一覧
            review_urls = soup.find_all('div', class_='rvw-item')

            # 1件も見つからなければ止める
            if len(review_urls) == 0:
                return

            # 取得した口コミURLを検索する
            for ri, review_url in enumerate(review_urls):
                review_detail_url = 'https://tabelog.com' + review_url.get('data-detail-url')
                review_soup = self.get_contents(review_detail_url)

                # reviewが含まれているタグの中身をすべて取得
                review = review_soup.find_all('div', class_='rvw-item__rvw-comment')
                if len(review) == 0:
                    review = ''
                else:
                    # 改行コードを除外する
                    review = review[0].p.text.strip()
                self.review = review

                logging.info({
                    '内容': 'review', 'ページ番号': review_page_num,
                    'レビュー番号': ri+1, 'review': self.review[:30]})

                with open(ramen_review_file, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        self.store_id, self.review])

                # データフレームの生成
                # self.make_df()

            # 最後のページまで
            if review_page_num >= end_page:
                return
            review_page_num += 1

    def get_contents(self, url):
        """
        指定したURLの内容を取得する
        Args:
            url: 内容を取得するURL
        Returns:
            soup: BeautifulSoupの解析結果（URLの情報を取得できなければ Noneを返す）
        """
        # Dos攻撃にならないように
        time.sleep(1)

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error({'action': 'scrape_reviews', 'url': url})
            return None
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    def make_df(self):
        # 行を作成
        se = pd.Series([
            self.store_id, self.store_name, self.store_url,
            self.score, self.review_count, self.review], self.columns)

        # データフレームに行を追加
        self.df = self.df.append(se, self.columns)


if __name__ == '__main__':
    begin_time = time.time()

    base_url = 'https://tabelog.com/tokyo/rstLst/ramen/'
    tabelog = Tabelog(base_url, begin_page=11, end_page=15)

    runtime = (time.time() - begin_time) / 60
    print(f'実行時間: {runtime} min')
