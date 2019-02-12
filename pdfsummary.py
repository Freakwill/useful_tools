#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Summarize pdf

Extract summary of text in pdf.
"""

import logging
logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def parse(fo):
    praser = PDFParser(fo)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = []
        for page in doc.get_pages(): # get page list
            interpreter.process_page(page)
   
            layout = device.get_result()
   
            p = ''.join(x.get_text() for x in layout if isinstance(x, LTTextBoxHorizontal))
            pages.append(p)
    return pages


LANGUAGE = "english"

def summarize(path, n=10):
    
    with open(path, 'rb') as fo:
        s = ''.join(parse(fo))
    parser = PlaintextParser.from_string(s, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    return summarizer(parser.document, n)

def show_summary(path, n=10):
    print('Summary of %s' % path)
    for k, sentence in enumerate(summarize(path, n), 1):
        print(k, sentence)

