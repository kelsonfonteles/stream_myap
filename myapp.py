import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
from PIL import Image
from pyzbar.pyzbar import decode

# Variáveis para armazenar os dados do formulário
codigo_barras = ""
campo2 = ""
campo3 = ""
campo4 = ""
campo5 = ""

# Define uma classe para processar o vídeo da webcam
class BarcodeReader(VideoProcessorBase):
    def __init__(self):
        self.is_streaming = False

    def recv(self, frame):
        if not self.is_streaming:
            self.is_streaming = True
            return

        # Converte o quadro em uma imagem PIL
        pil_image = Image.fromarray(frame)

        # Tenta decodificar o código de barras da imagem
        decoded_objects = decode(pil_image)

        # Se um código de barras for encontrado, extraia seus dados
        for obj in decoded_objects:
            global codigo_barras
            codigo_barras = obj.data.decode('utf-8')
            st.write("Código de Barras Detectado:", codigo_barras)

            # Mostra o quadro com o código de barras destacado
            st.image(pil_image)

# Função principal para o aplicativo Streamlit
def main():
    st.title("Formulário para Smartphone")

    # Iniciar o streaming da webcam e chamar o processador de vídeo para ler o código de barras
    webrtc_streamer(key="barcode", video_processor_factory=BarcodeReader, mode=WebRtcMode.SENDRECV)

    # Campos restantes do formulário
    global campo2, campo3, campo4, campo5
    campo2 = st.text_input("Campo 2")
    campo3 = st.text_input("Campo 3")
    campo4 = st.text_input("Campo 4")
    campo5 = st.text_input("Campo 5")

    # Botão para enviar os dados
    if st.button("Enviar"):
        st.success("Dados do formulário enviados com sucesso!")

if __name__ == "__main__":
    main()
