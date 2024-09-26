import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
gmail_user = 'dataresender@gmail.com'
gmail_password = 'mdzdcqyclzuhnpan'

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'html'))

    # Enviar o e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, destinatario, msg.as_string())
        server.quit()
        st.success('E-mail enviado com sucesso!')
    except Exception as e:
        st.error(f'Erro ao enviar e-mail: {e}')

def obter_definicoes_perfil(perfil):
    definicoes = {
        "Dominância": ("Pessoas com alta dominância tendem a ser diretas, objetivas e gostam de ter controle. Elas preferem tomar decisões rápidas e enfrentar desafios.", 
                       "Áreas sugeridas: Gestão de projetos, liderança, empreendedorismo, vendas."),
        "Influência": ("Pessoas com alta influência são comunicativas, sociáveis e gostam de persuadir e influenciar os outros. Elas têm facilidade em trabalhar em equipe e em ambientes dinâmicos.", 
                       "Áreas sugeridas: Vendas, marketing, relações públicas, recursos humanos."),
        "Estabilidade": ("Pessoas com alta estabilidade valorizam a harmonia, paciência e são excelentes em manter ambientes de trabalho tranquilos e organizados. Elas são confiáveis e consistentes.", 
                         "Áreas sugeridas: Atendimento ao cliente, gestão de processos, suporte técnico, administrativo."),
        "Conformidade": ("Pessoas com alta conformidade são detalhistas, analíticas e seguem regras e padrões rigorosos. Elas preferem ambientes organizados e bem estruturados.", 
                         "Áreas sugeridas: Contabilidade, controle de qualidade, auditoria, engenharia.")
    }
    return definicoes[perfil]

def teste_disc():
    st.title("Teste DISC")

    # Formulário para inserir o e-mail
    st.write("Por favor, preencha o formulário abaixo com seu e-mail para receber o resultado.")
    email = st.text_input("Digite seu e-mail para receber o resultado:")

    # Perguntas do teste
    respostas = []
    perguntas = [
        ("Eu gosto de desafios e me sinto confortável ao tomar decisões rápidas.", "dominancia"),
        ("Eu sou uma pessoa extrovertida e gosto de conversar e influenciar outras pessoas.", "influencia"),
        ("Eu prefiro ambientes estáveis e com menos mudanças repentinas.", "estabilidade"),
        ("Eu sou uma pessoa analítica e gosto de seguir regras e procedimentos.", "conformidade"),
        
        # Bloco adicional de perguntas
        ("Eu sou motivado por resultados e metas claras.", "dominancia"),
        ("Eu gosto de ser reconhecido pelo meu trabalho e desempenho.", "influencia"),
        ("Eu valorizo a harmonia e cooperação no ambiente de trabalho.", "estabilidade"),
        ("Eu prezo pela precisão e pela qualidade em tudo que faço.", "conformidade"),

        # Outro bloco adicional de perguntas
        ("Eu tomo decisões rápidas, mesmo em situações de pressão.", "dominancia"),
        ("Eu tenho facilidade em influenciar e persuadir os outros.", "influencia"),
        ("Eu prefiro evitar conflitos e sou paciente em lidar com outras pessoas.", "estabilidade"),
        ("Eu sigo regras e sou detalhista em tudo que faço.", "conformidade"),
        
        # Novas perguntas (10 blocos adicionais)
        ("Eu gosto de ter o controle das situações.", "dominancia"),
        ("Eu gosto de interagir com novas pessoas.", "influencia"),
        ("Eu valorizo a segurança e a previsibilidade.", "estabilidade"),
        ("Eu sou meticuloso em relação a detalhes.", "conformidade"),
        ("Eu tomo iniciativa em projetos e tarefas.", "dominancia"),
        ("Eu tenho facilidade em motivar as pessoas.", "influencia"),
        ("Eu sou persistente e determinado.", "estabilidade"),
        ("Eu sigo padrões e regras com rigor.", "conformidade"),
        ("Eu gosto de desafios complexos.", "dominancia"),
        ("Eu me adapto bem a mudanças sociais.", "influencia")
    ]

    # Loop pelas perguntas, mostrando apenas o texto da pergunta
    for pergunta, perfil in perguntas:
        resposta = st.radio(pergunta, ['Discordo totalmente', 'Discordo', 'Concordo', 'Concordo totalmente'])
        respostas.append(resposta)

    if st.button("Ver resultado"):
        # Processamento das respostas
        dominancia = respostas.count('Concordo totalmente')
        influencia = respostas.count('Concordo')
        estabilidade = respostas.count('Discordo')
        conformidade = respostas.count('Discordo totalmente')

        # Cria um dicionário com as pontuações dos perfis
        perfis = {
            "Dominância": dominancia,
            "Influência": influencia,
            "Estabilidade": estabilidade,
            "Conformidade": conformidade
        }

        # Exibir o perfil com a maior pontuação
        perfil_predominante = max(perfis, key=perfis.get)
        st.write(f"Seu perfil comportamental predominante é: {perfil_predominante}")

        # Obter a definição e área de trabalho sugerida para o perfil predominante
        definicao, areas_sugeridas = obter_definicoes_perfil(perfil_predominante)
        st.write(f"**Definição do perfil {perfil_predominante}:** {definicao}")
        st.write(f"**Sugestão de áreas de trabalho:** {areas_sugeridas}")

        # Enviar resultado por e-mail se o campo de e-mail estiver preenchido
        if email:
            corpo_email = f"""
            <html>
                <body>
                    <h2>Resultado do Teste DISC</h2>
                    <p>Seu perfil comportamental predominante é: <strong>{perfil_predominante}</strong></p>
                    <p><strong>Definição do perfil {perfil_predominante}:</strong> {definicao}</p>
                    <p><strong>Sugestão de áreas de trabalho:</strong> {areas_sugeridas}</p>
                    <p><strong>Pontuações:</strong></p>
                    <ul>
                        <li>Dominância: {dominancia}</li>
                        <li>Influência: {influencia}</li>
                        <li>Estabilidade: {estabilidade}</li>
                        <li>Conformidade: {conformidade}</li>
                    </ul>
                </body>
            </html>
            """
            enviar_email(email, "Resultado do Teste DISC", corpo_email)

if __name__ == "__main__":
    teste_disc()
