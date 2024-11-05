import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq, AsyncGroq
from openai import OpenAI, AsyncOpenAI
from together import Together, AsyncTogether
from typing import Optional, Union, List, Callable, Dict
# 获取项目根目录而不是当前文件目录
root_dir = Path(__file__).resolve().parent.parent
# 使用项目根目录的.env文件
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)

base_url_openai = "https://api.openai.com/v1"
api_key_openai = os.getenv("OPENAI_API_KEY")

base_url_deepseek = "https://api.deepseek.com"
api_key_deepseek = os.getenv("DEEPSEEK_API_KEY")

base_url_together = "https://api.together.xyz/v1"
api_key_together = os.getenv("TOGETHER_API_KEY")

base_url_groq = "https://api.groq.com"
api_key_groq = os.getenv("GROQ_API_KEY")

model_type_mapping = {
    "deepseek-chat": "DeepSeek",  # 支持function call，但是function call的能力不太行
    "mixtral-8x7b-32768": "Groq",  # 支持function call，但是不会说中文
    "llama3-70b-8192": "Groq",  # 支持function call，并且function call的能力也不错
    "llama3-groq-70b-8192-tool-use-preview": "Groq",
    "llama-3.2-90b-text-preview": "Groq",
    "llama-3.2-70b-versatile-preview": "Groq",
    "gemma2-9b-it": "Groq",
    "Qwen/Qwen2-72B-Instruct": "Together",  # 不支持function call
    "codellama/CodeLlama-34b-Python-hf": "Together",
    "gpt-4o": "OpenAI",
    "gpt-4o-mini": "OpenAI"
}


def get_client(model_type, stream: bool = False):
    if stream:
        if model_type == "DeepSeek":
            return AsyncOpenAI(
                base_url=base_url_deepseek, 
                api_key=api_key_deepseek
            )
        elif model_type == "OpenAI":
            return AsyncOpenAI(
                api_key=api_key_openai
            )
        elif model_type == "Groq":
            return AsyncGroq(
                base_url = base_url_groq,
                api_key = api_key_groq
            )
        elif model_type == "Together":
            return AsyncTogether(
                base_url = base_url_together,
                api_key = api_key_together
            )
    else:
        if model_type == "DeepSeek":
            return OpenAI(
                base_url=base_url_deepseek, 
                api_key=api_key_deepseek
            )
        elif model_type == "OpenAI":
            return OpenAI(
                api_key=api_key_openai
            )
        elif model_type == "Groq":
            return Groq(
                base_url = base_url_groq,
                api_key = api_key_groq
            )
        elif model_type == "Together":
            return Together(
                base_url = base_url_together,
                api_key = api_key_together
        )


async def aget_client(model_type, stream: bool = False):
    if stream:
        if model_type == "DeepSeek":
            return AsyncOpenAI(
                base_url=base_url_deepseek, 
                api_key=api_key_deepseek
            )
        elif model_type == "OpenAI":
            return AsyncOpenAI(
                api_key=api_key_openai
            )
        elif model_type == "Groq":
            return AsyncGroq(
                base_url = base_url_groq,
                api_key = api_key_groq
            )
        elif model_type == "Together":
            return AsyncTogether(
                base_url = base_url_together,
                api_key = api_key_together
            )
    else:
        if model_type == "DeepSeek":
            return OpenAI(
                base_url=base_url_deepseek, 
                api_key=api_key_deepseek
            )
        elif model_type == "OpenAI":
            return OpenAI(
                api_key=api_key_openai
            )
        elif model_type == "Groq":
            return Groq(
                base_url = base_url_groq,
                api_key = api_key_groq
            )
        elif model_type == "Together":
            return Together(
                base_url = base_url_together,
                api_key = api_key_together
        )


async def get_model_response(model_name, messages, temperature=0, is_json=False, tools: Optional[List[Callable]] = None, stop: Optional[Union[str, List]] = None):
    model_type = model_type_mapping[model_name]
    client = await aget_client(model_type)
    
    if is_json:
        chat_completion = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            response_format = {"type": "json_object"},
            stop = stop
        )
    else:
        chat_completion = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            stop = stop
        )
    return chat_completion.choices[0].message.content


def get_model_response_with_tools(model_name:str="deepseek-chat", messages:List[Dict[str, str]]=[], temperature=0, is_json=False, tools: Optional[List[Callable]] = None, stop: Optional[Union[str, List]] = None):
    model_type = model_type_mapping[model_name]
    client = get_client(model_type)
    
    if is_json:
        chat_completion = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            response_format = {"type": "json_object"},
            stop = stop,
            tools = tools
        )
    else:
        chat_completion = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            stop = stop,
            tools = tools
        )

    return chat_completion


async def get_model_response_stream(model_name, messages, temperature=0, is_json=False, stop: Optional[Union[str, List]] = None):
    model_type = model_type_mapping[model_name]
    client = await aget_client(model_type, stream=True)

    if is_json:
        chat_completion = await client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            response_format = {"type": "json_object"},
            stop = stop,
            stream = True
        )
    else:
        chat_completion = await client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature = temperature,
            stop = stop,
            stream = True
        )
    return chat_completion


# print(f"Looking for .env at: {env_path}")
# print(f"File exists: {env_path.exists()}")
