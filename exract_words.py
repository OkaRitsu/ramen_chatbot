import pandas as pd
import MeCab

#tagger = MeCab.Tagger(" -r /etc/mecabrc -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
tagger = MeCab.Tagger("-Owakati -d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd")


def tokenize_ja(text, lower):
    node = tagger.parseToNode(str(text))
    while node:
        # 分かち書きで取得する品詞を指定
        if lower and node.feature.split(',')[0] in ["名詞", "形容詞"]:
            yield node.surface.lower()
        node = node.next


def tokenize(content, lower):
    return [
        str(token) for token in tokenize_ja(content, lower)
        if not token.startswith('_')
    ]


def search_corpus(user_word):
    print(f"ユーザーワード:{user_word}")
    user_word = tokenize(user_word, True) #形態素解析
    print(f"形態素解析結果：{user_word}")

    with open("./data/word2vec.txt", "r") as f:
        corpus = f.read().split("\n")
    user_key_words = [word for word in user_word if word in corpus] 

    # print(f"コーパスの単語数：{len(corpus)}")
    return user_key_words
