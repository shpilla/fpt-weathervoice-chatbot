Aiogram 3.x -based Telegram chatbot that can do two things:
1. Transcribe direct voice messages using OpenAI's Whisper API
2. Give weather info based on OpenWeatherMap in a conversational manner. Context not managed.

###### Enviromental variables to be set prior to execution**
OPENWEATHERMAP_API_KEY (https://home.openweathermap.org/api_keys)
BOT_TOKEN (https://t.me/botfather)
OPENAI_API_KEY (https://platform.openai.com/account/api-keys)

###### How it works?**
**Audio transciption**
1. Download .ogg audio file recieved in a voice message (aiogram)
2. Covert .ogg to .mp3 (pydub). Mandatory step as Whisper API does not accept .ogg files
3. Send created .mp3 file to Whisper API for transcription (openai)
4. Remove temporary stored .ogg and .mp3 files (os)
5. Reply to user with trascription (aiogram)
**Weather conversational manner**
0. Set up langchain with OpenAI model with a OpenWeatherMap agent (langchain on startup)
1. Query the agent with text from user message (langchain)
2. Reply to user with agent's response (aiogram)

Any message without text or voice will notify user about the purpose of the bot.


###### Potential improvements to the bot's functionality
1. Provide LLM responses to voice messages (+text-to-speach?)
2. Fine-tune the agent to be more brave to let the user know that it only talks about weather. (currently answers with weather in London every time it get's lost)