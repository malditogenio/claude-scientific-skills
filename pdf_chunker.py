#!/usr/bin/env python3
"""
PDF Chunker - Script para dividir PDFs largos en chunks manejables
para procesamiento y aprendizaje incremental.
"""

import sys
import json
import re
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Instalando pdfplumber...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber"])
    import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> dict:
    """Extrae texto del PDF página por página."""
    pages_content = {}

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            pages_content[i] = {
                "page_number": i,
                "text": text.strip(),
                "char_count": len(text)
            }

    return pages_content


def create_chunks(pages_content: dict, chunk_size: int = 3000, overlap: int = 200) -> list:
    """
    Divide el contenido en chunks basados en tamaño de caracteres.

    Args:
        pages_content: Diccionario con contenido por página
        chunk_size: Tamaño aproximado de cada chunk en caracteres
        overlap: Caracteres de solapamiento entre chunks para contexto

    Returns:
        Lista de chunks con metadata
    """
    # Combinar todo el texto con marcadores de página
    full_text = ""
    page_markers = []

    for page_num, content in sorted(pages_content.items()):
        marker_pos = len(full_text)
        page_markers.append({"page": page_num, "position": marker_pos})
        full_text += f"\n\n[PÁGINA {page_num}]\n\n{content['text']}"

    # Dividir en chunks
    chunks = []
    start = 0
    chunk_num = 1

    while start < len(full_text):
        end = start + chunk_size

        # Intentar cortar en un punto natural (párrafo o oración)
        if end < len(full_text):
            # Buscar fin de párrafo
            paragraph_end = full_text.rfind("\n\n", start, end)
            if paragraph_end > start + chunk_size // 2:
                end = paragraph_end
            else:
                # Buscar fin de oración
                sentence_end = max(
                    full_text.rfind(". ", start, end),
                    full_text.rfind("? ", start, end),
                    full_text.rfind("! ", start, end)
                )
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1

        chunk_text = full_text[start:end].strip()

        # Identificar páginas incluidas en este chunk
        pages_in_chunk = []
        for marker in page_markers:
            if start <= marker["position"] < end:
                pages_in_chunk.append(marker["page"])

        if not pages_in_chunk and page_markers:
            # Encontrar la página más cercana
            for marker in reversed(page_markers):
                if marker["position"] <= start:
                    pages_in_chunk = [marker["page"]]
                    break

        chunks.append({
            "chunk_number": chunk_num,
            "total_chunks": None,  # Se actualizará después
            "pages": pages_in_chunk,
            "char_count": len(chunk_text),
            "text": chunk_text
        })

        chunk_num += 1
        start = end - overlap if end < len(full_text) else end

    # Actualizar total de chunks
    for chunk in chunks:
        chunk["total_chunks"] = len(chunks)

    return chunks


def create_semantic_chunks(pages_content: dict, max_chunk_size: int = 4000) -> list:
    """
    Crea chunks basados en secciones semánticas (títulos, capítulos).
    Útil para contenido estructurado.
    """
    full_text = ""
    for page_num, content in sorted(pages_content.items()):
        full_text += f"\n\n[PÁGINA {page_num}]\n\n{content['text']}"

    # Patrones para detectar títulos/secciones
    section_patterns = [
        r'\n(?:CAPÍTULO|CAPITULO|CHAPTER)\s+\d+',
        r'\n(?:PARTE|PART)\s+\d+',
        r'\n(?:SECCIÓN|SECCION|SECTION)\s+\d+',
        r'\n[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,50}(?:\n|$)',  # Títulos en mayúsculas
        r'\n\d+\.\s+[A-ZÁÉÍÓÚ]',  # Numeración tipo "1. Título"
    ]

    # Encontrar posiciones de secciones
    section_positions = [0]
    for pattern in section_patterns:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            section_positions.append(match.start())

    section_positions = sorted(set(section_positions))
    section_positions.append(len(full_text))

    # Crear chunks basados en secciones
    chunks = []
    current_chunk = ""
    chunk_num = 1

    for i in range(len(section_positions) - 1):
        section = full_text[section_positions[i]:section_positions[i+1]]

        if len(current_chunk) + len(section) <= max_chunk_size:
            current_chunk += section
        else:
            if current_chunk:
                chunks.append({
                    "chunk_number": chunk_num,
                    "text": current_chunk.strip(),
                    "char_count": len(current_chunk)
                })
                chunk_num += 1
            current_chunk = section

    if current_chunk:
        chunks.append({
            "chunk_number": chunk_num,
            "text": current_chunk.strip(),
            "char_count": len(current_chunk)
        })

    # Actualizar total
    for chunk in chunks:
        chunk["total_chunks"] = len(chunks)

    return chunks


