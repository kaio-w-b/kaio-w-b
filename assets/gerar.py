"""Gera os SVGs do perfil no mesmo estilo do banner (assets/header.svg).

Uso: python assets/gerar.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Fira Code', Consolas, 'Courier New', monospace"

DEFS = """<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1E33"/>
      <stop offset="0.55" stop-color="#123B5C"/>
      <stop offset="1" stop-color="#1B6F8F"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#5EE1C9"/>
      <stop offset="1" stop-color="#4FA8FF"/>
    </linearGradient>
  </defs>"""


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n  {DEFS}\n{body}\n</svg>\n'
    )


def text(x, y, s, size, weight=400, fill="#FFFFFF", family=FONT, extra=""):
    return (
        f'  <text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>'
    )


def largura(s, size):
    """Estimativa da largura do texto na fonte sans-serif."""
    total = 0.0
    for ch in s:
        if ch in "iljtfrI.,:;' ":
            total += 0.32
        elif ch in "mwMW":
            total += 0.86
        elif ch.isupper() or ch.isdigit():
            total += 0.64
        else:
            total += 0.55
    return total * size


def chips(x, y, items, max_w, size=13, gap=8):
    """Desenha chips em linhas, quebrando quando passa de max_w. Retorna (svg, y_final)."""
    out, cx, cy = [], x, y
    for item in items:
        w = int(largura(item, size)) + 22
        if cx + w > x + max_w:
            cx, cy = x, cy + 34
        out.append(
            f'  <rect x="{cx}" y="{cy}" width="{w}" height="26" rx="13" '
            f'fill="#5EE1C9" fill-opacity=".12" stroke="#5EE1C9" stroke-opacity=".45"/>'
        )
        out.append(text(cx + 11, cy + 18, item, size, 500, "#CFE8F5"))
        cx += w + gap
    return "\n".join(out), cy + 26


def secao(nome, titulo, icone):
    body = "\n".join([
        '  <rect width="900" height="64" rx="14" fill="url(#bg)"/>',
        '  <rect x="24" y="22" width="6" height="20" rx="3" fill="url(#accent)"/>',
        text(44, 41, f"{icone}  {titulo}", 22, 700),
        '  <line x1="560" y1="32" x2="876" y2="32" stroke="url(#accent)" stroke-width="2" stroke-opacity=".6"/>',
        '  <circle cx="876" cy="32" r="5" fill="#5EE1C9"/>',
    ])
    (OUT / f"secao-{nome}.svg").write_text(svg(900, 64, body, titulo), encoding="utf-8")


def card(nome, titulo, tag, linhas, destaque, stack):
    w, h = 440, 250
    parts = [
        f'  <rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>',
        f'  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="15" fill="none" stroke="#5EE1C9" stroke-opacity=".25"/>',
        text(24, 44, titulo, 22, 700),
        text(24, 68, tag.upper(), 12, 600, "url(#accent)", extra='letter-spacing="1"'),
    ]
    y = 98
    for linha in linhas:
        parts.append(text(24, y, linha, 14, 400, "#CFE8F5"))
        y += 21
    if destaque:
        parts.append(f'  <rect x="24" y="{y - 6}" width="{w - 48}" height="30" rx="8" fill="#0B1E33" fill-opacity=".55"/>')
        parts.append(text(36, y + 14, "> " + destaque, 13, 500, "#5EE1C9", MONO))
        y += 36
    # mede quantas linhas de chips cabem e ancora o bloco no rodapé do card
    _, fim = chips(0, 0, stack, w - 48, size=12, gap=6)
    c, _ = chips(24, max(y + 4, h - 20 - fim), stack, w - 48, size=12, gap=6)
    parts.append(c)
    (OUT / f"card-{nome}.svg").write_text(svg(w, h, "\n".join(parts), titulo), encoding="utf-8")


def experiencia():
    itens = [
        "Pipelines de extração e estruturação de documentos oficiais (RG, CNH)",
        "API com VLMs para identificar riscos em canteiros de obras e sugerir mitigação",
        "BERTopic em documentos jurídicos e sumarização com Llama 70B",
        "Dashboards de avaliação de qualidade, Python, SQL e Docker",
    ]
    parts = [
        '  <rect width="900" height="210" rx="16" fill="url(#bg)"/>',
        '  <line x1="44" y1="40" x2="44" y2="186" stroke="#5EE1C9" stroke-opacity=".35" stroke-width="2"/>',
        '  <circle cx="44" cy="40" r="9" fill="#5EE1C9"/>',
        text(68, 46, "Dataprev", 22, 700),
        text(170, 46, "Estagiário de Ciência de Dados e IA", 16, 500, "#CFE8F5"),
        text(876, 46, "OUT/2025 – OUT/2026", 13, 600, "url(#accent)", extra='text-anchor="end" letter-spacing="1"'),
    ]
    y = 86
    for item in itens:
        parts.append(f'  <circle cx="74" cy="{y - 5}" r="3" fill="#5EE1C9"/>')
        parts.append(text(88, y, item, 15, 400, "#CFE8F5"))
        y += 28
    (OUT / "experiencia.svg").write_text(svg(900, 210, "\n".join(parts), "Experiência na Dataprev"), encoding="utf-8")


def stack():
    grupos = [
        ("IA GENERATIVA", ["LLMs", "Agentes", "Tool calling", "RAG", "Embeddings", "ChromaDB",
                           "Sentence Transformers", "BERTopic", "VLMs", "LangChain", "LangGraph"]),
        ("MACHINE LEARNING", ["Python", "Pandas", "NumPy", "Scikit-learn", "XGBoost", "LightGBM",
                              "CatBoost", "SHAP"]),
        ("ENGENHARIA E MLOPS", ["FastAPI", "Docker", "SQL", "Git", "Pytest", "Streamlit", "Gradio",
                                "AWS Cloud Practitioner"]),
    ]
    parts, y = [], 30
    for nome, itens in grupos:
        parts.append(text(28, y + 6, nome, 12, 700, "url(#accent)", extra='letter-spacing="1.5"'))
        c, fim = chips(28, y + 18, itens, 844)
        parts.append(c)
        y = fim + 30
    h = y - 4
    parts.insert(0, f'  <rect width="900" height="{h}" rx="16" fill="url(#bg)"/>')
    (OUT / "stack.svg").write_text(svg(900, h, "\n".join(parts), "Stack"), encoding="utf-8")


def rodape():
    body = "\n".join([
        '  <rect width="900" height="120" rx="18" fill="url(#bg)"/>',
        text(450, 52, "Vamos conversar?", 24, 700, extra='text-anchor="middle"'),
        text(450, 82, "Aberto a vagas de AI Engineer, MLOps e Cientista de Dados", 15, 500, "#CFE8F5", extra='text-anchor="middle"'),
        '  <rect x="300" y="98" width="300" height="3" rx="1.5" fill="url(#accent)"/>',
    ])
    (OUT / "rodape.svg").write_text(svg(900, 120, body, "Vamos conversar?"), encoding="utf-8")


if __name__ == "__main__":
    secao("sobre", "Sobre mim", "👋")
    secao("projetos", "Projetos em destaque", "🔭")
    secao("experiencia", "Experiência", "💼")
    secao("stack", "Stack", "🛠️")
    card("lia", "Lia", "Agente de atendimento · desafio técnico",
         ["Agente com tool calling para uma loja de instrumentos:",
          "8 ferramentas e guardrail determinístico contra",
          "preços inventados."],
         "17/18 cenários com o modelo real",
         ["Groq", "gpt-oss-120b", "Streamlit", "Pytest", "LangGraph"])
    card("eixoai", "EixoAI", "RAG sobre a Constituição Federal",
         ["Perguntas e respostas sobre a CF/88 com busca",
          "semântica e avaliação da recuperação em 48",
          "perguntas próprias."],
         "Hit Rate 79% · MRR 0,65 · NDCG 0,68",
         ["e5 embeddings", "ChromaDB", "Llama 3.3", "Gradio"])
    card("churnshield", "ChurnShield", "Machine Learning de ponta a ponta",
         ["Predição de churn com EDA, gradient boosting,",
          "explicabilidade com SHAP e API de predição",
          "em FastAPI com Docker."],
         None,
         ["Scikit-learn", "XGBoost", "LightGBM", "SHAP", "FastAPI", "Docker"])
    card("haxball", "Haxball Agent", "Algoritmo genético · colaboração",
         ["Agente de Haxball com rede neural treinada por",
          "algoritmo genético e por aprendizado",
          "supervisionado."],
         None,
         ["Python", "Pygame", "Redes neurais"])
    experiencia()
    stack()
    rodape()
