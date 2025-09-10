import streamlit as st
import yt_dlp
import os
import tempfile
from pathlib import Path
import time

# Configuração da página
st.set_page_config(
    page_title="YouTube Downloader HD",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #FF0000;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 2rem;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 3rem;
}

.success-box {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    margin: 1rem 0;
}

.error-box {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    margin: 1rem 0;
}

.info-box {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #e7f3ff;
    border: 1px solid #b3d9ff;
    color: #0c5460;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def get_video_info(url):
    """Obtém informações do vídeo"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        return None

def format_duration(seconds):
    """Formata duração em segundos para HH:MM:SS"""
    if not seconds:
        return "N/A"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def download_video(url, quality):
    """Baixa o vídeo e retorna o caminho do arquivo"""
    try:
        # Cria pasta temporária
        temp_dir = tempfile.mkdtemp()
        
        # Configurações do yt-dlp
        ydl_opts = {
            'format': f"{quality}[ext=mp4]/best[ext=mp4]/best",
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai informações primeiro
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Faz o download
            ydl.download([url])
            
            return filename, temp_dir, info.get('title', 'video')
            
    except Exception as e:
        return None, None, str(e)

# Interface principal
def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">📺 YouTube Downloader HD</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Baixe vídeos do YouTube em alta qualidade de forma simples e rápida</p>', unsafe_allow_html=True)
    
    # Formulário principal
    with st.form("download_form"):
        st.subheader("🔗 URL do Vídeo")
        url = st.text_input(
            "Cole aqui o link do vídeo do YouTube:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Cole a URL completa do vídeo do YouTube que deseja baixar"
        )
        
        st.subheader("⚙️ Configurações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            quality = st.selectbox(
                "Qualidade do vídeo:",
                options=[
                    "best[height<=720]",
                    "best[height<=1080]", 
                    "best",
                    "worst"
                ],
                format_func=lambda x: {
                    "best[height<=720]": "HD 720p",
                    "best[height<=1080]": "Full HD 1080p", 
                    "best": "Melhor qualidade disponível",
                    "worst": "Menor arquivo (economia de espaço)"
                }[x],
                index=0,
                help="Escolha a qualidade do vídeo para download"
            )
        
        with col2:
            show_info = st.checkbox(
                "Mostrar informações do vídeo",
                value=True,
                help="Exibe detalhes do vídeo antes do download"
            )
        
        # Botões
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            submitted = st.form_submit_button(
                "📥 Baixar Vídeo",
                use_container_width=True,
                type="primary"
            )
    
    # Processamento
    if submitted:
        if not url:
            st.error("❌ Por favor, insira uma URL válida do YouTube.")
            return
            
        if not ("youtube.com" in url or "youtu.be" in url):
            st.error("❌ Por favor, insira uma URL válida do YouTube.")
            return
        
        # Mostrar informações do vídeo se solicitado
        if show_info:
            with st.spinner("🔍 Obtendo informações do vídeo..."):
                info = get_video_info(url)
                
                if info:
                    st.subheader("📋 Informações do Vídeo")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Título:** {info.get('title', 'N/A')}")
                        st.write(f"**Canal:** {info.get('uploader', 'N/A')}")
                        st.write(f"**Duração:** {format_duration(info.get('duration', 0))}")
                    
                    with col2:
                        st.write(f"**Visualizações:** {info.get('view_count', 0):,}")
                        st.write(f"**Data de upload:** {info.get('upload_date', 'N/A')}")
                        st.write(f"**Qualidade selecionada:** {quality}")
                    
                    st.markdown("---")
                else:
                    st.warning("⚠️ Não foi possível obter informações do vídeo, mas o download ainda pode funcionar.")
        
        # Download do vídeo
        with st.spinner("📥 Baixando vídeo... Isso pode levar alguns minutos dependendo do tamanho do arquivo."):
            filename, temp_dir, title = download_video(url, quality)
            
            if filename and os.path.exists(filename):
                st.success("✅ Vídeo baixado com sucesso!")
                
                # Lê o arquivo para download
                with open(filename, 'rb') as file:
                    video_bytes = file.read()
                
                # Botão de download
                st.download_button(
                    label="💾 Clique aqui para baixar o arquivo",
                    data=video_bytes,
                    file_name=f"{title}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
                
                # Limpa arquivos temporários
                try:
                    os.remove(filename)
                    os.rmdir(temp_dir)
                except:
                    pass
                    
            else:
                if isinstance(title, str) and title.startswith("ERROR"):
                    error_msg = title
                else:
                    error_msg = "Erro desconhecido durante o download"
                
                if "Video unavailable" in error_msg:
                    st.error("❌ Vídeo não disponível, privado ou removido.")
                elif "No video formats" in error_msg:
                    st.error("❌ Formato de vídeo não encontrado. Tente uma qualidade diferente.")
                else:
                    st.error(f"❌ Erro no download: {error_msg}")
    
    # Rodapé com informações
    st.markdown("---")
    with st.expander("ℹ️ Informações e Ajuda"):
        st.markdown("""
        **Como usar:**
        1. Cole a URL completa do vídeo do YouTube
        2. Escolha a qualidade desejada
        3. Clique em "Baixar Vídeo"
        4. Aguarde o processamento
        5. Clique no botão de download que aparecerá
        
        **Qualidades disponíveis:**
        - **HD 720p**: Boa qualidade, arquivo médio
        - **Full HD 1080p**: Alta qualidade, arquivo maior
        - **Melhor qualidade**: Máxima qualidade disponível
        - **Menor arquivo**: Qualidade reduzida, economia de espaço
        
        **Formatos suportados:**
        - A aplicação prioriza downloads em formato MP4
        - Compatível com a maioria dos vídeos públicos do YouTube
        
        **Observações:**
        - Vídeos muito longos podem demorar mais para processar
        - Vídeos privados ou removidos não podem ser baixados
        - A velocidade depende da sua conexão com a internet
        """)

if __name__ == "__main__":
    main()
