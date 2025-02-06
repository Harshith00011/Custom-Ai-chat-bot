# Custom-Ai-chat-bot
The Custom AI Chat Bot is designed to assist users in provide information on user datasets. Built using  Python, React, Memgraph, Docker. This chatbot offers natural language understanding, where user can ask questions in natural language and then a language model is used(open-ai) used to understand it and embedding it. This llm is also integrated with memgrapgh where the data sets of the user are there in form of Graph data base. Now the embeddings are get queried by in memgraph and then the response tokes will get converted again into natural language by llm so that the user can understand.

📍 User → Frontend → API Server → AI Model → Memgraph (Graph Database) → AI Model → Response sent back to user:
User: Sends a query or message to the chatbot.
Frontend: Receives the input and forwards it to the backend via API calls.
API Server: Processes the request and forwards it to the AI model.
AI Model (1st Instance): Generates an initial response based on the trained dataset.
Memgraph (Graph Database):Stores and retrieves conversation history, Maintains contextual relationships for improved responses, Enhances chatbot memory and knowledge base.
AI Model (2nd Instance):Re-evaluates the response with enriched context from Memgraph. Generates a refined, context-aware answer.
Response Sent Back to User: The chatbot delivers an improved, contextually aware response.

Technologies Used:
Frontend: React.js, HTML, CSS
Backend: Python (Fast API)
Database: Memgraph (GraphDB)
AI/ML Models: OpenAI GPT-4, LangChain, Hugging Face Transformers
Deployment: Docker

Contact:
For any queries or support, reach out to:
Email: harshithgandham11@gmail.com
LinkedIn: www.linkedin.com/in/harshith-gandham

Acknowledgements:
Credit to Memgraph and individuals that helped to the development of this project.
![image](https://github.com/user-attachments/assets/bd410f19-4fb7-4e17-8cd0-e588ccc1fcd0)
