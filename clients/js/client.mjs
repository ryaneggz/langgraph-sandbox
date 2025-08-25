import { Client } from "@langchain/langgraph-sdk";
import { RemoteGraph } from "@langchain/langgraph/remote";


// Point this to your running LangGraph server (FastAPI JSON-RPC, etc.)
const client = new Client({apiUrl: "http://localhost:2024"});

// Replace with your graph id / name
const GRAPH_ID = "article_writer";
const remoteGraph = new RemoteGraph({ graphId: GRAPH_ID, client });
const input = {
    messages: [
      { role: "user", content: "Write an article about the latest trends in AI" },
    ],
  };

async function run(stream = true) {
  // create a thread (or use an existing thread instead)
  const thread = await client.threads.create();
  const config = { configurable: { thread_id: thread.thread_id }, streamMode: "updates"};

  if (stream) {
    // stream outputs from the graph
    for await (const chunk of await remoteGraph.stream(input, config)) {
      console.log(JSON.stringify(chunk));
    }
  } else {
    const result = await remoteGraph.invoke(input, config);
    console.log(result);
  }
}

run().catch(console.error);
