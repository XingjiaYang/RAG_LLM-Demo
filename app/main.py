from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from qdrant_client.http.exceptions import UnexpectedResponse

from app.config import settings
from app.llm_client import LocalLLMClient
from app.rag import RAGPipeline
from app.vector_store import SearchResult, VectorStore


app = FastAPI(title="Local RAG LLM", version="0.1.0")


INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Local RAG LLM</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f4;
      --panel: #ffffff;
      --text: #1f2933;
      --muted: #64707d;
      --line: #d9ded6;
      --accent: #1f7a5c;
      --accent-strong: #176348;
      --danger: #b42318;
      --code: #eef2ec;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    main {
      width: min(1120px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 32px 0;
    }

    header {
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
    }

    h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 760;
      line-height: 1.15;
    }

    .status {
      min-width: 126px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 8px 10px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }

    .status.ok {
      color: var(--accent-strong);
      border-color: #add8c7;
      background: #eff8f3;
    }

    .status.bad {
      color: var(--danger);
      border-color: #f3b4ad;
      background: #fff2f0;
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
      gap: 16px;
      align-items: start;
    }

    section {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }

    .ask-panel {
      padding: 16px;
    }

    label {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 650;
    }

    textarea {
      width: 100%;
      min-height: 156px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      color: var(--text);
      font: inherit;
      line-height: 1.5;
      outline: none;
    }

    textarea:focus,
    input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(31, 122, 92, 0.13);
    }

    .controls {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-top: 12px;
    }

    .top-k {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-size: 14px;
    }

    input {
      width: 72px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 9px 10px;
      color: var(--text);
      font: inherit;
      outline: none;
    }

    button {
      min-width: 112px;
      border: 0;
      border-radius: 8px;
      background: var(--accent);
      color: white;
      padding: 10px 14px;
      font: inherit;
      font-weight: 720;
      cursor: pointer;
    }

    button:hover {
      background: var(--accent-strong);
    }

    button:disabled {
      cursor: wait;
      opacity: 0.62;
    }

    .answer-panel {
      min-height: 280px;
      padding: 16px;
    }

    h2 {
      margin: 0 0 12px;
      font-size: 15px;
      font-weight: 760;
    }

    .answer {
      min-height: 120px;
      white-space: pre-wrap;
      line-height: 1.62;
    }

    .placeholder {
      color: var(--muted);
    }

    .error {
      color: var(--danger);
    }

    .contexts {
      margin-top: 16px;
      border-top: 1px solid var(--line);
      padding-top: 14px;
    }

    .context-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      margin-top: 10px;
      background: #fbfcfa;
    }

    .context-meta {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }

    code {
      display: block;
      overflow-wrap: anywhere;
      border-radius: 6px;
      background: var(--code);
      padding: 8px;
      color: #374151;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
      line-height: 1.45;
      white-space: pre-wrap;
    }

    @media (max-width: 820px) {
      main {
        width: min(100vw - 24px, 720px);
        padding: 20px 0;
      }

      header {
        align-items: stretch;
        flex-direction: column;
      }

      .layout {
        grid-template-columns: 1fr;
      }

      .controls {
        align-items: stretch;
        flex-direction: column;
      }

      .top-k {
        justify-content: space-between;
      }

      button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Local RAG LLM</h1>
      <div id="status" class="status">Checking</div>
    </header>

    <div class="layout">
      <section class="ask-panel">
        <label for="question">Question</label>
        <textarea id="question" placeholder="What is DuckDB good for?"></textarea>
        <div class="controls">
          <label class="top-k" for="topK">
            Top K
            <input id="topK" type="number" min="1" max="20" value="3">
          </label>
          <button id="askButton" type="button">Ask</button>
        </div>
      </section>

      <section class="answer-panel">
        <h2>Answer</h2>
        <div id="answer" class="answer placeholder">Waiting for a question.</div>
        <div id="contexts" class="contexts" hidden>
          <h2>Contexts</h2>
          <div id="contextList"></div>
        </div>
      </section>
    </div>
  </main>

  <script>
    const statusEl = document.getElementById("status");
    const questionEl = document.getElementById("question");
    const topKEl = document.getElementById("topK");
    const askButton = document.getElementById("askButton");
    const answerEl = document.getElementById("answer");
    const contextsEl = document.getElementById("contexts");
    const contextListEl = document.getElementById("contextList");

    function setStatus(text, className) {
      statusEl.textContent = text;
      statusEl.className = `status ${className || ""}`.trim();
    }

    async function checkHealth() {
      try {
        const response = await fetch("/health");
        const data = await response.json();
        const ready = Boolean(data.qdrant && data.llm);
        setStatus(ready ? "Ready" : "Degraded", ready ? "ok" : "bad");
      } catch {
        setStatus("Offline", "bad");
      }
    }

    function renderContexts(contexts) {
      contextListEl.innerHTML = "";
      contextsEl.hidden = contexts.length === 0;

      for (const item of contexts) {
        const wrapper = document.createElement("div");
        wrapper.className = "context-item";

        const meta = document.createElement("div");
        meta.className = "context-meta";

        const source = document.createElement("span");
        source.textContent = `${item.source} · chunk ${item.chunk_id}`;

        const score = document.createElement("span");
        score.textContent = item.score.toFixed(4);

        const text = document.createElement("code");
        text.textContent = item.text;

        meta.appendChild(source);
        meta.appendChild(score);
        wrapper.appendChild(meta);
        wrapper.appendChild(text);
        contextListEl.appendChild(wrapper);
      }
    }

    async function ask() {
      const question = questionEl.value.trim();
      if (!question) {
        questionEl.focus();
        return;
      }

      askButton.disabled = true;
      askButton.textContent = "Thinking";
      answerEl.className = "answer placeholder";
      answerEl.textContent = "Thinking...";
      renderContexts([]);

      try {
        const response = await fetch("/rag", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            question,
            top_k: Number(topKEl.value || 3)
          })
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "Request failed");
        }

        answerEl.className = "answer";
        answerEl.textContent = data.answer;
        renderContexts(data.contexts || []);
      } catch (error) {
        answerEl.className = "answer error";
        answerEl.textContent = error.message;
      } finally {
        askButton.disabled = false;
        askButton.textContent = "Ask";
      }
    }

    askButton.addEventListener("click", ask);
    questionEl.addEventListener("keydown", (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        ask();
      }
    });

    checkHealth();
  </script>
