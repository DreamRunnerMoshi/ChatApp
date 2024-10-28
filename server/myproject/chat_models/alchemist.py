# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class LangChainGPT(AsyncWebsocketConsumer):

    client = OpenAI(
            organization='org-ROdsRxFwHq5KOHYVhreIGG25',
            project='proj_dyNIbzUJx56xiXHve8VY9P3A',
        )

    async def connect(self):
        
        await self.accept()  # Accept the connection

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        try: 
            messages = json.loads(text_data)
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages= messages,
                stream=True,
            )

            for chunk in stream:
                choice = chunk.choices[0]
                if choice.finish_reason!='stop' and choice.delta.content is not None:
                    await self.send(text_data=chunk.choices[0].delta.content)
                else:
                    await self.send(text_data='[DONE]')
        except Exception as e:
            print(e)
            await self.send(text_data='[ERROR]')
