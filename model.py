# --- Required Libraries ---
import pandas as pd
from googletrans import Translator  # Backup translator if needed (not used in final translation here)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # Hugging Face model and tokenizer
import torch  # For tensor operations
from nltk.translate.bleu_score import sentence_bleu  # For BLEU score calculation
import math  # For perplexity calculation

# --- Translation Model Wrapper ---
class TranslationModel:
    def __init__(self):
        # Optional: Google Translate backup
        self.translator = Translator()

        # Load multilingual model from Hugging Face (M2M100)
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/m2m100_418M")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/m2m100_418M")

    def translate(self, text: str) -> str:
        """
        Translate English text to French using the M2M100 model.
        """
        self.tokenizer.src_lang = "en"  # Source language
        encoded = self.tokenizer(text, return_tensors="pt")  # Tokenize input
        generated = self.model.generate(
            **encoded, 
            forced_bos_token_id=self.tokenizer.get_lang_id("fr")  # Force French as target
        )
        return self.tokenizer.decode(generated[0], skip_special_tokens=True)

    def compute_bleu(self, source: str, predicted: str) -> float:
        """
        Compute BLEU score between source and predicted translations.
        """
        reference = [source.split()]  # Tokenized reference
        hypothesis = predicted.split()  # Tokenized prediction
        return sentence_bleu(reference, hypothesis)

    def compute_perplexity(self, sentence: str) -> float:
        """
        Compute perplexity of a given sentence.
        Lower is better (less surprise).
        """
        input_ids = self.tokenizer(sentence, return_tensors="pt").input_ids
        with torch.no_grad():
            outputs = self.model(input_ids, labels=input_ids)
            loss = outputs.loss
        return math.exp(loss.item())  # Perplexity = exp(loss)

# --- Instantiate the Model ---
model = TranslationModel()
