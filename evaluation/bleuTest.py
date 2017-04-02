from __future__ import division

import math

from nltk import word_tokenize
from nltk.compat import Counter
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
    candidate1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which','ensures', 'that', 'the', 'military', 'always', 'obeys', 'the', 'commands', 'of', 'the', 'party']
    reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that','ensures', 'that', 'the', 'military', 'will', 'forever','heed', 'Party', 'commands']

    print (BLEU.modified_precision(candidate1, [reference1], 1))