def save_chunks(chunks: list, output_dir: str, base_name: str):
    """Guarda los chunks en archivos individuales y un índice."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Guardar índice
    index = {
        "total_chunks": len(chunks),
        "chunks": [
            {
                "chunk_number": c["chunk_number"],
                "char_count": c["char_count"],
                "file": f"{base_name}_chunk_{c['chunk_number']:03d}.txt"
            }
            for c in chunks
        ]
    }

    with open(output_path / f"{base_name}_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    # Guardar cada chunk
    for chunk in chunks:
        filename = f"{base_name}_chunk_{chunk['chunk_number']:03d}.txt"
        with open(output_path / filename, "w", encoding="utf-8") as f:
            f.write(f"=== CHUNK {chunk['chunk_number']} de {chunk['total_chunks']} ===\n")
            f.write(f"=== Caracteres: {chunk['char_count']} ===\n\n")
            f.write(chunk["text"])

    return output_path


def print_chunk(chunk: dict):
    """Imprime un chunk de forma legible."""
    print("\n" + "="*60)
    print(f"CHUNK {chunk['chunk_number']} de {chunk['total_chunks']}")
    print(f"Caracteres: {chunk['char_count']}")
    if "pages" in chunk:
        print(f"Páginas: {chunk['pages']}")
    print("="*60 + "\n")
    print(chunk["text"])
    print("\n" + "="*60)


def process_pdf(pdf_path: str, chunk_size: int = 3000, output_dir: str = None):
    """
    Procesa un PDF y lo divide en chunks.

    Args:
        pdf_path: Ruta al archivo PDF
        chunk_size: Tamaño aproximado de cada chunk
        output_dir: Directorio para guardar los chunks (opcional)

    Returns:
        Lista de chunks
    """
    print(f"Procesando: {pdf_path}")

    # Extraer texto
    print("Extrayendo texto del PDF...")
    pages = extract_text_from_pdf(pdf_path)
    print(f"Páginas extraídas: {len(pages)}")

    total_chars = sum(p["char_count"] for p in pages.values())
    print(f"Total de caracteres: {total_chars:,}")

    # Crear chunks
    print(f"\nCreando chunks (tamaño objetivo: {chunk_size} caracteres)...")
    chunks = create_chunks(pages, chunk_size=chunk_size)
    print(f"Chunks creados: {len(chunks)}")

    # Guardar si se especificó directorio
    if output_dir:
        base_name = Path(pdf_path).stem
        save_path = save_chunks(chunks, output_dir, base_name)
        print(f"\nChunks guardados en: {save_path}")

    return chunks


def interactive_review(chunks: list):
    """Permite revisar chunks de forma interactiva."""
    current = 0

    while True:
        print_chunk(chunks[current])

        print("\nOpciones: [n]ext, [p]revious, [g]o to #, [q]uit")
        choice = input(">>> ").strip().lower()

        if choice == 'n' and current < len(chunks) - 1:
            current += 1
        elif choice == 'p' and current > 0:
            current -= 1
        elif choice.startswith('g'):
            try:
                num = int(choice[1:].strip() or input("Número de chunk: "))
                if 1 <= num <= len(chunks):
                    current = num - 1
            except ValueError:
                print("Número inválido")
        elif choice == 'q':
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pdf_chunker.py <archivo.pdf> [tamaño_chunk] [directorio_salida]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    output_directory = sys.argv[3] if len(sys.argv) > 3 else None

    chunks = process_pdf(pdf_file, chunk_size, output_directory)

    print("\n" + "="*60)
    print("RESUMEN DE CHUNKS")
    print("="*60)
    for chunk in chunks:
        pages_info = f" (págs: {chunk.get('pages', 'N/A')})" if chunk.get('pages') else ""
        print(f"  Chunk {chunk['chunk_number']:3d}: {chunk['char_count']:,} caracteres{pages_info}")

    # Opción de revisión interactiva
    if output_directory is None:
        review = input("\n¿Iniciar revisión interactiva? [s/n]: ").strip().lower()
        if review == 's':
            interactive_review(chunks)
