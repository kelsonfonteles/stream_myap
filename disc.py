import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psycopg2
from psycopg2 import sql

# Configurações do servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587
gmail_user = 'dataresender@gmail.com'
gmail_password = 'mdzdcqyclzuhnpan'

# Função para enviar e-mail
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

# Função para inserir os dados no banco de dados
def inserir_dados_bd(nome, telefone, email, perfil, definicao, areas, combinacao, caracteristicas, perfil_equipe, motivadores, limitantes, desenvolvimento):
    db_params = {
        'dbname': 'defaultdb',
        'user': 'avnadmin',
        'password': 'AVNS_OV0tPMSnWRwf4C_zqgv',
        'host': 'pg-1598f41b-aecaged.k.aivencloud.com',
        'port': 26498  # Porta do banco de dados
    }

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO trusted_zone.disc 
            (nome_completo, telefone, email, spcp, dpi, sat, cf, pc, pet, mtv, pl, od) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        cursor.execute(insert_query, (nome, telefone, email, perfil, definicao, areas, combinacao, caracteristicas, perfil_equipe, motivadores, limitantes, desenvolvimento))

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Dados inseridos no banco de dados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inserir dados no banco de dados: {e}")

# Função para obter as definições do perfil DISC
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
            "cf": "Decisões rápidas, busca por desafios, foco em resultados.",
            "pc": "Determinado, assertivo, independente.",
            "pet": "Prefere liderar, tomar decisões e resolver problemas.",
            "mtv": "Resultados, metas claras, liberdade de ação.",
            "pl": "Tendência a ser impaciente ou autoritário em certas situações.",
            "od": "Desenvolver paciência e melhorar a escuta ativa."
        },
        "Influência": {
            "cf": "Facilidade de comunicação, desejo de influenciar e interagir.",
            "pc": "Comunicativo, persuasivo, sociável.",
            "pet": "Trabalha bem em equipe e motiva os outros ao seu redor.",
            "mtv": "Reconhecimento, interação social, ambiente positivo.",
            "pl": "Tendência a perder o foco ou evitar conflitos.",
            "od": "Aprender a lidar com críticas e desenvolver foco em resultados."
        },
        "Estabilidade": {
            "cf": "Desejo por harmonia e consistência em ambientes tranquilos.",
            "pc": "Paciente, confiável, persistente.",
            "pet": "Oferece suporte, mantém a estabilidade e evita conflitos.",
            "mtv": "Ambientes estáveis, segurança e relacionamentos de confiança.",
            "pl": "Resistência a mudanças rápidas ou inesperadas.",
            "od": "Trabalhar a adaptabilidade e assumir mais riscos calculados."
        },
        "Conformidade": {
            "cf": "Atenção aos detalhes, foco em qualidade e seguir normas.",
            "pc": "Detalhista, organizado, preciso.",
            "pet": "Prefere seguir regras, garantindo qualidade e conformidade.",
            "mtv": "Padrões claros, regras definidas e segurança.",
            "pl": "Excesso de crítica a si mesmo ou aos outros, dificuldade em lidar com incertezas.",
            "od": "Desenvolver flexibilidade e lidar melhor com situações ambíguas."
        }
    }
    return informacoes[perfil]

# Função principal do teste DISC
def teste_disc():
    st.title("Teste DISC")

    # Formulário para inserir os dados do usuário
    st.write("Por favor, preencha o formulário abaixo.")
    nome_completo = st.text_input("Nome Completo")
    telefone = st.text_input("Telefone Whatsapp", placeholder="(xx)xxxxx-xxxx")
    email = st.text_input("Email")

    if not nome_completo or not telefone or not email:
        st.warning("Por favor, preencha todos os campos.")
        return

    # Perguntas do teste DISC
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

        perfis = {
            "Dominância": dominancia,
            "Influência": influencia,
            "Estabilidade": estabilidade,
            "Conformidade": conformidade
        }

        perfil_predominante = max(perfis, key=perfis.get)
        st.write(f"Seu perfil comportamental predominante é: {perfil_predominante}")

        definicao, areas_sugeridas = obter_definicoes_perfil(perfil_predominante)
        info_adicional = obter_info_adicional(perfil_predominante)

        st.write(f"**Definição do perfil {perfil_predominante}:** {definicao}")
        st.write(f"**Sugestão de áreas de trabalho:** {areas_sugeridas}")
        st.write(f"**Combinação de Fatores:** {info_adicional['cf']}")
        st.write(f"**Principais Características:** {info_adicional['pc']}")
        st.write(f"**Perfil em Equipe e no Trabalho:** {info_adicional['pet']}")
        st.write(f"**Motivadores:** {info_adicional['mtv']}")
        st.write(f"**Pontos Limitantes:** {info_adicional['pl']}")
        st.write(f"**Oportunidades de Desenvolvimento:** {info_adicional['od']}")

        # Enviar e-mail com o resultado
        corpo_email = f"""
        <p>Olá {nome_completo},</p>
        <p>Seu perfil comportamental predominante é: <strong>{perfil_predominante}</strong></p>
        <p><strong>Definição do perfil {perfil_predominante}:</strong> {definicao}</p>
        <p><strong>Sugestão de áreas de trabalho:</strong> {areas_sugeridas}</p>
        <p><strong>Combinação de Fatores:</strong> {info_adicional['cf']}</p>
        <p><strong>Principais Características:</strong> {info_adicional['pc']}</p>
        <p><strong>Perfil em Equipe e no Trabalho:</strong> {info_adicional['pet']}</p>
        <p><strong>Motivadores:</strong> {info_adicional['mtv']}</p>
        <p><strong>Pontos Limitantes:</strong> {info_adicional['pl']}</p>
        <p><strong>Oportunidades de Desenvolvimento:</strong> {info_adicional['od']}</p>
        """
        enviar_email(email, "Resultado do Teste DISC", corpo_email)

        # Inserir os dados no banco de dados
        inserir_dados_bd(nome_completo, telefone, email, perfil_predominante, definicao, areas_sugeridas, 
                         info_adicional['cf'], info_adicional['pc'], info_adicional['pet'], 
                         info_adicional['mtv'], info_adicional['pl'], info_adicional['od'])

if __name__ == "__main__":
    teste_disc()
