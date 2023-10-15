import logging
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
import os
import openai
from aiogram import Bot, Dispatcher
from aiogram.types import File, Message
from aiogram import F
from aiogram.filters.command import Command
import asyncio
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)

# Global variables setup
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

# LLM setup
llm = OpenAI(temperature=0)
tools = load_tools(["openweathermap-api"], llm)
agent_chain = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


async def ask_agent(query: str):
    return agent_chain.run(query)


async def convert_voice_to_text(path: str):
    """Process an MP3 file using Whisper-1"""
    return openai.Audio.transcribe("whisper-1", open(path, "rb"))['text']


async def transcribe(file: File, file_name: str):
    """Converting ogg to mp3, sending it to Whisper and returning the transcription"""
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    ogg_file_path = f'tmp/{file_name}.ogg'
    mp3_file_path = f'tmp/{file_name}.mp3'
    await bot.download_file(file.file_path, ogg_file_path)
    sound = AudioSegment.from_ogg(ogg_file_path)
    os.remove(ogg_file_path)
    sound.export(mp3_file_path, format='mp3')
    text = await convert_voice_to_text(mp3_file_path)
    os.remove(mp3_file_path)
    return text


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(token=BOT_TOKEN)


@dp.message(Command('start'))
async def start_command_handler(message: Message):
    """Handling start command"""
    await message.reply("This is a primitive bot that can do two things:\n"
                        "1. Transcribe direct voice messages using OpenAI('s Whisper API\n"
                        "2. Give weather info based on OpenWeatherMap in a conversational manner. Context not "
                        "managed.\n\n"
                        "Created by @shpilla as a test task.")


@dp.message(F.voice)
async def voice_message_handler(message: Message):
    """Handling voice messages"""
    audio_id = message.voice.file_id
    audio = await bot.get_file(audio_id)
    transcription = await transcribe(file=audio, file_name=audio.file_id)
    await message.reply(transcription)


@dp.message(F.text.len())
async def text_message_handler(message: Message):
    """Handling messages with text"""
    answer = await ask_agent(message.text)
    await message.reply(answer)


@dp.message()
async def unsupported_message_handler(message: Message):
    """Handling messages without text nor voice"""
    await message.reply("Sorry, this type of message is not supported."
                        "Please ask a question about the weather in text or send a voice message for transcription.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
