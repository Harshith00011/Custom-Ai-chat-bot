from fastapi import FastAPI
from app.database import db
from app import schemas
from app.gpt_handler import gpt_handler
from app.llama_handler import llama_handler
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    
    
)

def  generate_event(user_input: schemas.Question):
    try:
        response_accumulator = ""
        for token in gpt_handler.get_response(user_input, stream_to_terminal=False):
            response_accumulator += token
            # Stream only meaningful tokens
            if token.strip():
                data = json.dumps({"message": token})
                yield f"data: {data}\n\n"
        # Ensure to send the final accumulated response at the end
        if response_accumulator.strip():
            final_data = json.dumps({"final_message": response_accumulator})
            yield f"data: {final_data}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
    yield "event: end\n\n"


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up and checking database connection...")
    try:
        # Test database connection
        with db.get_session() as session:
            session.run("RETURN 1")
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Failed to establish database connection: {e}")
        raise e

@app.get("/")
def ask_question():
    print("\n calling default website ")
    return {"question": "calling default webpage", "response": "fastAPI is working!!!"}
# ask Memgraph via GPT
@app.post("/ask/gpt2")
def ask_question(question: schemas.Question,response_model=schemas.QuestionResponse):
    return StreamingResponse(generate_event(question), media_type="text/event-stream")
    

@app.post("/ask/gpt", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = gpt_handler.get_response(question.question)
    return {"question": question.question, "response": response}
    

# ask Memgraph via Llama
@app.post("/ask/llama", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = llama_handler.get_response(question.question)
    return {"question": question.question, "response": response["result"]}
