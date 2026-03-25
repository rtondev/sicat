from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from app.models import FichaCatalografica


PUBLIC_DIR = Path(__file__).parent.parent / "public"
IMAGENS_DIR = PUBLIC_DIR / "imagens"
IMAGENS_DIR.mkdir(parents=True, exist_ok=True)

def gerar_id_curto(ano: int, sequencia: int) -> str:
    return f"FICHA-{ano}-{sequencia:06d}"

def gerar_imagem_png(ficha: FichaCatalografica) -> str:
    IMAGENS_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 1060, 1480
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_cdu = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_cdu = ImageFont.load_default()
    
    margin_x = 50
    margin_y = 40
    box_margin = 30
    
    title_text = "Dados Internacionais de Catalogação na Publicação (CIP)"
    try:
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
    except AttributeError:
        title_width = draw.textsize(title_text, font=font_title)[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, margin_y), title_text, fill='black', font=font_title)
    
    box_y_start = margin_y + 80
    box_x_start = margin_x
    box_x_end = width - margin_x
    box_y_end = height - margin_y - 100
    box_width = box_x_end - box_x_start
    box_height = box_y_end - box_y_start
    
    draw.rectangle(
        [(box_x_start, box_y_start), (box_x_end, box_y_end)],
        outline='black',
        width=2
    )
    
    y_position = box_y_start + box_margin
    line_height = 28
    content_x = box_x_start + box_margin
    
    autor_parts = ficha.autor_nome_completo.split()
    if len(autor_parts) > 1:
        sobrenome = autor_parts[-1]
        nome = ' '.join(autor_parts[:-1])
        autor_formatado = f"{sobrenome.upper()}, {nome}"
    else:
        autor_formatado = ficha.autor_nome_completo.upper()
    
    draw.text((content_x, y_position), autor_formatado, fill='black', font=font_text)
    y_position += line_height + 10
    
    titulo_completo = ficha.titulo
    if ficha.subtitulo:
        titulo_completo += f" : {ficha.subtitulo}"
    draw.text((content_x, y_position), f"{titulo_completo} / {autor_formatado}", fill='black', font=font_text)
    y_position += line_height + 10
    
    cidade_estado = ficha.cidade
    ano_publicacao = ficha.data_ano
    biblioteca_nome = ""
    if ficha.biblioteca:
        biblioteca_nome = ficha.biblioteca.nome
    linha3 = f"{cidade_estado}, {ficha.campus}. Edição. 1ª, {ano_publicacao}."
    if biblioteca_nome:
        linha3 += f" {biblioteca_nome}."
    draw.text((content_x, y_position), linha3, fill='black', font=font_text)
    y_position += line_height + 8
    
    palavras_chave_list = ficha.palavras_chave.split(',') if ficha.palavras_chave else []
    if palavras_chave_list:
        genero = palavras_chave_list[0].strip()
        draw.text((content_x, y_position), f"1. {genero}.", fill='black', font=font_text)
        y_position += line_height
    
    draw.text((content_x, y_position), f"I. {titulo_completo}.", fill='black', font=font_text)
    y_position += line_height
    
    if ficha.orientador_nome_completo:
        orientador_parts = ficha.orientador_nome_completo.split()
        if len(orientador_parts) > 1:
            orientador_sobrenome = orientador_parts[-1]
            orientador_nome = ' '.join(orientador_parts[:-1])
            orientador_formatado = f"{orientador_sobrenome.upper()}, {orientador_nome}"
        else:
            orientador_formatado = ficha.orientador_nome_completo.upper()
        draw.text((content_x, y_position), f"II. {orientador_formatado}.", fill='black', font=font_text)
        y_position += line_height
    
    if ficha.coorientador_nome_completo:
        coorientador_parts = ficha.coorientador_nome_completo.split()
        if len(coorientador_parts) > 1:
            coorientador_sobrenome = coorientador_parts[-1]
            coorientador_nome = ' '.join(coorientador_parts[:-1])
            coorientador_formatado = f"{coorientador_sobrenome.upper()}, {coorientador_nome}"
        else:
            coorientador_formatado = ficha.coorientador_nome_completo.upper()
        draw.text((content_x, y_position), f"III. {coorientador_formatado}.", fill='black', font=font_text)
        y_position += line_height
    
    cdu_text = "CDU 000.0"
    try:
        cdu_bbox = draw.textbbox((0, 0), cdu_text, font=font_cdu)
        cdu_width = cdu_bbox[2] - cdu_bbox[0]
    except AttributeError:
        cdu_width = draw.textsize(cdu_text, font=font_cdu)[0]
    cdu_x = box_x_end - box_margin - cdu_width
    cdu_y = box_y_end - box_margin - 30
    draw.text((cdu_x, cdu_y), cdu_text, fill='black', font=font_cdu)
    
    if ficha.biblioteca and ficha.biblioteca.nome:
        nota_text = f"Bibliotecária responsável pela execução da ficha: {ficha.biblioteca.nome}"
    else:
        nota_text = "Bibliotecária responsável pela execução da ficha caso houver"
    try:
        nota_bbox = draw.textbbox((0, 0), nota_text, font=font_small)
        nota_width = nota_bbox[2] - nota_bbox[0]
    except AttributeError:
        nota_width = draw.textsize(nota_text, font=font_small)[0]
    nota_x = box_x_start + (box_width - nota_width) // 2
    nota_y = box_y_end - box_margin - 50
    draw.text((nota_x, nota_y), nota_text, fill='black', font=font_small)
    
    filename = f"{ficha.id_curto}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
    img_path = IMAGENS_DIR / filename
    
    try:
        img.save(img_path, format='PNG')
    except Exception as e:
        raise
    
    return f"imagens/{filename}"

