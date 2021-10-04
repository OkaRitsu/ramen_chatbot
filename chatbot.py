#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import exract_words
import recommend
import telegram_token

# telegram_token.pyファイルに以下を書き込む
# TOKEN = "XXXXXXXXXXXXXXXXXX"
TOKEN = telegram_token.TOKEN

# 以下の部分を各自書き換えれば自分のシステムができる
# ctrl-cで強制終了

class SampleBot:
    def __init__(self):
        self.counter = 0
        self.answer = ""
        pass


    def start(self, bot, update):
        #update.message.reply_text()内にテキストを入れるとtelegramに送信
        update.message.reply_text('こんにちは。ラーメンマイスターだよ')
        update.message.reply_text('はじめに，君のことについて教えて！')
        update.message.reply_text('ラーメン以外の好きな食べ物は何？無ければ，”なし”と答えてね！')

    def message(self, bot, update):
        print('カウンター：', self.counter)

        # 
        if self.counter == 0:
            #update.message.textでtelegramのユーザーからの入力を取得
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}っておいしいよね")
            update.message.reply_text("趣味は何かあるかな？無ければ，”なし”と答えてね！")
            self.counter += 1

        elif self.counter == 1:
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}いいね！")
            update.message.reply_text("次にラーメンのことについて教えて！")
            update.message.reply_text("何ラーメンが好き？僕は味噌ラーメンが好き")
            self.counter += 1
        
        # 好きな食べ物
        elif self.counter == 2:
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}いいね！")
            update.message.reply_text("好きなトッピングはある？僕は，コーンとバターが好き！")
            self.counter += 1
        
        elif self.counter == 3:
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}いいね！")
            update.message.reply_text("麺の太さの好みは？僕は太麺がいいなー")
            self.counter += 1

        elif self.counter == 4:
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}いいね！")
            update.message.reply_text("最後に他の好み教えて！調味料とか，色とかなんでも大丈夫だよ！無ければ，”なし”と答えてね！")
            self.counter += 1

        # 言語処理への興味
        elif self.counter == 5:
            self.counter = 0
            response_text = update.message.text
            if response_text != "なし":
                self.answer += response_text + ' '
                update.message.reply_text(f"{response_text}いいね！")
            update.message.reply_text("今まで教えてくれた情報からおすすめのラーメン屋を見つけてくるから，ちょっと待っててね")

            response_words = exract_words.search_corpus(self.answer)
            print(response_words)
            result_ramen_stores = recommend.search_similar_stores(response_words)
            print(result_ramen_stores)
            update.message.reply_text(result_ramen_stores.loc[0]['url'])
            update.message.reply_text('．．．システム停止')
        

#telegramの動作コマンド（変えなくても動くはず）
    def run(self):
        updater = Updater(TOKEN)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", self.start))

        dp.add_handler(MessageHandler(Filters.text, self.message))

        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    mybot = SampleBot()
    mybot.run()
