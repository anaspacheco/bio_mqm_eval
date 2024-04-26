# Core translation function taking the corpus, source/target languages, and calling appropriate API functions
from utils import api_utils as api

# ================= GPT4 TRANSLATION =================

def generate_text(prompt):
    try:
        message = {
            'role': 'user',
            'content': prompt
        }
        model_name = api.OPENAI_MODEL
        response = api.openai_client.chat.completions.create(model=model_name, messages=[message])
        #print(response)
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)


def generate_prompt(src, trg, sentence):
    return f"You are a helpful assistant specialized in biomedical translation. " \
           f"You will be provided with a sentence in {src}, and your task is to translate " \
           f"it into {trg}. Here is the sentence to translate " \
           f"(give me nothing else other than the translated sentence): {sentence}"

def gpt4_translate(src, trg, sentence):
    prompt = generate_prompt(src, trg, sentence)
    generated_text = generate_text(prompt)
    return generated_text


# ================= GOOGLE TRANSLATION =================

def google_translate(src, trg, sentence):
    response = api.google_client.translate_text(
        parent=api.PARENT,
        contents=[sentence],
        target_language_code=trg,
        source_language_code=src,
    )

    for translation in response.translations:
        return translation.translated_text
    

# ================= DEEPL TRANSLATION =================
    

def deepl_translate(src, trg, sentence):
    translator = api.translator

    result = translator.translate_text([sentence], source_lang=src, target_lang=trg)
    for translation in result: 
        return translation.text
# Core translation function taking the corpus, source/target languages, and calling appropriate API functions
from utils import api_utils as api

# ================= GPT4 TRANSLATION =================

def generate_text(prompt):
    try:
        message = {
            'role': 'user',
            'content': prompt
        }
        model_name = api.OPENAI_MODEL
        response = api.openai_client.chat.completions.create(model=model_name, messages=[message])
        #print(response)
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)


def generate_prompt(src, trg, sentence):
    return f"You are a helpful assistant specialized in biomedical translation. " \
           f"You will be provided with a sentence in {src}, and your task is to translate " \
           f"it into {trg}. Here is the sentence to translate " \
           f"(give me nothing else other than the translated sentence): {sentence}"

def gpt4_translate(src, trg, sentence):
    prompt = generate_prompt(src, trg, sentence)
    generated_text = generate_text(prompt)
    return generated_text


# ================= GOOGLE TRANSLATION =================

def google_translate(src, trg, sentence):
    response = api.google_client.translate_text(
        parent=api.PARENT,
        contents=[sentence],
        target_language_code=trg,
        source_language_code=src,
    )

    for translation in response.translations:
        return translation.translated_text
    

# ================= DEEPL TRANSLATION =================
    

def deepl_translate(src, trg, sentence):
    translator = api.translator
    result = translator.translate_text([sentence], source_lang=src, target_lang=trg)
    for translation in result: 
        return translation.text
