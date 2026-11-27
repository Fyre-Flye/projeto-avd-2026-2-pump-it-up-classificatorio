"""Gera as versoes em PDF do roteiro e do guia de arguicao a partir dos arquivos Markdown.

Usa o mesmo visual do relatorio.pdf (Montserrat, secoes em azul, caixas azul-claro), para os documentos
do grupo ficarem com a mesma cara. O conteudo vem so dos .md: para mudar o texto, edite o .md e rode de novo.

Execucao, a partir da raiz do repositorio:
    python docs/gerar_pdfs_apoio.py
"""

import html
import io
import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar_relatorio  # noqa: E402
from gerar_relatorio import (  # noqa: E402  (reaproveita o visual e a paginacao do relatorio)
    CINZA_NOTA,
    DIR_FONTES,
    MARGEM_X,
    TEM_MONTSERRAT,
    criar_archive,
    documento,
    paginar,
    unidades_de_layout,
)

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTOS = [
    ("docs/ROTEIRO_APRESENTACAO.md", "docs/ROTEIRO_APRESENTACAO.pdf", "Roteiro de Apresentação"),
    ("docs/GUIA_ARGUICAO_E_VARIAVEIS.md", "docs/GUIA_ARGUICAO_E_VARIAVEIS.pdf", "Guia de Arguição e Variáveis"),
]

CSS_EXTRA = """
<style>
  .doc-titulo { font-size: 19pt; font-weight: bold; color: #0F62FE; margin: 0 0 10pt 0; line-height: 1.2; }
  pre { font-family: 'Consolas', Courier, monospace; font-size: 8.8pt; background-color: #EAF2FF;
        padding: 8pt 10pt; margin: 4pt 0 8pt 0; white-space: pre-wrap; }
  ol, ul { margin: 2pt 0 6pt 15pt; padding: 0; }
  li { margin-bottom: 3.5pt; }
  li ul, li ol { margin-top: 3pt; margin-bottom: 2pt; }
  .box-azul p { margin: 0 0 4pt 0; }
</style>
"""
# O documento() do relatorio le CSS_BASE na hora da chamada: somando aqui, o estilo extra vai para o <head>
# (o MuPDF ignora <style> dentro do <body>).
gerar_relatorio.CSS_BASE = gerar_relatorio.CSS_BASE + CSS_EXTRA


# ---------------------------------------------------------------------------
# Markdown -> HTML (so o que os dois documentos usam: titulos, listas, tabelas, citacao, codigo)
# ---------------------------------------------------------------------------
def inline(texto: str) -> str:
    """Negrito, italico e codigo, com o restante escapado (o negrito pode conter `codigo`)."""
    codigos: list[str] = []

    def guarda(m):
        codigos.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codigos) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guarda, texto)
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codigos[int(m.group(1))], t)


def tabela(linhas: list[str]) -> str:
    def celulas(linha):
        return [c.strip() for c in linha.strip().strip("|").split("|")]

    cab = celulas(linhas[0])
    corpo = [celulas(l) for l in linhas[2:]]
    out = ["<table><thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in cab]
    out.append("</tr></thead><tbody>")
    for linha in corpo:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in linha) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def lista(linhas: list[str]) -> str:
    """Listas com aninhamento pela indentacao; blocos de codigo dentro de itens viram <pre>."""
    out: list[str] = []
    pilha: list[tuple[int, str]] = []  # (indentacao, "ul" ou "ol")
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        m = ITEM.match(linha)
        if m:
            ind, marca, texto = len(m.group(1)), m.group(2), m.group(3)
            tipo = "ol" if marca[0].isdigit() else "ul"
            while pilha and pilha[-1][0] > ind:
                out.append(f"</li></{pilha.pop()[1]}>")
            if pilha and pilha[-1][0] == ind:
                if pilha[-1][1] != tipo:
                    out.append(f"</li></{pilha.pop()[1]}><{tipo}><li>")
                    pilha.append((ind, tipo))
                else:
                    out.append("</li><li>")
            else:
                out.append(f"<{tipo}><li>")
                pilha.append((ind, tipo))
            out.append(inline(texto))
        elif linha.strip().startswith("```"):
            codigo = []
            i += 1
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                codigo.append(linhas[i].strip())
                i += 1
            out.append(f"<pre>{html.escape(chr(10).join(codigo))}</pre>")
        elif linha.strip():
            out.append(" " + inline(linha.strip()))
        i += 1
    while pilha:
        out.append(f"</li></{pilha.pop()[1]}>")
    return "".join(out)


