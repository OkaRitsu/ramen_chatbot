#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import exract_words
import recommend
import telegram_token

# telegram_token.pyファイルに以下を書き込む
TOKEN = telegram_token.TOKEN

# ctrl-cで強制終了


class RamenBot:
    def __init__(self):
        self.counter = 0
        self.answer = []
        self.ranking = []
        pass

    def start(self, bot, update):
        self.counter = 0
        self.answer = []
        # update.message.reply_text()内にテキストを入れるとtelegramに送信
        update.message.reply_text("こんにちは。ラーメンマイスターだよ")
        update.message.reply_text("はじめに，君のことについて教えて！")
        update.message.reply_text("ラーメン以外の好きな食べ物は何？無ければ，”なし”と答えてね！")

    def message(self, bot, update):
        print("カウンター：", self.counter)

        # ラーメン以外の好きな食べ物
        if self.counter == 0:
            # update.message.textでtelegramのユーザーからの入力を取得
            response_text = update.message.text
            if response_text != "なし":
                self.answer.extend(exract_words.search_corpus(response_text))
                update.message.reply_text("ラーメン以外にもおいしいものはたくさんあるよね！")
            update.message.reply_text("趣味は何かあるかな？無ければ，”なし”と答えてね！")
            self.counter += 1

        # 趣味
        elif self.counter == 1:
            response_text = update.message.text
            if response_text != "なし":
                self.answer.extend(exract_words.search_corpus(response_text))
                update.message.reply_text("いいね！")
            update.message.reply_text("次にラーメンのことについて教えて！")
            update.message.reply_text("何ラーメンが好き？僕は味噌ラーメンが好き")
            self.counter += 1

        # 種類（味）
        elif self.counter == 2:
            response_text = update.message.text
            if response_text == "なし":
                pass
            else:
                self.answer.extend(exract_words.search_corpus(response_text))

                if "醤油" in response_text or "しょうゆ" in response_text:
                    update.message.reply_text(
                        "やっぱり定番の醤油ラーメンだよね！でも，醤油ラーメンといっても味が濃いものからさっぱりしたものもあって奥が深いんだよね"
                    )
                elif "味噌" in response_text or "みそ" in response_text:
                    update.message.reply_text(
                        "札幌ラーメンで有名な味噌ラーメンか！札幌も有名だけど，信州とか九州にも人気の味噌ラーメンもあるんだよ！"
                    )
                elif "塩" in response_text or "しお" in response_text:
                    update.message.reply_text("塩ラーメン！シンプルだけど，色々な出汁の味が楽しめて美味しいよね")
                elif "とんこつ" in response_text or "豚骨" in response_text:
                    update.message.reply_text(
                        "博多ラーメンで有名なとんこつラーメンか！博多ラーメンの極細麺はいくらでも替え玉して食べれちゃうよね．"
                    )
                elif "二郎" in response_text:
                    update.message.reply_text(
                        "二郎系ラーメン！一度食べるとハマっちゃうよね．量がすごく多いけど，君は結構大食いなのかな？でも，ニンニクがたくさん入ってるから次の日の予定は確認しておこうね．"
                    )
                elif "家系" in response_text:
                    update.message.reply_text(
                        "横浜の吉村家から生まれた家系ラーメンか！あの濃厚なスープたまらないよね．一緒にライスを食べるととても美味しいけど食べ過ぎには注意しようね．"
                    )
                elif "つけ麺" in response_text:
                    update.message.reply_text(
                        "麺の味を一番楽しめるつけ麺か！はじめの一口はスープにつけずに食べる人もいるんだよね．麺を食べ切った後のスープ割りも格別だよね．"
                    )
                elif "油そば" in response_text or "まぜそば" in response_text:
                    update.message.reply_text(
                        "まぜそばか！はじめはスープのないラーメンってどうなの？って思うけど食べてみると全然美味しいよね！食べてる途中に味変したりして味の変化を楽しめるのもいいよね．"
                    )
                else:
                    update.message.reply_text("めずらしい種類のラーメンが好きなんだね．やっぱりラーメンは奥が深いなあ．")

            update.message.reply_text("好きなトッピングはある？僕は，コーンとバターが好き！")
            self.counter += 1

        # トッピング
        elif self.counter == 3:
            response_text = update.message.text
            if response_text == "なし":
                pass
            else:
                self.answer.extend(exract_words.search_corpus(response_text))

                if "チャーシュー" in response_text:
                    update.message.reply_text(
                        "ラーメンのトッピングといえばチャーシューだよね．でも1枚しかないといつ食べるか迷っちゃうなあ．"
                    )
                elif (
                    "卵" in response_text
                    or "たまご" in response_text
                    or "味玉" in response_text
                ):
                    update.message.reply_text(
                        "ラーメンの卵ってなぜか特別感があるよね．有料のつけずに卵が乗ってるととってもうれしいよね．"
                    )
                elif "メンマ" in response_text:
                    update.message.reply_text("メンマか！ラーメンに当たり前のようにのってるけど，何が原料なんだろう...")
                elif "のり" in response_text or "海苔" in response_text:
                    update.message.reply_text("のりか！スープに浸しても，パリパリのままで食べても美味しいよね")
                elif "もやし" in response_text:
                    update.message.reply_text("ラーメンの上に山盛りに盛られたもやしはとても存在感があって食べ応え抜群だよね．")
                elif "ネギ" in response_text or "ねぎ" in response_text:
                    update.message.reply_text(
                        "ネギがのっていると味にアクセントがついて美味しいよね．東日本では白ネギ，西日本では青ネギが一般的なんだって．"
                    )
                elif "コーン" in response_text:
                    update.message.reply_text(
                        "コーン！僕と一緒だ！甘くておいしいよねー．あのプチプチした食感も病みつきになるよね．"
                    )
                elif "バター" in response_text:
                    update.message.reply_text("僕と一緒だ！バターを入れると一気に味が濃厚になるよね！")
                else:
                    update.message.reply_text(
                        "珍しいトッピングが好きなんだね．トッピングだけみても店によって色々あって面白いよね．"
                    )

            update.message.reply_text("最後に他の好み教えて！調味料とか，色とかなんでも大丈夫だよ！無ければ，”なし”と答えてね！")
            self.counter += 1

        # その他 ＆ レコメンド
        elif self.counter == 4:
            response_text = update.message.text
            if response_text != "なし":
                self.answer.extend(exract_words.search_corpus(response_text))

            print(f"モデルにある単語{self.answer}")
            update.message.reply_text("今まで教えてくれた情報からおすすめのラーメン屋を見つけてくるね！")

            result_ramen_stores, ranking = recommend.search_similar_stores(self.answer)
            self.ranking = ranking

            print(result_ramen_stores.loc[:, ["name", "texts_tfidf_sorted_top20"]])

            update.message.reply_text(
                self.make_recommend_message(
                    "一押しのラーメン屋はこちら！！！", result_ramen_stores.iloc[0]
                )
            )

            update.message.reply_text(
                self.make_recommend_message(
                    "おすすめのラーメン屋はこちら！！", result_ramen_stores.iloc[1]
                )
            )

            update.message.reply_text(
                self.make_recommend_message(
                    "こんなラーメン屋はどうかな？", result_ramen_stores.iloc[2]
                )
            )
            update.message.reply_text("行きやすいお店なかったりする？なければ行きやすい地区教えて！これで良ければ“以上”と入力してね")
            self.counter += 1

        # 地区
        elif self.counter == 5:
            user_area = update.message.text
            new_ranking = recommend.search_area(user_area, self.ranking)

            # 正しいarea名を受け取るまで聞き返す
            while new_ranking.empty and user_area != "以上":
                update.message.reply_text("そんな区市町村知らない。")
                user_area = update.message.text
                new_ranking = recommend.search_area(user_area, self.ranking)

            if user_area != "以上":
                update.message.reply_text(
                    self.make_recommend_message(
                        f"{user_area}のおすすめはこちら！", new_ranking.iloc[0]
                    )
                )

            update.message.reply_text("君とのお話とっても楽しかったよ！\nまたラーメンについて知りたくなったらお話ししよう！")

    def make_recommend_message(self, message, store):
        recommend_message = message + "\n"
        recommend_message += store["url"]
        return recommend_message

    # telegramの動作コマンド
    def run(self):
        updater = Updater(TOKEN)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start))

        dp.add_handler(MessageHandler(Filters.text, self.message))

        updater.start_polling()

        updater.idle()


if __name__ == "__main__":
    mybot = RamenBot()
    mybot.run()
