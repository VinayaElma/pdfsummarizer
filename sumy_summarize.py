from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from pdftotext import pdf_text, text_file

LANGUAGE = "english"
SENTENCES_COUNT = 10


if __name__ == "__main__":
    text = pdf_text()
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    final=""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        text = str(sentence)
        text = text.replace('\n', ' ')
        text = text.replace('\r', '')
        text = re.sub(r'[^\x00-\x7f]',r' ',text)
        text = re.sub(r'\s+',r" ",text)
        final += text
    print(final)
    text_file(final)
    