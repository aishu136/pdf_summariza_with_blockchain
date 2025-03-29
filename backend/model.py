from transformers import pipeline, DPRQuestionEncoder, DPRQuestionEncoderTokenizer
import torch
import ollama
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate

# Load Hugging Face Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load DPR Encoder
dpr_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
dpr_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
dpr_encoder.eval()

def summarize_text(text, model="transformers"):
    if not text:
        return "No content to summarize."

    if model == "transformers":
        summary = summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    elif model == "ollama":
        response = ollama.chat("mistral", text)
        summary = response["message"]["content"]
    elif model == "langchain":
        prompt = PromptTemplate(template="Summarize: {text}", input_variables=["text"])
        llm = HuggingFacePipeline.from_model_id("facebook/bart-large-cnn")
        chain = LLMChain(llm=llm, prompt=prompt)
        summary = chain.run(text)
    else:
        summary = "Invalid model selection."

    return summary

def get_query_embedding(query):
    with torch.no_grad():
        inputs = dpr_tokenizer(query, return_tensors="pt")
        embedding = dpr_encoder(**inputs).pooler_output
        return embedding.squeeze().cpu()

