"""
For homework this week, please find the 200th most common word in the book "Alice's Adventures in Wonderland",
available as a text file here: https://drive.google.com/file/d/1u61M5V_Wp7uJW2foLthuqO9arTmNZ9sK/view?usp=sharing
Be sure to strip out all whitespace and punctuation, and convert everything to lower case before beginning.
Choose whichever language you'd like to implement your solution, but I would recommend python.
"""
import string, re
from operator import itemgetter

text_obj = open("alice_in_wonderland.txt", "r")

# Prep text to perform counting
# THERE HAS TO BE A BETTER WAY IN REGEX, BUT I GOT ANNOYED
text = text_obj.read()
text = text.replace('--', ' ').replace('-', ' ').lower().replace('\n', ' ').replace('\ufeff', '').replace("'", '')

# Remove multiple spaces
text = re.sub('\s+', ' ', text)

# Split string into list of words
text_list = text.split(' ')

# Strip punctuation at beginning and end of each word
for i, word in enumerate(text_list):
    text_list[i] = word.strip(string.punctuation)

# Remove blanks that are still there for some reason
text_list = list(filter(None, text_list))

# Make set of words and initialize list of lists
word_set = set(text_list)
word_count = []

for word in word_set:
    word_count.append(tuple((word, text_list.count(word))))

word_count = sorted(word_count, key=itemgetter(1), reverse=True)
print(word_count)
count_200 = word_count[199][1]

for (x, y) in word_count:
    if y == count_200:
        print(x)


# print(text.lower())

text_obj.close()

