import sacrebleu
import os
from sacremoses import MosesDetokenizer
from sacrebleu.metrics import BLEU, CHRF, TER
md = MosesDetokenizer(lang='en')

def detokenize(reference_file, translation_file, language):
    md = MosesDetokenizer(lang=language)
    refs = []
    with open(reference_file, 'r', encoding='utf-8') as ref_file:
        for line in ref_file:
            _, sentence = line.strip().split('\t') 
            sentence = md.detokenize(sentence.split())  
            refs.append(sentence)
    preds = []
    with open(translation_file, 'r', encoding='utf-8') as trans_file:
        for line in trans_file:
            _, sentence = line.strip().split('\t') 
            sentence = md.detokenize(sentence.split())  
            preds.append(sentence)
    return refs, preds

def calculate_bleu(refs, preds, mt, src, trg):
    directory = f"../evaluation_files/{mt}/{src}2{trg}"
    os.makedirs(directory, exist_ok=True)
    output_file = os.path.join(directory, f"bleu_{src}2{trg}.txt")
    with open(output_file, "w+") as output:
        for ref, pred in zip(refs, preds):
            bleu = sacrebleu.sentence_bleu(pred, [ref], smooth_method='exp')
            output.write(f"{bleu.score}\n")
        print(f"BLEU Scores for each sentence generated in bleu_{src}2{trg}.txt")
        bleu_score = sacrebleu.corpus_bleu(preds, [refs])
        output.write(f"BLEU Score for corpus: {bleu_score.score}\n")

def calculate_chrf(refs, preds, mt, src, trg):
    directory = f"../evaluation_files/{mt}/{src}2{trg}"
    os.makedirs(directory, exist_ok=True)
    output_file = os.path.join(directory, f"chrf_{src}2{trg}.txt")
    with open(output_file, "w+") as output:
        for ref, pred in zip(refs, preds):
            chrf = sacrebleu.sentence_chrf(pred, [ref])
            output.write(f"{chrf.score}\n")
        print(f"chrF Scores for each sentence generated in chrF_{src}2{trg}.txt")
        chrf = CHRF()
        chrf_score = chrf.corpus_score(preds, [refs])
        output.write(f"chrF Score for corpus: {chrf_score}\n")

def calculate_ter(refs, preds, mt, src, trg):
    directory = f"../evaluation_files/{mt}/{src}2{trg}"
    os.makedirs(directory, exist_ok=True)
    output_file = os.path.join(directory, f"ter_{src}2{trg}.txt")
    with open(output_file, "w+") as output:
        for ref, pred in zip(refs, preds):
            ter = sacrebleu.sentence_ter(pred, [ref])
            output.write(f"{ter.score}\n")
        print(f"TER Scores for each sentence generated in ter_{src}2{trg}.txt")
        ter = TER()
        ter_score = ter.corpus_score(preds, [refs])
        output.write(f"TER Score for corpus: {ter_score}\n")




