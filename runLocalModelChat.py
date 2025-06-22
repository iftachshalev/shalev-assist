import threading

from litellm import max_tokens
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch
import time
from colorama import Fore, Style, init
import re
init(autoreset=True)


# MODEL = "microsoft/phi-4-mini-reasoning" # "microsoft/Phi-4-mini-instruct"  # "microsoft/phi-4-mini-reasoning"
MODEL = "microsoft/Phi-4-mini-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_4bit=True
)

#%% chat

if MODEL == "microsoft/Phi-4-mini-instruct":
    system_message = (
        "You are a friendly, helpful, and highly knowledgeable assistant. "
        "You excel at math, logic, and problem-solving, and you have a vast amount of general knowledge. "
        "For every question, first share your reasoning in a section labeled 'Reasoning:'. "
        "Provide a clear and concise answer (up to short sentence) in a section labeled 'Answer:'. "
        "Make sure to answer correctly and accurately, DO NOT make up answers. "
        "Your goal is to be as helpful and insightful as possible!")
elif MODEL == "microsoft/phi-4-mini-reasoning":
    system_message = (
        "You are a friendly, helpful, and highly knowledgeable assistant. "
        "You excel at math, logic, and problem-solving, and you have a vast amount of general knowledge. "
        "For every question, first share your reasoning in a section labeled 'Reasoning:'. "
        "Provide a clear and concise answer (up to short sentence) in a section labeled 'Answer:'. "
        "Do not repeat the question. "
        "Respond in plain text only. "
        "Your goal is to be as helpful and insightful as possible!")
else:
    raise ValueError(f"Unknown model: {MODEL}")

history = [system_message]

while True:
    # Get user input
    user_input = input()

    # Exit condition
    if user_input.lower() in {"exit", "quit", "q"}:
        break

    # Append user input to history and prepare prompt
    history.append(f"User: {user_input}")
    prompt = "\n".join(history) + "\nAssistant:"

    # Tokenize input and generate response
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    start_time = time.time()

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    generation_kwargs = dict(
        input_ids=input_ids,
        max_new_tokens=2048,
        do_sample=True,
        temperature=0.5,
        top_p=0.9,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id,
        streamer=streamer
    )


    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    for new_text in streamer:
        print(new_text, end="", flush=True)

#%%
# # Example questions to test the assistant
# solve for me (with logic only, no code): im 37 and my child is 5. what will be my age when my child will be exactly 1/3 of my age?
# there is a sine wave [-pi,pi] and a line y=x. where do they intersect?
    # there is a cosinus wave [-pi,pi] and a line y=1. where do they intersect?
# solve: 2x-10=-x^2+5x+6
# What is the capital city of Gondor in Lord Of The Rings?
    # Why did the king of Rohan help Gondor at the battle of Minas Tirith?
    # What is the name of the first and second white wizards?

