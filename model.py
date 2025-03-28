from googletrans import Translator  # For quick translation using Google Translate API
from nltk.translate.bleu_score import sentence_bleu  # For calculating BLEU score
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # HuggingFace tools for loading models and tokenizers
import torch  # PyTorch for handling tensors and model inference

class TranslationModel:
    def __init__(self):
        # Initialize Google Translate API for fast translation
        self.translator = Translator()
        
        # Load the tokenizer for the M2M100 multilingual translation model
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/m2m100_418M")
        
        # Load the actual translation model
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/m2m100_418M")
    
    def translate(self, text: str, src_lang: str = 'en', dest_lang: str = 'fr') -> str:
        """
        Translates a given text from the source language to the destination language
        using Google Translate API.
        """
        try:
            # Perform translation
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            print(f"Translation: {text} -> {translated.text}")  # Output the translation
            return translated.text
        except Exception as e:
            # Handle errors (e.g., internet issues, API limits)
            print(f"Translation Error: {str(e)}")
            return f"Error: {str(e)}"
    
    def compute_bleu(self, reference: str, candidate: str) -> float:
        """
        Calculates BLEU (Bilingual Evaluation Understudy) score for evaluating translation quality.
        Reference: Ground-truth sentence.
        Candidate: Translated sentence.
        """
        reference = [reference.split()]  # Tokenize reference sentence (as list of list)
        candidate = candidate.split()  # Tokenize candidate sentence
        bleu_score = sentence_bleu(reference, candidate)  # Compute BLEU score
        print(f"BLEU Score: {bleu_score}")  # Output BLEU score
        return bleu_score
    
    def compute_perplexity(self, text: str) -> float:
        """
        Calculates perplexity of a sentence using the loaded transformer model.
        Perplexity measures how well a model predicts a sentence — lower is better.
        """
        inputs = self.tokenizer(text, return_tensors="pt")  # Tokenize input text for PyTorch
        with torch.no_grad():  # Disable gradient calculation (no training)
            # Forward pass to get loss (auto-regressive mode: input = output labels)
            outputs = self.model(**inputs, labels=inputs["input_ids"])
        
        loss = outputs.loss  # Get the loss value
        perplexity = torch.exp(loss).item()  # Convert loss to perplexity (exp(loss))
        print(f"Perplexity: {perplexity}")  # Output perplexity
        return perplexity

# Initialize the translation model (loads Google translator and M2M100 model)
model = TranslationModel()
