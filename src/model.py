import os
import urllib.request
from llama_cpp import Llama
import psutil
import configparser
import math

class MyLanguageModel:
    def __init__(self, name) -> None:
        self.name = name
        config = configparser.ConfigParser()
        config.read('src/config.ini')
        self.url = config.get('MODEL','url')
        self.path = config.get('MODEL','path')
        self.sequence_length = int(config.get('MODEL','max_sequence_length'))
        self.layers = int(config.get('MODEL','gpu_layers'))
        self.ratio = float(config.get('MODEL','cpu_ratio'))
        self.download_file()
        self.llm = self.get_llm()
        self.history = f"{self.name}: The AI Cinema Ticket Assistant is here to help you get your movie tickets quickly and easily! How may I assist you today?"

    def download_file(self):
        # Dowloading GGML model from HuggingFace, checks if the file already exists before downloading
        if not os.path.isfile(self.path):
            urllib.request.urlretrieve(self.url, self.path)
            print("File downloaded successfully.")
        else:
            print("File already exists.")

    def get_llm(self):
        llm = Llama(
            model_path=self.path,
            n_ctx=self.sequence_length,
            n_threads=math.floor(psutil.cpu_count()*self.ratio),
            n_gpu_layers=self.layers,         
        )
        return llm

    def generate_text(self, prompt, max_tokens=512, temperature=0.1, top_p=0.5, echo=False, stop=["#", "User:"]):
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=echo,
            stop=stop,
        )
        return output["choices"][0]["text"].strip()

    def generate_prompt_from_template(self, input):
        chat_prompt_template = f"""<|im_start|>system
You are an assistant that supports the user to quickly buy a ticket to the cinema.<|im_end|>
<|im_start|>history
{self.history}<|im_end|>
<|im_start|>user
{input}<|im_end|>"""
        return chat_prompt_template

    def answer(self, question):
        prompt = self.generate_prompt_from_template(question)
        output = self.generate_text(prompt)
        output = output.replace(self.name + ": ", "")
        self.history += f"\nUser: {question}"
        self.history += f"\n{self.name}: {output}"
        return output

if __name__ == "__main__":
    model = MyLanguageModel("Cinema ticket chatbot")
    model.history = f"{model.name}: The AI Cinema Ticket Assistant is here to help you get your movie tickets quickly and easily! How may I assist you today?"
    output = model.answer("Recommend me a movie")
    print(output)