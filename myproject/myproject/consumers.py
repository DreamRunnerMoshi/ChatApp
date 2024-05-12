# consumers.py

import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class ChatGPTConsumer(AsyncWebsocketConsumer):

    client = OpenAI(
            organization='org-ROdsRxFwHq5KOHYVhreIGG25',
            project='proj_dyNIbzUJx56xiXHve8VY9P3A',
        )

    async def websocket_receive(self, message):
        await self.stream_completions(message=message['text'])

    async def stream_completions(self, message):

        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": "{message}".format(message=message)}],
            stream=True,
        )

        for chunk in stream:
            choice = chunk.choices[0]
            if choice.finish_reason!='stop' and choice.delta.content is not None:
                await self.send(text_data=chunk.choices[0].delta.content)
                await asyncio.sleep(.05)
            else:
                await self.send(text_data='[DONE]')