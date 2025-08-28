import asyncio
from langgraph.pregel.remote import RemoteGraph
from langgraph_sdk import get_client

sync_client = get_client(url="https://langserve.enso.sh", api_key="super-secret-key")
remote_graph = RemoteGraph("xml_agent", client=sync_client)

async def main():
    async for chunk in remote_graph.astream({
        "messages": [{"role": "user", "content": "what's the weather in sf"}]
    }, stream_mode="messages"):
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())

