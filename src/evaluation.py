import sacrebleu
from sacremoses import MosesDetokenizer
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
    with open(f"../evaluation_files/{mt}/bleu_{src}2{trg}.txt", "w+") as output:
        for ref, pred in zip(refs, preds):
            '''print(f"Reference: {ref}")
            print(f"Prediction: {pred}")'''
            bleu = sacrebleu.sentence_bleu(pred, [ref], smooth_method='exp')
            output.write(f"{bleu.score}\n")
        print(f"BLEU Scores for each sentence generated in bleu_{src}2{trg}.txt")
        blue_score = calculate_bleu_corpus(refs, preds)
        output.write(f"BLEU Score for corpus: {blue_score}\n")

def calculate_bleu_corpus(refs, preds):
    bleu = sacrebleu.corpus_bleu(preds, [refs])
    print(f"BLEU Score for corpus: {bleu.score}")
    return bleu.score
    



