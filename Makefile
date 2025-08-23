.PHONY: dev debug

dev:
	langgraph dev

debug:
	langgraph dev --debug-port 5678	

build:
	langgraph build -t ghcr.io/ryaneggz/langgraph-starter:latest --push

docker:
	docker run \
	-e REDIS_URI=${REDIS_URI} \
	-e DATABASE_URI=${DATABASE_URI} \
	-e LANGSMITH_API_KEY=${LANGSMITH_API_KEY} \
    -e EXA_API_KEY=${EXA_API_KEY} \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    ghcr.io/ryaneggz/langgraph-starter:latest