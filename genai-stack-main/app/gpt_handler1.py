from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import MemgraphGraph
from langchain_openai import ChatOpenAI
import os
import threading
import queue    
from langchain.callbacks.base import BaseCallbackHandler 

# Set up the connection details from environment variables
URI = os.getenv("NEO4J_URI", "bolt://memgraph:7687")
USER = os.getenv("NEO4J_USER", "")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")

class TokenStreamHandler(BaseCallbackHandler):
    def __init__(self,stream_to_terminal=False):
        self.queue = queue.Queue()
        self.stream_to_terminal = stream_to_terminal
    
    def on_llm_new_token(self, token:str, **kwargs)-> None:
        self.queue.put(token)
        if self.stream_to_terminal:
            print(token, end='', flush=True)

    def get_token(self):
        while True:
            token = self.queue.get()
            if token is None:
                break
            yield token
class GPTHandler:
    def __init__(self):
        self.graph = MemgraphGraph(
            url=URI,
            username=USER,
            password=PASSWORD,
        )
        self.chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(
                temperature=0,
            ),
            graph=self.graph,
            verbose=True,
            model_name="gpt-4",
            
        )

    def get_response(self, question: str,stream_to_terminal=False):
        print("\n inside  get response")
        try:
            handler = TokenStreamHandler(stream_to_terminal=stream_to_terminal)
            thread = threading.Thread(target=self.chain, args=(question, handler))
            thread.start()
            for token in handler.get_token():
                yield token
            handler.queue.put(None)
            thread.join()
        except Exception as e:
              yield f"An error occurred: {str(e)}"
        finally :
            print('finally ')
        
    def _run_chain(self, question, handler):
        # This function runs the chain to get a response
        try:

            self.chain.invoke({"query": question}, callbacks=[handler])
        except Exception as e:
            handler.queue.put(None)  # Ensure the queue is closed in case of an error
            raise e
gpt_handler = GPTHandler()

