from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Web Analyzer API is running"}

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

prompt = PromptTemplate(
    template="""
You are an AI web page analyzer.
Analyze the following website text and answer the user question.
Question:
{question}
Website Text:
{text}
Give a clear and simple answer.
""",
input_variables=["question", "text"]
)

parser = StrOutputParser()

chain = prompt | model | parser


class AnalyzeRequest(BaseModel):
    url: str
    question: str


@app.post("/analyze")
def analyze_website(request: AnalyzeRequest):
    loader = WebBaseLoader(request.url)
    docs = loader.load()

    text = docs[0].page_content[:6000]

    result = chain.invoke({
        "question": request.question,
        "text": text
    })

    return {"answer": result}
