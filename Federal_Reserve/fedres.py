from collections import Counter

with open('fedRes.txt') as f:
    file = f.read()
file = file.split()

wordCount = (Counter(file)).most_common()
for i in wordCount:
    print(i)

