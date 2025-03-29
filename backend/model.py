from transformers import pipeline, DPRQuestionEncoder, DPRQuestionEncoderTokenizer
import torch

# Load Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load DPR Encoder for Query Embeddings
dpr_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
dpr_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
dpr_encoder.eval()  # Set to evaluation mode

def summarize_text(text):
    if not text:
        return "No content to summarize."

    summary = summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return summary

def get_query_embedding(query):
    with torch.no_grad():
        inputs = dpr_tokenizer(query, return_tensors="pt")
        embedding = dpr_encoder(**inputs).pooler_output
        return embedding.squeeze().cpu()  # Convert tensor to NumPy array

