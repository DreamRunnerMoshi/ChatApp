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

    async def connect(self, *args, **kwargs):
        await self.accept()  # Accept the connection
        # You can access parameters from kwargs if needed

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        try: 
            payload = json.loads(text_data)
            gpt_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages= payload['messages'],
                stream=payload['stream'],
            )
            if(payload['stream']):
                await self.chat_stream(gpt_response)
            else: 
                await self.chat_completion(gpt_response)

        except Exception as e:
            await self.send(text_data='[ERROR]')

    async def chat_stream(self, stream):
        """
        If the completion is streamed, the completion object will have multiple choices.
        """

        for chunk in stream:
            choice = chunk.choices[0]
            if choice.finish_reason!='stop' and choice.delta.content is not None:
                await self.send(text_data=chunk.choices[0].delta.content)
            else:
                await self.send(text_data='[DONE]')

    async def chat_completion(self, completion):
        """
        If the completion is not streamed, the completion object will have a single choice.
        ChatCompletion(id='chatcmpl-APTlK5au2y5fSzt3gmXWxaY0iOykN', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Hello! How can I assist you today?', role='assistant', function_call=None, tool_calls=None, refusal=None))], created=1730635970, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=9, prompt_tokens=180, total_tokens=189, prompt_tokens_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens': 0}))
        """
        choice = completion.choices[0]
        print(choice)
        if choice.message.content is not None:
            await self.send(text_data=choice.message.content)
        else:
            await self.send(text_data='[DONE]')        