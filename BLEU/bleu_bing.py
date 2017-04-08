from __future__ import division

import math
import re
from translation import bing
from nltk import word_tokenize
from nltk.compat import Counter
from google.cloud import translate
from nltk.util import ngrams


class BLEU(object):
    @staticmethod
    def compute(candidate, references, weights):
        candidate = [c.lower() for c in candidate]
        references = [[r.lower() for r in reference] for reference in references]

        p_ns = (BLEU.modified_precision(candidate, references, i) for i, _ in enumerate(weights, start=1))
        s = math.fsum(w * math.log(p_n) for w, p_n in zip(weights, p_ns) if p_n)

        bp = BLEU.penalty(candidate, references)
        return bp * math.exp(s)

    @staticmethod
    def modified_precision(candidate, references, n):
        counts = Counter(ngrams(candidate, n))

        if not counts:
            return 0

        max_counts = {}
        for reference in references:
            reference_counts = Counter(ngrams(reference, n))
            for ngram in counts:
                max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

        clipped_counts = dict((ngram, min(count, max_counts[ngram])) for ngram, count in counts.items())

        return sum(clipped_counts.values()) / sum(counts.values())

    @staticmethod
    def penalty(candidate, references):
        c = len(candidate)
        r = min(abs(len(r) - c) for r in references)

        if c > r:
            return 1
        else:
            return math.exp(1 - r / c)


if __name__ == "__main__":
    # candidate1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which','ensures', 'that', 'the', 'military', 'always', 'obeys', 'the', 'commands', 'of', 'the', 'party']
    # reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that','ensures', 'that', 'the', 'military', 'will', 'forever','heed', 'Party', 'commands']
    #
    # print (BLEU.modified_precision(candidate1, [reference1], 1))

    with open("1_en.txt", "r", encoding="utf8") as file:
        for line in file:
            if line:
                line = line.rstrip()
                line = line.lower()
                line = re.sub("[^'$A-z\d ]", '', line)
                # print(line)
                subtitles = line.split('$')
                length = len(subtitles[1])
                candidate=[]
                i=0
                for sub in subtitles[1:length]:
                    main = []
                    word = sub.split()
                    for w in word:
                        main.append(w)
                    candidate.append(main)
                cand_length=len(candidate)

    with open("1_es.txt", "r", encoding="utf8") as file1:
        for line1 in file1:
            if line1:
                line1 = line1.rstrip()
                line1 = line1.lower()
                line1 = re.sub("[^'$A-z\d ]", '', line1)
                # print(line)
                subtitles1 = line1.split('$')
                length1=len(subtitles1)
                reference=[]
                target = 'en'
                for sub1 in subtitles1[1:length1]:
                    word1=sub1.split()
                    english = []
                    for word in word1:
                        english.append(bing(word, dst='en'))
                    reference.append(english)
    score=[]
    for (cand,ref) in zip(candidate,reference):
        score.append(BLEU.modified_precision(cand,ref,1))
    bleu=sum(score) / float(len(score))
    print(bleu)
