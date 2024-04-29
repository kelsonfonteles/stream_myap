import streamlit as st

# Função principal para o aplicativo Streamlit
def main():
    st.title("Formulário para Smartphone")

    # Ajusta o layout para uma visualização otimizada em smartphones
    st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Campos do formulário
    campo1 = st.text_input("Campo 1")
    campo2 = st.text_input("Campo 2")
    campo3 = st.text_input("Campo 3")
    campo4 = st.text_input("Campo 4")
    campo5 = st.text_input("Campo 5")

    # Botão para enviar os dados
    if st.button("Enviar"):
        # Aqui você pode adicionar a lógica para lidar com os dados do formulário
        st.success("Dados do formulário enviados com sucesso!")

if __name__ == "__main__":
    main()
