import { Client } from "@langchain/langgraph-sdk";
import { RemoteGraph } from "@langchain/langgraph/remote";

// Point this to your running LangGraph server (FastAPI JSON-RPC, etc.)
const client = new Client({
  apiUrl: "http://localhost:2024",
  defaultHeaders: {
    "x-api-key": "super-secret-key"
  }
});

// Replace with your graph id / name
const remoteGraph = new RemoteGraph({ graphId: "xml_agent", client });
const input = {
    messages: [
      { role: "user", content: "TSLA stock price?" },
    ],
  };

async function run(stream = true) {
  // create a thread (or use an existing thread instead)
  const thread = await client.threads.create();
  const config = {
    streamMode: "messages",
    configurable: { 
      thread_id: thread.thread_id, 
      model: "openai:gpt-5-nano", 
      system: "You are a helpful assistant that talks your pirate." 
    },
  };

  if (stream) {
    // stream outputs from the graph
    for await (const chunk of await remoteGraph.stream(input, config)) {
      // console.log(JSON.stringify(chunk, null, 2));
      process.stdout.write(chunk[0].content);
    }
  } else {
    const result = await remoteGraph.invoke(input, config);
    console.log(result[0].content);
  }

  // const threadState = await remoteGraph.getState(config);
  // console.log(JSON.stringify(threadState, null, 2));
}

run().catch(console.error);
