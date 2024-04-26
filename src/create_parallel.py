import os
import csv 

LANGUAGE_CODES = {
    "1":"en",
    "2":"pt",
    "3":"de",
    "4": "es", 
    "5": "fr",
    "6": "it",
    "7": "zh",
    "8": "ru",
}

def main():
    print("Welcome! To create the parallel corpora, please choose (1) source and (2) target languages")
    src = input("Choose source language:\n(1)english\n(2)portuguese\n(3)german\n(4)spanish\n(5)french\n(6)italian\n(7)chinese\n(8)russian\n>").lower()
    if src not in LANGUAGE_CODES:
        raise ValueError("Invalid source language.")
    trg = input("Choose target language:\n(1)english\n(2)portuguese\n(3)german\n(4)spanish\n(5)french\n(6)italian\n(7)chinese\n(8)russian\n>").lower()
    if trg not in LANGUAGE_CODES:
        raise ValueError("Invalid target language.")
    elif src == trg:
        raise ValueError("Source and target languages must be different.")
    elif src != "1":
        if trg != "1":
            raise ValueError("One of the languages must be English.")
    
    filename = f"abstract_{LANGUAGE_CODES[src]}2{LANGUAGE_CODES[trg]}.tsv"
    with open(f"../orig_data/{filename}", "r") as f:
        data = csv.reader(f, delimiter="\t")  
        next(data)
        sent_id = 0
        prev_sent = ""
        for row in data:
            if (row[8] != "Major" or "Critical") and row[2] != prev_sent:
                sent_id += 1
                src_sentence = row[2]
                trg_sentence = row[4]
                with open(f"../prl_data/{LANGUAGE_CODES[src]}2{LANGUAGE_CODES[trg]}/{LANGUAGE_CODES[src]}.txt", "a") as f:
                    f.write(str(sent_id) + "\t"+src_sentence + "\n")
                with open(f"../prl_data/{LANGUAGE_CODES[src]}2{LANGUAGE_CODES[trg]}/{LANGUAGE_CODES[trg]}.txt", "a") as f:
                    f.write(str(sent_id) + "\t"+trg_sentence + "\n")
                prev_sent = src_sentence



if __name__ == "__main__":
    main()
