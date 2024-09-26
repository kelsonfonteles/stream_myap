


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

def obter_info_adicional(perfil):
    informacoes = {
        "Dominância": {
            "Combinação de Fatores": "Decisões rápidas, busca por desafios, foco em resultados.",
            "Principais Características": "Determinado, assertivo, independente.",
            "Perfil em Equipe e no Trabalho": "Prefere liderar, tomar decisões e resolver problemas.",
            "Motivadores": "Resultados, metas claras, liberdade de ação.",
            "Pontos Limitantes": "Tendência a ser impaciente ou autoritário em certas situações.",
            "Oportunidades de Desenvolvimento": "Desenvolver paciência e melhorar a escuta ativa."
        },
        "Influência": {
            "Combinação de Fatores": "Facilidade de comunicação, desejo de influenciar e interagir.",
            "Principais Características": "Comunicativo, persuasivo, sociável.",
            "Perfil em Equipe e no Trabalho": "Trabalha bem em equipe e motiva os outros ao seu redor.",
            "Motivadores": "Reconhecimento, interação social, ambiente positivo.",
            "Pontos Limitantes": "Tendência a perder o foco ou evitar conflitos.",
            "Oportunidades de Desenvolvimento": "Aprender a lidar com críticas e desenvolver foco em resultados."
        },
        "Estabilidade": {
            "Combinação de Fatores": "Desejo por harmonia e consistência em ambientes tranquilos.",
            "Principais Características": "Paciente, confiável, persistente.",
            "Perfil em Equipe e no Trabalho": "Oferece suporte, mantém a estabilidade e evita conflitos.",
            "Motivadores": "Ambientes estáveis, segurança e relacionamentos de confiança.",
            "Pontos Limitantes": "Resistência a mudanças rápidas ou inesperadas.",
            "Oportunidades de Desenvolvimento": "Trabalhar a adaptabilidade e assumir mais riscos calculados."
        },
        "Conformidade": {
            "Combinação de Fatores": "Atenção aos detalhes, foco em qualidade e seguir normas.",
            "Principais Características": "Detalhista, organizado, preciso.",
            "Perfil em Equipe e no Trabalho": "Prefere seguir regras, garantindo qualidade e conformidade.",
            "Motivadores": "Padrões claros, regras definidas e segurança.",
            "Pontos Limitantes": "Excesso de crítica a si mesmo ou aos outros, dificuldade em lidar com incertezas.",
            "Oportunidades de Desenvolvimento": "Desenvolver flexibilidade e lidar melhor com situações ambíguas."
        }
    }
    return informacoes[perfil]

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

    # Loop pelas perguntas
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

        # Obter a definição e áreas sugeridas
        definicao, areas_sugeridas = obter_definicoes_perfil(perfil_predominante)
        st.write(f"**Definição do perfil {perfil_predominante}:** {definicao}")
        st.write(f"**Sugestão de áreas de trabalho:** {areas_sugeridas}")

        # Obter informações adicionais do perfil
        info_adicional = obter_info_adicional(perfil_predominante)
        for chave, valor in info_adicional.items():
            st.write(f"**{chave}:** {valor}")

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
                    <p><strong>Informações adicionais:</strong></p>
                    <ul>
            """
            for chave, valor in info_adicional.items():
                corpo_email += f"<li><strong>{chave}:</strong> {valor}</li>"

            corpo_email += """
                    </ul>
                </body>
            </html>
            """
            enviar_email(email, "Resultado do Teste DISC", corpo_email)

if __name__ == "__main__":
    teste_disc()
