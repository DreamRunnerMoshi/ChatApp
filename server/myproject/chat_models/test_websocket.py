import asyncio
import pytest
import websockets
import json

@pytest.mark.asyncio
async def test_websocket():
    uri = "ws://localhost:8000/ws/chatgpt/"
    async with websockets.connect(uri) as websocket:
        test_message = json.dumps({
            "stream": False,
            "messages": [{"role": "user", "content": "Hello, GPT!"}]
        })
        await websocket.send(test_message)
        
        response = await websocket.recv()
        assert response  == "Hello! How can I assist you today?"

# Run the test
if __name__ == "__main__":
    asyncio.run(test_websocket())
