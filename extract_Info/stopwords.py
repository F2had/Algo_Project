
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

def badCharHeuristic(string, size):
    '''
    The preprocessing function for
    Boyer Moore's bad character heuristic
    '''

    # Initialize all occurrence as -1
    badChar = [-1] * 0xFFFF

    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i

        # retun initialized list
    return badChar

def Boyer_Moore_Matcher(text, pattern):
        '''
        A pattern searching function that uses Bad Character
        Heuristic of Boyer Moore Algorithm
        '''
        m = len(pattern)
        n = len(text)

        # create the bad character list by calling
        # the preprocessing function badCharHeuristic()
        # for given pattern
        badChar = badCharHeuristic(pattern, m)

        # s is shift of the pattern with respect to text
        s = 0
        result = []
        while (s <= n - m):
            j = m - 1

            # Keep reducing index j of pattern while
            # characters of pattern and text are matching
            # at this shift s
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1

            # If the pattern is present at current shift,
            # then index j will become -1 after the above loop
            if j < 0:
                result.append(s)

                '''     
                    Shift the pattern so that the next character in text 
                          aligns with the last occurrence of it in pattern. 
                    The condition s+m < n is necessary for the case when 
                       pattern occurs at the end of text 
                   '''
                chara = ord(text[s + j])
                # if chara > 256:
                #     chara = 0
                s += (m - badChar[chara] if s + m < n else 1)
            else:
                ''' 
                   Shift the pattern so that the bad character in text 
                   aligns with the last occurrence of it in pattern. The 
                   max function is used to make sure that we get a positive 
                   shift. We may get a negative shift if the last occurrence 
                   of bad character in pattern is on the right side of the 
                   current character. 
                '''
                chara = ord(text[s + j])
                # if chara > 256:
                #     chara = 0
                s += max(1, j - badChar[chara])

        return result


def text_stopwords(text,stopwords):
    text_stopwords=[]
    for st in stopwords:
        result=Boyer_Moore_Matcher(text, st)
        if len(result)!=0:
            text_stopwords.append(text[result[0]:result[0] + len(st)])


    return text_stopwords


def remove(wordlist, text_stopwords):
    return [w for w in wordlist if w not in text_stopwords]



