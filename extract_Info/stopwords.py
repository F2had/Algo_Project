
# Given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric).

def stripNonAlphaNum(text):
    import re
    text=re.findall('[a-zA-Z]+',text)
    return text


def wordListToFreqDict(wordlist):
    wordfreq = dict((p,wordlist.count(p))for p in set(wordlist))
    return wordfreq

def sortFreqDict(freqdic):
    aux=[(freqdic[key],key) for key in freqdic]
    aux.sort()
    aux.reverse()
    return aux


def Rabin_Karp_Matcher(text, pattern, d, q):
        n = len(text)
        m = len(pattern)
        h = pow(d, m - 1) % q
        p = 0
        t = 0
        result = []
        for i in range(m):
            p = (d * p + ord(pattern[i])) % q
            t = (d * t + ord(text[i])) % q

        for s in range(n - m + 1):
            if p == t:
                match = True
                for i in range(m):
                    if pattern[i] != text[s + i]:
                        match = False
                        break
                if match:
                    result = result + [s]
            if s < n - m:
                t = (t - h * ord(text[s])) % q  # remove letter s
                t = (t * d + ord(text[s + m])) % q  # add letter s+m
                t = (t + q) % q  # make sure that t >= 0
        return result


def text_stopwords(text,stopwords):
    text_stopwords=[]
    for st in stopwords:
        result=Rabin_Karp_Matcher(text,st,256,101)
        if len(result)!=0:
            text_stopwords.append(text[result[0]:result[0] + len(st)])


    return text_stopwords


def remove(wordlist, text_stopwords):
    return [w for w in wordlist if w not in text_stopwords]



