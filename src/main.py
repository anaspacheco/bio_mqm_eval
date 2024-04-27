#  main
import os
from logging import Logger
from tqdm.auto import tqdm
import utils.api_utils as api 
from translation import google_translate, deepl_translate, gpt4_translate
from evaluation import * 

SRC_LANGUAGE_CODES = {
    "1":"en",
    "2":"pt",
    "3":"de",
    "4": "es", 
    "5": "fr",
    "6": "zh",
    "7": "ru",
}

TRG_LANGUAGE_CODES = {
    "1":"en-us",
    "2":"pt-br",
    "3":"de",
    "4": "es", 
    "5": "fr",
    "6": "zh",
    "7": "ru",
}

source = None
target = None

try:
    api.test_all_auth()
    print("APIs Authenthicated.")
except Exception as e:
    Logger.error("One or more APIs failed: ", e)

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = [line.strip() for line in data]
    return data

def generate_prediction_file(filename, pm_ids, lines, sentences):
    with open(filename, 'w') as f:
        for i in range(len(pm_ids)):
            f.write(f"{pm_ids[i]}\t{sentences[i]}\n")

def process_sentences(data, src, trg, model):
    sentences = []
    pm_ids = []
    lines = []
    with tqdm(total=len(lines), desc="\033[92mTranslating sentences\033[0m") as pbar:  # Progress bar for sentences
        for line in data:
            items = line.split('\t')
            pm_ids.append(items[0])
            lines.append(items[1])
            sentence = items[1]
            if model == 'gpt-4':
                translated_sentence = gpt4_translate(src, trg, sentence)
            elif model == 'google-translate':
                translated_sentence = google_translate(src, trg, sentence)
            elif model == 'deepl':
                translated_sentence = deepl_translate(src, trg, sentence)
            sentences.append(translated_sentence)
            pbar.update(1)
    return pm_ids, lines, sentences

def handle_translation(data, model, src, trg):
    pmids, lines, sentences = process_sentences(data, src, trg, model)
    output_filename = f"prediction_{model}_{source}2{target}.txt" 
    generate_prediction_file(os.path.join('../result_files/'+model, output_filename), pmids, lines, sentences)
    print(f"Prediction file generated: {output_filename}")

def handle_evaluation(model, src, trg):
    appendix = f"{SRC_LANGUAGE_CODES.get(src)}2{SRC_LANGUAGE_CODES.get(trg)}"
    reference_file = os.path.join('../prl_data/', f"{SRC_LANGUAGE_CODES.get(src)}2{SRC_LANGUAGE_CODES.get(trg)}", f"{SRC_LANGUAGE_CODES.get(trg)}.txt")
    if model == "deepl":
        test_file = os.path.join('../result_files/deepl/', f"prediction_deepl_{appendix}.txt")
    elif model == "gpt-4":
        test_file = os.path.join('../result_files/gpt-4', f"prediction_gpt-4_{appendix}.txt")
    elif model == "google-translate":
        test_file = os.path.join('../result_files/google-translate', f"prediction_google-translate_{appendix}.txt")
    refs, pred = detokenize(reference_file, test_file, SRC_LANGUAGE_CODES.get(trg))
    calculate_bleu(refs, pred, model, SRC_LANGUAGE_CODES.get(src), SRC_LANGUAGE_CODES.get(trg))
    calculate_chrf(refs, pred, model, SRC_LANGUAGE_CODES.get(src), SRC_LANGUAGE_CODES.get(trg))
    calculate_ter(refs, pred, model, SRC_LANGUAGE_CODES.get(src), SRC_LANGUAGE_CODES.get(trg))
    print(f"Evaluation complete.") 
    pass

def main():
    task = input("Choose a task:\n(1)translate\t\t(2)evaluate\n> ")
    model = input("Choose translation model: \n(1)gpt-4\t\t(2)google-translate\t\t(3)deepl\n> ").lower()
    if model not in ("1","2","3"):
        raise ValueError("Invalid translation model")
    TRANSLATION_MODELS = {
        "1":"gpt-4",
        "2":"google-translate",
        "3":"deepl",
    }
    model = TRANSLATION_MODELS.get(model)
    src = input("Choose source language:\n(1)english\n(2)portuguese\n(3)german\n(4)spanish\n(5)french\n(6)chinese\n(7)russian\n>").lower()
    if src not in SRC_LANGUAGE_CODES:
        raise ValueError("Invalid source language.")
    trg = input("Choose target language:\n(1)english\n(2)portuguese\n(3)german\n(4)spanish\n(5)french\n(6)chinese\n(7)russian\n>").lower()
    if trg not in TRG_LANGUAGE_CODES:
        raise ValueError("Invalid target language.")
    elif src == trg:
        raise ValueError("Source and target languages must be different.")
    elif src != "1":
        if trg != "1":
            raise ValueError("One of the languages must be English.")
    if task == "2":
        handle_evaluation(model, src, trg)
    elif task == "1":
        global source, target 
        if src != "1":
            file_name = os.path.join('../prl_data/', f"{SRC_LANGUAGE_CODES.get(src)}2en", f"{SRC_LANGUAGE_CODES.get(trg)}.txt")
        else:
            file_name = os.path.join('../prl_data/', f"en2{SRC_LANGUAGE_CODES.get(trg)}", f"{SRC_LANGUAGE_CODES.get(trg)}.txt")
        data = load_data(file_name)
        source = SRC_LANGUAGE_CODES.get(src)
        target = SRC_LANGUAGE_CODES.get(trg)
        if model == "deepl" or model == "gpt-4":
            src = SRC_LANGUAGE_CODES.get(src).upper() 
            trg = TRG_LANGUAGE_CODES.get(trg).upper()
        elif model == "google-translate":
            src = SRC_LANGUAGE_CODES.get(src)
            trg = TRG_LANGUAGE_CODES.get(trg)
        handle_translation(data, model, src, trg)    
    else:
        raise ValueError("Enter valid task name. 1 for translation, 2 for evaluation.")
    
if __name__ == "__main__":
    main()
