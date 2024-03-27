from typing import Annotated

from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

from whisper_api.model import WHISPER, ZEPHYR, ZEPHYR_TOKENIZER, device

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Hello, World"}


def get_response(messages):
    inputs = ZEPHYR_TOKENIZER.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(device)
    tokens = ZEPHYR.generate(inputs, max_new_tokens=64, temperature=.5, do_sample=True)
    return ZEPHYR_TOKENIZER.decode(tokens[0], skip_special_tokens=True)


@app.post("/upload/")
def upload(file: Annotated[bytes, File()]):
    result = WHISPER(file)
    response = result.get("text")
    messages = [response, get_response([{"role": "user", "content": response}])]
    return {"file_size": len(file), "messages": [{"id": i, "text": message} for i, message in enumerate(messages)]}
