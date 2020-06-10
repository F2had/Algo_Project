import stopwords as st

import re
import urllib.request
from bs4 import BeautifulSoup
import plotly.graph_objects as go


class Analysis():
    def __init__(self):

        self.articles_url = {
            'https://www.freemalaysiatoday.com/category/world/2020/05/15/asias-traffic-makes-roaring-return-to-streets-as-lockdowns-end/',
            'http://english.astroawani.com/technology-news/will-carpooling-culture-catch-malaysia-227482',
            'https://en.antaranews.com/news/122433/using-mrt-to-go-around-kuala-lumpur'
        }

        self.url_count =0



    def main(self):

        for url in self.articles_url:
            self.stopword = []
            self.freq = []
            self.word = []
            self.article_len = 0
            self.pos = 0
            self.neg = 0
            self.neutral = 0
            self.url_count+=1
            # request the article
            response = urllib.request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, features='lxml')
            text = soup.get_text(strip=True)

            self.words_frequency(text)
            self.freq_graph()

            self.article_len = len(text)
            self.article_sentiment(text)
            self.senti_graph()

            with open('articles/article{}.txt'.format(self.url_count), 'w', encoding='utf-8') as article:
                for t in text:
                    article.write(t)


    # count article's words frequency
    def words_frequency(self,text):
        file = open("articles/stopwords", encoding='utf-8')
        stopwords = file.read().lower().split()

        # remove stopwords in the article
        wordList= st.stripNonAlphaNum(text)
        text_stopwords=st.text_stopwords(text,stopwords)
        fullwordList=st.remove(wordList,text_stopwords)
        dictionary = st.wordListToFreqDict(fullwordList)
        sorteddict = st.sortFreqDict(dictionary)


        for t in sorteddict:
            self.freq.append(t[0])

        for i in sorteddict:
            self.word.append(i[1])

        print('The article {} :\n\t\tfrequency:{}\n'.format(self.url_count,sorteddict))


    # draw the frequency graph
    def freq_graph(self):
        fig = go.Figure(data=go.Bar(x=self.word, y=self.freq, width=5))
        fig.write_html('article_graph/freqFigure{}.html'.format(self.url_count), auto_open=True)


    # count article's positive , negative words and neutral words
    def article_sentiment(self,text):
        File = open('articles/negative_words', encoding='utf-8')
        negativeFile = File.read().lower()
        negativeText = re.sub('[,-]', '', negativeFile).split()

        File = open('articles/positive_words', encoding='utf-8')
        positiveFile = File.read().lower()
        positiveText = re.sub('[,-]', '', positiveFile).split()

        for n in negativeText:
            result = st.Rabin_Karp_Matcher(text, n, 256, 101)
            self.pos += len(result)

        for p in positiveText:
            result = st.Rabin_Karp_Matcher(text, p, 256, 101)
            self.neg += len(result)

        self.neutral = self.article_len - (self.pos + self.neg)
        print('\t\tConclusion: The article {} has total {} words ,which {} positive words , {} negative words, and {} neutral words.\n\t\t\t\t\tTherefore, this article is giving {} sentiment ,and this public transportation has {} sentiment.\n'.format(self.url_count,self.article_len, self.pos, self.neg,self.neutral,'positive' if self.pos>self.neg else 'negative','positive' if self.pos>self.neg else 'negative'))



    #draw the positive ,neutral and negative words graph
    def senti_graph(self):
        x = ["Positive words", "Neutral words", "Negative words"]
        colors = ['red','blue','lightslategray']
        fig = go.Figure([go.Bar(x=x, y=[self.pos, self.neutral, self.neg], marker_color=colors)])
        fig.update_layout(title_text='positive/negative sentiment graph')
        fig.write_html('article_graph/sentiFigure{}.html'.format(self.url_count), auto_open=True)



if __name__ == '__main__':
    analysis=Analysis()
    analysis.main()


