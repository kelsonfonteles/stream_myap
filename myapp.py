import streamlit as st
import mysql.connector
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode
from PIL import Image
from pyzbar.pyzbar import decode

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="seu_host",
    user="seu_usuario",
    password="sua_senha",
    database="seu_banco_de_dados"
)
cursor = conn.cursor()

# Função para criar tabela se não existir
def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS formulario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo_barras VARCHAR(255),
                    campo2 VARCHAR(255),
                    campo3 VARCHAR(255),
                    campo4 VARCHAR(255),
                    campo5 VARCHAR(255))''')

# Função para inserir dados no banco de dados
def insert_data(codigo_barras, campo2, campo3, campo4, campo5):
    cursor.execute('''INSERT INTO formulario (codigo_barras, campo2, campo3, campo4, campo5) 
                   VALUES (%s, %s, %s, %s, %s)''', (codigo_barras, campo2, campo3, campo4, campo5))
    conn.commit()

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
            barcode_data = obj.data.decode('utf-8')
            st.write("Código de Barras Detectado:", barcode_data)

            # Mostra o quadro com o código de barras destacado
            st.image(pil_image)

# Função principal para o aplicativo Streamlit
def main():
    st.title("Formulário para Smartphone")

    # Iniciar o streaming da webcam e chamar o processador de vídeo para ler o código de barras
    webrtc_streamer(key="barcode", video_processor_factory=BarcodeReader, mode=WebRtcMode.SENDRECV)

    # Campos restantes do formulário
    campo2 = st.text_input("Campo 2")
    campo3 = st.text_input("Campo 3")
    campo4 = st.text_input("Campo 4")
    campo5 = st.text_input("Campo 5")

    # Botão para enviar os dados
    if st.button("Enviar"):
        # Substitua 'barcode_data' pela variável que contém o código de barras lido
        insert_data(barcode_data, campo2, campo3, campo4, campo5)
        st.success("Dados enviados com sucesso!")

if __name__ == "__main__":
    create_table()
    main()
