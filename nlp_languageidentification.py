# -*- coding: utf-8 -*-
"""NLP_LanguageIdentification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NrilCHrTe6R61Vzg9QJTTNSHdE50iwnY

# **Training** **of** **Data**
"""

pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

pip install inltk

pip install polyglot

pip install pycld2

pip install PyICU

class LanguageCodes:
    bengali = 'bn'   
    hindi = 'hi'
    panjabi = 'pa'
    sanskrit = 'sa'
    tamil = 'ta' 

    def get_all_language_codes(self):
        return [self.bengali,  self.hindi,self.panjabi,
                self.sanskrit, self.tamil]


class LMConfigs:
    all_language_codes = LanguageCodes()
    lm_model_file_url = {
        all_language_codes.bengali: 'https://www.dropbox.com/s/4berhstpw836kcw/export.pkl?raw=1',      
        all_language_codes.hindi: 'https://www.dropbox.com/s/sakocwz413eyzt6/export.pkl?raw=1',
        all_language_codes.panjabi: 'https://www.dropbox.com/s/ejiv5pdsi2mhhxa/export.pkl?raw=1',
        all_language_codes.sanskrit: 'https://www.dropbox.com/s/4ay1by5ryz6k39l/sanskrit_export.pkl?raw=1',
        all_language_codes.tamil: 'https://www.dropbox.com/s/88klv70zl82u39b/export.pkl?raw=1',
    }
    tokenizer_model_file_url = {
        all_language_codes.bengali: 'https://www.dropbox.com/s/29h7vqme1kb8pmw/bengali_lm.model?raw=1',
        
        all_language_codes.hindi: 'https://www.dropbox.com/s/xrsjt8zbhwo7zxq/hindi_lm.model?raw=1',
        all_language_codes.panjabi: 'https://www.dropbox.com/s/jxwr9ytn0zfzulc/panjabi_lm.model?raw=1',
        all_language_codes.sanskrit: 'https://www.dropbox.com/s/e13401nsekulq17/tokenizer.model?raw=1',
        all_language_codes.tamil: 'https://www.dropbox.com/s/jpg4kaqyfb71g1v/tokenizer.model?raw=1',
        
    }

    def __init__(self, language_code: str):
        self.language_code = language_code

    def get_config(self):
        return {
            'lm_model_url': self.lm_model_file_url[self.language_code],
            'lm_model_file_name': 'export.pkl',
            'tokenizer_model_url': self.tokenizer_model_file_url[self.language_code],
            'tokenizer_model_file_name': 'tokenizer.model'
        }


class AllLanguageConfig(object):

    @staticmethod
    def get_config():
        return {
            'all_languages_identifying_model_name': 'export.pkl',
            'all_languages_identifying_model_url': 'https://www.dropbox.com/s/a06fa0zlr7bfif0/export.pkl?raw=1',
            'all_languages_identifying_tokenizer_name': 'tokenizer.model',
            'all_languages_identifying_tokenizer_url':
                'https://www.dropbox.com/s/t4mypdd8aproj88/all_language.model?raw=1'
        }

from fastai.text import *
import sentencepiece as spm

class LanguageTokenizer(BaseTokenizer):
    def __init__(self, lang: str):
        self.lang = lang
        self.sp = spm.SentencePieceProcessor()
        model_path = path/f'models/{lang}/tokenizer.model'
        self.sp.Load(str(model_path))

    def tokenizer(self, t: str) -> List[str]:
        return self.sp.EncodeAsPieces(t)


    def remove_foreign_tokens(self, t: str):
        local_pieces = []
        for i in self.sp.EncodeAsIds(t):
            local_pieces.append(self.sp.IdToPiece(i))
        return local_pieces



class SanskritTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)


class BengaliTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)


class HindiTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)


class PanjabiTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)


class TamilTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)

pip install aiohttp

from pathlib import Path

import aiohttp as aiohttp
import os

all_language_codes = LanguageCodes()

async def setup_language(language_code: str):
    lmconfig = LMConfigs(language_code)
    config = lmconfig.get_config()
    await download_file(config['lm_model_url'], path/'models'/f'{language_code}', config["lm_model_file_name"])
    await download_file(config['tokenizer_model_url'], path/'models'/f'{language_code}',
                        config["tokenizer_model_file_name"])
    print('Done!')
    return True


def verify_language(language_code: str):
    lmconfig = LMConfigs(language_code)
    config = lmconfig.get_config()
    if (path/'models'/f'{language_code}'/f'{config["lm_model_file_name"]}').exists() and \
            (path/'models'/f'{language_code}'/f'{config["tokenizer_model_file_name"]}').exists():
        return True
    else:
        return False

import asyncio
from fastai.text import *
from inltk.tokenizer import LanguageTokenizer


lcodes = LanguageCodes()
all_language_codes = lcodes.get_all_language_codes()


async def download(language_code: str):
    if language_code not in all_language_codes:
        raise Exception(f'Language code should be one of {all_language_codes} and not {language_code}')
    learn = await setup_language(language_code)
    return learn


def setup(language_code: str):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(download(language_code))]
    learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
    loop.close()


def check_input_language(language_code: str):
    if language_code not in all_language_codes:
        raise Exception(f'Language code should be one of {all_language_codes} and not {language_code}')
    if not verify_language(language_code):
        raise Exception(f'You need to do setup for the **first time** for language of your choice so that '
                        f'we can download models. So, '
                        f'Please run setup({language_code}) first!')



def tokenize(input: str, language_code: str):
    check_input_language(language_code)
    tok = LanguageTokenizer(language_code)
    output = tok.tokenizer(input)
    return output


def identify_language(input: str):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(check_all_languages_identifying_model())]
    done = loop.run_until_complete(asyncio.gather(*tasks))[0]
    loop.close()
    defaults.device = torch.device('cpu')
    path = Path(__file__).parent
    learn = load_learner(path / 'models' / 'all')
    output = learn.predict(input)
    return str(output[0],output[1])


def remove_foreign_languages(input: str, host_language_code: str):
    check_input_language(host_language_code)
    tok = LanguageTokenizer(host_language_code)
    output = tok.remove_foreign_tokens(input)
    return output

f = open('./text.txt', 'r')
file_contents = f.read()
print (file_contents)

f = open('./tamil.txt', 'r')
file_contents1 = f.read()
print (file_contents1)

from inltk.inltk import setup
from inltk.inltk import identify_language
from inltk.inltk import identify_language, reset_language_identifying_models
from inltk.inltk import predict_next_words
from inltk.inltk import remove_foreign_languages
from inltk.inltk import get_sentence_encoding
from inltk.inltk import get_similar_sentences
from inltk.inltk import get_sentence_similarity
setup('hi')
setup('bn')
setup('pa')
setup('sa')

"""# **Monolingual** **language** **identification**"""

identify_language(file_contents)

identify_language(file_contents1)

identify_language("আবহাওয়া চমৎকার")

identify_language("ਤੁਸੀ ਕਿਵੇਂ ਹੋ")

identify_language("भवान् संस्कृतं भाषते वा ")

"""# **Applications**

# **Remove Foreign Language**
"""

remove_foreign_languages(file_contents, 'hi')

"""# **Multilingual Language Identification**"""

import polyglot
from polyglot.utils import pretty_list
import pycld2 as cld2

mixed_text=("எப்படி இருக்கிறீர்கள்  আপনি কেমন আছেন आप कैसे हैं")



isReliable, textBytesFound, details, vectors = cld2.detect(
    mixed_text, returnVectors=True
)
print(details)