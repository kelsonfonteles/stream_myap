import streamlit as st
import cv2
from pyzbar import pyzbar

# Função para decodificar códigos de barras
def decode_barcode(frame):
    # Convertendo a imagem para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Localizando códigos de barras na imagem
    barcodes = pyzbar.decode(gray)
    # Iterando sobre os códigos de barras encontrados
    for barcode in barcodes:
        # Obtendo as coordenadas do código de barras
        (x, y, w, h) = barcode.rect
        # Desenhando uma caixa delimitadora ao redor do código de barras
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Decodificando os dados do código de barras
        barcode_data = barcode.data.decode("utf-8")
        # Desenhando o texto com os dados do código de barras na imagem
        cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Adicionando os dados do código de barras à lista de resultados
        if barcode_data not in detected_barcodes:
            detected_barcodes.append(barcode_data)
    return frame

# Configurando a página do Streamlit
st.set_page_config(layout="wide")

# Inicializando a lista de resultados dos códigos de barras detectados
detected_barcodes = []

# Título da aplicação
st.title("Leitor de Código de Barras")

# Instrução para o usuário
st.write("Aponte a câmera para um código de barras.")

# Inicializando a câmera
video_capture = cv2.VideoCapture(0)

# Loop para capturar e exibir vídeo da câmera
while True:
    # Capturando frame da câmera
    ret, frame = video_capture.read()
    if not ret:
        break
    
    # Decodificando códigos de barras
    frame = decode_barcode(frame)
    
    # Exibindo o frame na interface do Streamlit
    st.image(frame, channels="BGR", use_column_width=True)
    
    # Exibindo os resultados dos códigos de barras detectados
    if detected_barcodes:
        st.write("Códigos de barras detectados:")
        for barcode in detected_barcodes:
            st.write(barcode)
    
    # Verificando se o usuário deseja encerrar a aplicação
    if st.button("Encerrar"):
        break

# Liberando a câmera
video_capture.release()