def markdown_para_html(md: str) -> str:
    linhas = md.splitlines()
    out: list[str] = []
    i = 0
    primeiro_titulo = True
    while i < len(linhas):
        linha = linhas[i]
        s = linha.strip()
        if not s or s == "---":
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            nivel = len(m.group(1))
            texto = inline(m.group(2))
            if nivel == 1 and primeiro_titulo:
                out.append(f'<div class="doc-titulo">{texto}</div>')
                primeiro_titulo = False
            else:
                out.append(f"<h{min(nivel - 1, 3) if nivel > 1 else 1}>{texto}</h{min(nivel - 1, 3) if nivel > 1 else 1}>")
            i += 1
            continue
        if s.startswith("```"):
            codigo = []
            i += 1
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                codigo.append(linhas[i])
                i += 1
            out.append(f"<pre>{html.escape(chr(10).join(codigo))}</pre>")
            i += 1
            continue
        if s.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i])
                i += 1
            out.append(tabela(bloco))
            continue
        if s.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                bloco.append(re.sub(r"^\s*>\s?", "", linhas[i]))
                i += 1
            out.append(f'<div class="box-azul">{markdown_para_html(chr(10).join(bloco))}</div>')
            continue
        if ITEM.match(linha):
            bloco = []
            while i < len(linhas) and (
                ITEM.match(linhas[i])
                or (linhas[i].startswith((" ", "\t")) and linhas[i].strip())
            ):
                bloco.append(linhas[i])
                i += 1
            out.append(lista(bloco))
            continue
        # Paragrafo: linhas seguidas; "dois espacos no fim" vira quebra de linha
        par = []
        while i < len(linhas) and linhas[i].strip() and not re.match(r"^\s*(#|\||>|```|---)", linhas[i]) and not ITEM.match(linhas[i]):
            quebra = "<br/>" if linhas[i].endswith("  ") else " "
            par.append(inline(linhas[i].strip()) + quebra)
            i += 1
        out.append("<p>" + "".join(par).strip() + "</p>")
    return "".join(out)


def dividir_tabelas_grandes(unidades: list[str], arch, area) -> list[str]:
    """Uma tabela que nao cabe sozinha numa pagina vira varias, cada uma com o cabecalho repetido."""
    saida: list[str] = []
    for unidade in unidades:
        if "<table>" not in unidade or gerar_relatorio.cabe(unidade, arch, area):
            saida.append(unidade)
            continue
        antes, resto = unidade.split("<table>", 1)
        cab, corpo = resto.split("<tbody>", 1)
        corpo, depois = corpo.split("</tbody></table>", 1)
        linhas = re.findall(r"<tr>.*?</tr>", corpo, flags=re.S)
        atual: list[str] = []
        prefixo = antes
        for linha in linhas:
            teste = prefixo + "<table>" + cab + "<tbody>" + "".join(atual + [linha]) + "</tbody></table>"
            if atual and not gerar_relatorio.cabe(teste, arch, area):
                saida.append(prefixo + "<table>" + cab + "<tbody>" + "".join(atual) + "</tbody></table>")
                atual, prefixo = [linha], ""
            else:
                atual.append(linha)
        saida.append(prefixo + "<table>" + cab + "<tbody>" + "".join(atual) + "</tbody></table>" + depois)
    return saida


def gerar(origem: str, destino: str, rotulo: str) -> None:
    md = (ROOT / origem).read_text(encoding="utf-8")
    corpo = markdown_para_html(md)
    arch = criar_archive()
    mediabox = pymupdf.paper_rect("a4")
    area = mediabox + (MARGEM_X, 48, -MARGEM_X, -46)
    paginas = paginar(dividir_tabelas_grandes(unidades_de_layout(corpo), arch, area), arch, area)

    bio = io.BytesIO()
    writer = pymupdf.DocumentWriter(bio)
    for idx, html_pagina in enumerate(paginas, start=1):
        story = pymupdf.Story(html=documento(html_pagina), archive=arch)
        dev = writer.begin_page(mediabox)
        mais, _ = story.place(area)
        if mais:
            print(f"[AVISO] {rotulo}: pagina {idx} tem um bloco maior que a pagina.")
        story.draw(dev)
        writer.end_page()
    writer.close()

    doc = pymupdf.open("pdf", bio.getvalue())
    total = len(doc)
    fonte = str(DIR_FONTES / "Montserrat-Regular.ttf") if TEM_MONTSERRAT else None
    for idx, page in enumerate(doc):
        if fonte:
            page.insert_font(fontname="mont_r", fontfile=fonte)
            fn, largura = "mont_r", pymupdf.Font(fontfile=fonte).text_length
        else:
            fn = "helv"
            largura = lambda txt, fontsize: pymupdf.get_text_length(txt, fontname="helv", fontsize=fontsize)
        page.insert_text((MARGEM_X, mediabox.height - 22), f"{rotulo} · Projeto Final AVD 2026.2 · Grupo 6",
                         fontsize=7.4, fontname=fn, color=CINZA_NOTA)
        num = f"{idx + 1} / {total}"
        page.insert_text((mediabox.width - MARGEM_X - largura(num, fontsize=7.4), mediabox.height - 22), num,
                         fontsize=7.4, fontname=fn, color=CINZA_NOTA)
    caminho = ROOT / destino
    doc.save(str(caminho), garbage=4, deflate=True, clean=True)
    doc.close()
    print(f"Gerado: {destino} ({total} paginas)")


if __name__ == "__main__":
    for origem, destino, rotulo in DOCUMENTOS:
        gerar(origem, destino, rotulo)
