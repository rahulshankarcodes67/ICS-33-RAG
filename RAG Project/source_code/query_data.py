import os
import argparse
from flask import Flask, request, jsonify, render_template_string
from langchain_groq import ChatGroq
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from get_embedding_function import get_embedding_function

# Configuration
CHROMA_PATH = ""
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

app = Flask(__name__)

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RAG QA Frontend</title>
</head>
<body>
    <h1>RAG Question-Answer Interface</h1>
    <textarea id="question" rows="4" cols="60" placeholder="Enter your question here..."></textarea><br/>
    <button onclick="ask()">Ask</button>
    <pre id="answer"></pre>

    <script>
    async function ask() {
        const q = document.getElementById('question').value;
        const res = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: q })
        });
        const data = await res.json();
        document.getElementById('answer').textContent = `Answer: ${data.answer}\nSources: ${data.sources.join(', ')}`;
    }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/query', methods=['POST'])
def query():
    payload = request.get_json()
    question = payload.get('question', '')

    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_score(question, k=5)

    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context,
        question=question
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    ai_msg = llm.invoke([("system", prompt)])
    answer = ai_msg.content

    sources = [doc.metadata.get('id') for doc, _ in results]
    return jsonify({ 'answer': answer, 'sources': sources })

if __name__ == '__main__':
    app.run(debug=True)