</body>
</html>
"""


class RAGRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)


class ContextResponse(BaseModel):
    text: str
    source: str
    chunk_id: int
    score: float

    @classmethod
    def from_search_result(cls, result: SearchResult) -> "ContextResponse":
        return cls(
            text=result.text,
            source=result.source,
            chunk_id=result.chunk_id,
            score=result.score,
        )


class RAGResponse(BaseModel):
    answer: str
    contexts: list[ContextResponse]


vector_store = VectorStore(settings)
llm_client = LocalLLMClient(settings)
rag_pipeline = RAGPipeline(
    settings,
    vector_store=vector_store,
    llm_client=llm_client,
)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return INDEX_HTML


@app.get("/health")
def health() -> dict[str, object]:
    qdrant_ok = True
    try:
        vector_store.client.get_collections()
    except Exception:
        qdrant_ok = False

    llm_ok = llm_client.health()

    return {
        "status": "ok" if qdrant_ok and llm_ok else "degraded",
        "qdrant": qdrant_ok,
        "llm": llm_ok,
        "collection": settings.collection_name,
        "llm_base_url": settings.llm_base_url,
        "llm_model": settings.llm_model,
    }


@app.post("/rag", response_model=RAGResponse)
def rag(request: RAGRequest) -> RAGResponse:
    try:
        result = rag_pipeline.answer(request.question, top_k=request.top_k)
    except UnexpectedResponse as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return RAGResponse(
        answer=result.answer,
        contexts=[
            ContextResponse.from_search_result(item) for item in result.contexts
        ],
    )
