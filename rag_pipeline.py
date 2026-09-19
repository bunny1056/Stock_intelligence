import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

VECTORSTORE_DIR = "vectorstore"


class StockResearchRAG:

    def __init__(self):

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.vectorstore = FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    def retrieve(self, query, companies=None, k=8):

        if companies:
            results = []

            for company in companies:
                docs = self.vectorstore.similarity_search(
                    query,
                    k=k,
                    filter={"company": company}
                )
                results.extend(docs)

            return results

        return self.vectorstore.similarity_search(
            query,
            k=k
        )

    def generate_answer(self, query, companies=None):

        documents = self.retrieve(
            query,
            companies=companies
        )

        if not documents:
            return "No relevant information was found."

        context_parts = []

        for i, doc in enumerate(documents):

            source = doc.metadata.get("source", "Unknown")
            company = doc.metadata.get("company", "Unknown")
            page = doc.metadata.get("page", "Unknown")

            context_parts.append(
                f"""
SOURCE {i + 1}
Company: {company}
Report: {source}
Page: {page}

{doc.page_content}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
You are a financial research assistant.

Answer the user's question using ONLY the provided
financial-report context.

Rules:
1. Do not invent financial figures.
2. Clearly distinguish facts from interpretation.
3. If the reports do not contain enough information,
   explicitly state that.
4. Compare companies when multiple companies are provided.
5. Cite sources using [Company | Report | Page].

USER QUESTION:
{query}

FINANCIAL REPORT CONTEXT:
{context}
"""

        response = self.llm.invoke(prompt)

        return response.content
