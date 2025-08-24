.PHONY: dev debug

dev:
	langgraph dev

debug:
	langgraph dev --debug-port 5678	

build:
	langgraph build -t ghcr.io/ryaneggz/langgraph-starter:latest --push
