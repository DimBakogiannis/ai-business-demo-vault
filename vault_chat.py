import base64
import os
from pathlib import Path

import anthropic
import streamlit as st
from dotenv import load_dotenv

VAULT = Path(__file__).parent
ASSETS = Path(__file__).parent / "vault_chat_assets"
FOLDERS = ["10-News", "20-Concepts", "25-People", "00-Inbox"]
MODEL = "claude-sonnet-4-6"

N8N_CORAL = "#EA4B71"
OBSIDIAN_PURPLE = "#7C3AED"


@st.cache_data
def load_vault() -> tuple[str, int]:
    chunks = []
    for folder in FOLDERS:
        for path in sorted((VAULT / folder).glob("*.md")):
            chunks.append(f"=== {path.relative_to(VAULT)} ===\n{path.read_text()}")
    content = "\n\n".join(chunks)
    return content, len(chunks)


def svg_html(path: Path, width: int = 70) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{width}">'


def clean_answer(text: str) -> str:
    import re
    # [[Page|Display]] -> Display
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    # [[Page]] -> Page
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    # Strip vault path prefix and .md extension from file references
    text = text.replace("ai-business-demo-vault/", "")
    text = re.sub(r"\.md\b", "", text)
    # Escape $ so Streamlit doesn't render dollar amounts as LaTeX math
    text = text.replace("$", r"\$")
    # Last step: every markdown image starts with "![", so escaping it means none can render
    # (a prompt-injected note could otherwise exfiltrate the chat via an image URL)
    return text.replace("![", "!\\[")


load_dotenv(dotenv_path=Path(__file__).parent / ".env")


def get_anthropic_api_key() -> str:
    # Tolerate common .env formatting issues like extra spaces or quoted values.
    raw = os.getenv("ANTHROPIC_API_KEY", "")
    key = raw.strip().strip('"').strip("'")
    if not key:
        st.error("Missing ANTHROPIC_API_KEY. Add it to .env and restart Streamlit.")
        st.stop()
    return key


API_KEY = get_anthropic_api_key()

st.set_page_config(page_title="Vault Chat", page_icon="🧠", layout="centered")

st.markdown(
    f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #1a1626 0%, #2a1f3d 50%, #1a1626 100%);
    }}
    .block-container {{ padding-top: 2rem; }}
    h1, h2, h3 {{ color: {N8N_CORAL} !important; }}
    .stChatMessage {{
        background: rgba(124, 58, 237, 0.08);
        border-left: 3px solid {OBSIDIAN_PURPLE};
        border-radius: 8px;
    }}
    .stChatMessage[data-testid="user-message"] {{
        border-left-color: {N8N_CORAL};
    }}
    .stChatInput textarea {{
        background: rgba(124, 58, 237, 0.05) !important;
        border: 1px solid {OBSIDIAN_PURPLE} !important;
        color: #f0f0f0 !important;
    }}
    .stChatInput textarea:focus {{
        border-color: {N8N_CORAL} !important;
        box-shadow: 0 0 0 1px {N8N_CORAL} !important;
    }}
    .header-bar {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 24px;
        margin-bottom: 8px;
    }}
    .header-bar img:last-child {{
        margin-top: 12px;
    }}
    .vault-title {{
        text-align: center;
        color: {N8N_CORAL};
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }}
    .vault-subtitle {{
        text-align: center;
        color: #c4b5fd;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }}
    .stMarkdown, .stMarkdown p, .stMarkdown li {{ color: #e9e4f5; }}
    .stSpinner > div {{ border-top-color: {N8N_CORAL} !important; }}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="header-bar">
    {svg_html(ASSETS / "n8n.svg", 90)}
    <span style="color: #c4b5fd; font-size: 1.5rem;">×</span>
    {svg_html(ASSETS / "obsidian.svg", 90)}
</div>
<h1 class="vault-title">Vault Chat</h1>
<p class="vault-subtitle">Ask anything about your AI tech news vault</p>
""",
    unsafe_allow_html=True,
)

vault_content, file_count = load_vault()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    f'<p style="text-align:center; color:#7C3AED; font-size:0.85rem;">'
    f"Loaded {file_count} notes from the vault</p>",
    unsafe_allow_html=True,
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about the vault..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the vault..."):
            client = anthropic.Anthropic(api_key=API_KEY)
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": (
                            "You are an assistant for an Obsidian vault of AI tech news. "
                            "Answer questions strictly from the vault content below. "
                            "Be concise (1-3 sentences direct answer, then bullets if helpful). "
                            "Always end with a 'Sources:' list of the markdown filenames you used. "
                            "If the vault doesn't cover the question, say so."
                        ),
                    },
                    {
                        "type": "text",
                        "text": f"<vault>\n{vault_content}\n</vault>",
                        "cache_control": {"type": "ephemeral"},
                    },
                ],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            answer = response.content[0].text
            answer = clean_answer(answer)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
