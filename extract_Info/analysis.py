from .stopwords import *
from .stopwords import text_stopwords as text_stop_words

import re
import urllib.request
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import os.path as path


class Analysis():
    def __init__(self, debug=False):

        self.articles_url = {
            'https://www.freemalaysiatoday.com/category/world/2020/05/15/asias-traffic-makes-roaring-return-to-streets-as-lockdowns-end/',
            'http://english.astroawani.com/technology-news/will-carpooling-culture-catch-malaysia-227482',
            'https://en.antaranews.com/news/122433/using-mrt-to-go-around-kuala-lumpur'
        }

        self.url_count = 0

        self.debug = debug

    def run_analysis(self):

        for num in range(1, 1 + 1):
            file = path.dirname(__file__) + f'/articles/article{num}.txt'

            self.stopword = []
            self.freq = []
            self.word = []
            self.article_len = 0
            self.pos = 0
            self.neg = 0
            self.neutral = 0
            self.url_count += 1
            # request the article

            text = ""
            with open(file, 'r') as f:
                text = f.read()

            self.words_frequency(text)
            self.freq_graph()

            self.article_len = len(text)
            self.article_sentiment(text)
            self.senti_graph()

            with open(path.dirname(__file__) + '/articles/article{}.txt'.format(self.url_count), 'w', encoding='utf-8') as article:
                for t in text:
                    article.write(t)

    # count article's words frequency
    def words_frequency(self, text):
        file = open(path.dirname(__file__) + "/articles/stopwords", encoding='utf-8')
        stopwords = file.read().lower().split()

        # remove stopwords in the article
        wordList = stripNonAlphaNum(text)
        text_stopwords = text_stop_words(text, stopwords)
        fullwordList = remove(wordList, text_stopwords)
        dictionary = wordListToFreqDict(fullwordList)
        sorteddict = sortFreqDict(dictionary)

        for t in sorteddict:
            self.freq.append(t[0])

        for i in sorteddict:
            self.word.append(i[1])

        print('The article {} :\n\t\tfrequency:{}\n'.format(self.url_count, sorteddict))

    # draw the frequency graph
    def freq_graph(self):
        if self.debug:
            fig = go.Figure(data=go.Bar(x=self.word, y=self.freq, width=5))
            fig.write_html(path.dirname(__file__) + '/article_graph/freqFigure{}.html'.format(self.url_count), auto_open=True)

    # count article's positive , negative words and neutral words
    def article_sentiment(self, text):
        File = open(path.dirname(__file__) + '/articles/negative_words', encoding='utf-8')
        negativeFile = File.read().lower()
        negativeText = re.sub('[,-]', '', negativeFile).split()

        File = open(path.dirname(__file__) + '/articles/positive_words', encoding='utf-8')
        positiveFile = File.read().lower()
        positiveText = re.sub('[,-]', '', positiveFile).split()

        for n in negativeText:
            result = Boyer_Moore_Matcher(text, n)
            self.pos += len(result)

        for p in positiveText:
            result = Boyer_Moore_Matcher(text, p)
            self.neg += len(result)

        self.neutral = self.article_len - (self.pos + self.neg)
        if self.debug:
            print(
                '\t\tConclusion: The article {} has total {} words ,which {} positive words , {} negative words, and {} neutral words.\n\t\t\t\t\tTherefore, this article is giving {} sentiment ,and this public transportation has {} sentiment.\n'.format(
                    self.url_count, self.article_len, self.pos, self.neg, self.neutral,
                    'positive' if self.pos > self.neg else 'negative',
                    'positive' if self.pos > self.neg else 'negative'))

    # draw the positive ,neutral and negative words graph
    def senti_graph(self):
        if self.debug:
            x = ["Positive words", "Neutral words", "Negative words"]
            colors = ['red', 'blue', 'lightslategray']
            fig = go.Figure([go.Bar(x=x, y=[self.pos, self.neutral, self.neg], marker_color=colors)])
            fig.update_layout(title_text='positive/negative sentiment graph')
            fig.write_html(path.dirname(__file__) + '/article_graph/sentiFigure{}.html'.format(self.url_count), auto_open=True)


if __name__ == '__main__':
    analysis = Analysis(debug=True)
    analysis.run_analysis()
