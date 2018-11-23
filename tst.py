from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    a_list = a.split("\n")
    b_list = b.split("\n")
    matched = []

    for aline in a_list:
        for bline in b_list:
            if aline == bline:
                if aline not in matched:
                    matched.append(aline)

    return matched


def sentences(a, b):
    import re
    """Return sentences in both a and b"""

    a_list = re.split('. |! |\? |\n', a)
    b_list = re.split('. |! |\? |\n', b)
    matched = []

    for aline in a_list:
        for bline in b_list:
            if aline == bline:
                if aline not in matched:
                    matched.append(aline + ".")

    return matched


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    return []

text1 = """
"Goodbye," said the fox. "Here is my secret. It's quite simple: One sees clearly only with the heart. Anything essential is invisible to the eyes."
"Anything essential is invisible to the eyes," the little prince repeated, in order to remember.
"It's the time you spend on your rose that makes your rose so important."
"It's the time I spent on my rose...," the little prince repeated, in order to remember.
"People have forgotten this truth," the fox said. "But you mustn't forget it. You become responsible forever for what you've tamed. You're responsible for your rose..."
"I'm responsible for my rose...," the little prince repeated, in order to remember.

"""


text2 = """
"Goodbye," said the fox. "Here is my secret. It's quite simple: One sees clearly only with the heart. Anything essential is invisible to the eyes."
"What is essential is invisible to the eye," the little prince repeated, so that he would be sure to remember.
"It's the time you spend on your rose that makes your rose so important."
"It is the time I have wasted for my rose--" said the little prince, so that he would be sure to remember.
"People have forgotten this truth," the fox said. "But you mustn't forget it. You become responsible forever for what you've tamed. You're responsible for your rose..."
"I am responsible for my rose," the little prince repeated, so that he would be sure to remember.

"""

print(sentences(text1, text2))

