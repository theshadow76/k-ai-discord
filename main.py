import subprocess
from discord.ext import commands
import vertexai
from vertexai.preview.language_models import CodeGenerationModel, CodeChatModel, ChatModel, InputOutputTextPair # type: ignore
import discord
import uvicorn
import threading
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse(content={"Message": "Hello, World!"})


def ChatModel(data):
    vertexai.init(project="flash-garage-392521", location="us-central1")
    chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 1024
    }
    chat = chat_model.start_chat()
    response = chat.send_message(data, **parameters)
    return response.text

def model(data):
    vertexai.init(project="flash-garage-392521", location="us-central1")
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 2048
    }
    model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = model.predict(
        prefix = data,
        **parameters
    )
    return response.text

def ChatGen(data):
    vertexai.init(project="flash-garage-392521", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.7,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat()
    response = chat.send_message(data, **parameters)
    return response.text

def run_code(python_code):
  """Runs Python code and C++ code using subprocess.

  Args:
    python_code: The Python code to run.
    c_code: The C++ code to compile and run.

  Returns:
    The output of the Python code and C++ code.
  """

  if python_code is not None:
    # Run the Python code.
    data = str(python_code).replace("```py", "")
    data1 = str(data).replace("```", "")
    with open("./python_code.py", "w") as f:
        f.write(data1)    
    python_run_command = "python python_code.py"
    python_run_output = subprocess.check_output(python_run_command, shell=True)
    print(python_run_output)
    return python_run_output, None

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$CodeGen') and message.channel.id == 1128751395219193908:
        data = message.content.replace("$CodeGen", "")
        try:
            await message.channel.send(str(model(data)))
        except Exception as e:
            await message.channel.send(f"I am sorry, something went wrong: {e}")
    if message.content.startswith('$CodeChat') and message.channel.id == 1128751395219193908:
        data = message.content.replace("$CodeChat", "")
        try:
            await message.channel.send(str(ChatModel(data)))
        except Exception as e:
            await message.channel.send(f"I am sorry, something went wrong: {e}")
    if message.content.startswith('$Chat') and message.channel.id == 1128751395219193908:
        data = message.content.replace("$Chat", "")
        try:
            await message.channel.send(str(ChatGen(data)))
        except Exception as e:
            await message.channel.send(f"I am sorry, something went wrong: {e}")
    if message.content.startswith('$RunCodePy') and message.channel.id == 1128751395219193908:
        data = message.content.replace("$RunCodePy", "")
        try: 
            await message.channel.send(str(run_code(data)))
        except Exception as e:
            await message.channel.send(f"I am sorry, something went wrong: {e}")
    if message.content.startswith('$help') and message.channel.id == 1128751395219193908:
        data = message.content.replace("$help", "")
        try: 
            await message.channel.send("My name is K-AI, a model developed by Vigo Walker at The Sunset Code, this is a free model to use within the permition of Vigo Walker or Alexandre Portner, please refer to them for any use, thanks for understanding!")
        except Exception as e:
            await message.channel.send(f"I am sorry, something went wrong: {e}")

def run_bot():
    client.run('MTEyODc0NjU0MDE0NDUzMzU3NQ.Gzlafr.Z1xtQgZmEWRM0TdOsXJ8jk4lboNqiEhWKe5bM0')

@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=run_bot)
    thread.start()