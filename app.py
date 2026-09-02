# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# Configurações de página (Fontes, Estilos, Sem menu lateral)
st.set_page_config(
    page_title="Recuperação de Química - 3º Ano Ensino Médio",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização Arial e remoção do menu padrão do Streamlit
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Arial', sans-serif !important;
        }
        /* Esconder botão do menu lateral padrão e barra de ferramentas */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 800px;
        }
    </style>
""", unsafe_allow_html=True)

# Banco de dados de questões grounded nas fontes (Módulo 17 PEQ e Gabriel Cabral)
BANCO_QUESTOES = [
    {
        "id": 1,
        "funcao": "Álcool",
        "pergunta": "O Etanol (combustível automotivo e solvente) possui fórmula estrutural **H₃C-CH₂-OH**. Identifique a função orgânica deste composto caracterizado pelo grupo hidroxila (-OH) ligado diretamente a um carbono saturado (carbono de alcano que realiza apenas ligações simples):",
        "alternativas": ["Álcool", "Fenol", "Aldeído", "Cetona", "Ácido Carboxílico", "Éster"],
        "correta": "Álcool"
    },
    {
        "id": 2,
        "funcao": "Fenol",
        "pergunta": "A Dopamina (neurotransmissor do prazer) e o Paracetamol (analgésico clássico) possuem em sua estrutura um ou mais anéis aromáticos (benzeno) com hidroxilas ligadas diretamente a carbonos insaturados do anel aromático (**Ar-OH**). De acordo com as diretrizes e regras ensinadas por Cabral e o Módulo 17, esses anéis fenólicos pertencem à função:",
        "alternativas": ["Álcool", "Fenol", "Amida", "Éter", "Ácido Carboxílico", "Éster"],
        "correta": "Fenol"
    },
    {
        "id": 3,
        "funcao": "Aldeído",
        "pergunta": "O Metanal (comumente chamado de formaldeído) apresenta um grupo carbonila terminal na ponta de sua cadeia carbônica (**C=O na ponta**, acoplado ao hidrogênio, muitas vezes condensado como -CHO). Identifique a função química deste composto:",
        "alternativas": ["Álcool", "Cetona", "Aldeído", "Éter", "Ácido Carboxílico", "Éster"],
        "correta": "Aldeído"
    },
    {
        "id": 4,
        "funcao": "Cetona",
        "pergunta": "A Propanona (composto químico clássico de aplicação como removedor de esmalte de unhas) apresenta uma carbonila posicionada entre carbonos (**C=O entre dois carbonos**, caráter intermediário). Identifique o grupo funcional deste composto:",
        "alternativas": ["Álcool", "Cetona", "Aldeído", "Éter", "Ácido Carboxílico", "Éster"],
        "correta": "Cetona"
    },
    {
        "id": 5,
        "funcao": "Ácido Carboxílico",
        "pergunta": "O Ácido Carboxílico apresenta o grupo funcional carboxila, decorrente da união de uma carbonila com uma hidroxila no mesmo carbono (**-COOH**). Um exemplo cotidiano clássico é o Ácido Acético (composto do vinagre). Qual é o grupo funcional correspondente?",
        "alternativas": ["Álcool", "Aldeído", "Éster", "Éter", "Ácido Carboxílico", "Cetona"],
        "correta": "Ácido Carboxílico"
    },
    {
        "id": 6,
        "funcao": "Éster",
        "pergunta": "O Etanoato de Isoamila é um éster flavorizante sintético utilizado pela indústria alimentícia para imitar o odor e o aroma de banana em chicletes e guloseimas. Ele é derivado de ácidos carboxílicos, onde a carboxila apresenta o oxigênio intermediário acoplado a outra cadeia carbônica (**R-COO-R'**). Classifique a função:",
        "alternativas": ["Éter", "Éster", "Cetona", "Ácido Carboxílico", "Álcool", "Amida"],
        "correta": "Éster"
    },
    {
        "id": 7,
        "funcao": "Éter",
        "pergunta": "O composto anestésico Etóxietano (conhecido historicamente como éter etílico) possui um oxigênio ligado de forma simples a dois radicais de carbono, deixando a cadeia heterogênea (**R-O-R'**). De acordo com a videoaula de Cabral, esta função apresenta o 'heteroátomo de oxigênio eternamente sozinho entre carbonos'. Classifique-a:",
        "alternativas": ["Álcool", "Aldeído", "Éter", "Éster", "Cetona", "Ácido Carboxílico"],
        "correta": "Éter"
    },
    {
        "id": 8,
        "funcao": "Amina",
        "pergunta": "A Metilamina é um gás altamente solúvel em água, formado na decomposição de carnes de peixes, responsável por aquele odor forte característico. Trata-se do grupo funcional que confere o maior caráter básico na química orgânica, derivado direto da substituição de hidrogênios da amônia (**R-NH₂**). Classifique-a:",
        "alternativas": ["Amina", "Amida", "Nitrocomposto", "Álcool", "Fenol", "Éster"],
        "correta": "Amina"
    },
    {
        "id": 9,
        "funcao": "Amida",
        "pergunta": "A Acrilamida é uma substância tóxica gerada durante o preparo de batatas fritas industriais. De acordo com o Módulo 17 e as diretrizes de Cabral, as amidas apresentam uma carbonila ligada diretamente ao nitrogênio (**C=O acoplado ao N**). Identifique a função correspondente:",
        "alternativas": ["Amina", "Amida", "Nitrocomposto", "Nitrila", "Ácido Carboxílico", "Éster"],
        "correta": "Amida"
    },
    {
        "id": 10,
        "funcao": "Haleto Orgânico",
        "pergunta": "O Cloreto de Etila (monocloroetano) é um haleto sintético utilizado como anestésico local por congelamento da pele em práticas desportivas. Apresenta o átomo de Cloro ligado a carbono saturado (**R-Cl**). Identifique a função orgânica correspondente a esse composto halogênico:",
        "alternativas": ["Haleto Orgânico", "Éter", "Éster", "Cetona", "Álcool", "Ácido Carboxílico"],
        "correta": "Haleto Orgânico"
    }
]

# Inicialização do Banco de Notas Simulado em Session State
if "historico_notas" not in st.session_state:
    st.session_state["historico_notas"] = []

if "etapa" not in st.session_state:
    st.session_state["etapa"] = "identificacao"

if "aluno" not in st.session_state:
    st.session_state["aluno"] = {"nome": "", "turma": "", "inicio": 0, "questoes": []}

# Função de Navegação
def mudar_etapa(nova_etapa):
    st.session_state["etapa"] = nova_etapa
    st.rerun()

# --- TELA 1: IDENTIFICAÇÃO ---
if st.session_state["etapa"] == "identificacao":
    st.image("https://contribution.usercontent.google.com/download?c=Cgpub3RlYm9va2xtEkASCWFydGlmYWN0cxozCiQ4NDAzYTZmZC04M2RmLTQ4ZmMtYWYyOS1hYzA0YjY1OTg0OWESCxIHEJW8iv-AGBgB&filename=projeto_recuperacao_quimica.pdf&opi=96797242", use_container_width=True, caption="Setor Ômega - Ensino Médio")
    
    st.markdown("""
        <div style='background-color:#0f766e; padding:1.5rem; border-radius:8px; color:white; margin-bottom:2rem;'>
            <h1 style='margin:0; font-size:22px; font-weight:bold;'>🧪 Recuperação de Química</h1>
            <p style='margin:5px 0 0 0; font-size:14px; opacity:0.9;'>3º Ano Ensino Médio - Reconhecimento de Funções Orgânicas</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Identificação do Aluno")
    st.write("Preencha os campos obrigatórios abaixo para iniciar sua prova de recuperação de Química.")

    nome = st.text_input("Nome Completo:", placeholder="Ex: Ana Silva Costa").strip()
    turma = st.selectbox("Sua Turma:", ["", "3º Ano A", "3º Ano B", "3º Ano C", "3º Ano D"], format_func=lambda x: "Selecione..." if x == "" else x)

    # Bloqueio Anticola (Nome duplicado)
    ja_fez = False
    for r in st.session_state["historico_notas"]:
        if r["nome"].lower() == nome.lower() and r["turma"] == turma:
            ja_fez = True
            break

    if st.button("Iniciar Atividade de Recuperação", use_container_width=True):
        if not nome or not turma:
            st.error("⚠️ Por favor, digite seu nome e escolha sua turma!")
        elif ja_fez:
            st.error("⚠️ Erro Anticola: Esse aluno já realizou o teste anteriormente! Novas tentativas estão bloqueadas para o mesmo dispositivo/nome.")
        else:
            # Sorteia as questões
            questoes_copia = BANCO_QUESTOES.copy()
            random.shuffle(questoes_copia)
            
            st.session_state["aluno"] = {
                "nome": nome,
                "turma": turma,
                "inicio": time.time(),
                "questoes": questoes_copia
            }
            mudar_etapa("video")

# --- TELA 2: ESTUDO (VÍDEO) ---
elif st.session_state["etapa"] == "video":
    st.markdown("""
        <div style='background-color:#0f766e; padding:1rem; border-radius:8px; color:white; margin-bottom:1.5rem;'>
            <h2 style='margin:0; font-size:18px; font-weight:bold;'>Etapa 1: Revisão Teórica Orientada</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"Olá **{st.session_state['aluno']['nome']}**! Assista ao vídeo explicativo do **Professor Gabriel Cabral** antes de iniciar o questionário de 10 perguntas. Preste atenção nas dicas de identificação rápida de oxigenados e nitrogenados!")
    
    # Video aula do Youtube incorporada
    st.video("https://www.youtube.com/watch?v=6_rU9IeD_6g")

    st.info("""
    **📌 Macetes Curriculares rápidos das Fontes:**
    - **Álcool:** Hidroxila (-OH) acoplada diretamente a carbono saturado.
    - **Fenol:** Hidroxila (-OH) ligada diretamente a anel aromático (benzeno). Apresenta caráter ácido pronunciado.
    - **Aldeído:** Carbonila na ponta da cadeia terminal (-CHO).
    - **Cetona:** Carbonila intermediária (C=O entre dois carbonos).
    - **Ácido Carboxílico:** Carboxila terminal (-COOH).
    - **Éster:** Grupo flavorizante (-CooC-).
    - **Amina:** Grupo básico nitrogenado derivado da amônia (R-NH2).
    - **Amida:** Carbonila colada ao nitrogênio (C=O ligado diretamente ao N).
    """)

    if st.button("Estudei! Iniciar Questionário de Avaliação", use_container_width=True):
        mudar_etapa("prova")

# --- TELA 3: PROVA ---
elif st.session_state["etapa"] == "prova":
    st.markdown("""
        <div style='background-color:#0f766e; padding:1rem; border-radius:8px; color:white; margin-bottom:1.5rem;'>
            <h2 style='margin:0; font-size:18px; font-weight:bold;'>Etapa 2: Exame de Recuperação</h2>
            <p style='margin:2px 0 0 0; font-size:12px; opacity:0.9;'>Identifique a função orgânica de cada um dos compostos químicos reais das fontes.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**Estudante:** {st.session_state['aluno']['nome']} ({st.session_state['aluno']['turma']})")
    
    respostas_aluno = {}
    
    # Exibir questões de forma randômica
    for i, q in enumerate(st.session_state["aluno"]["questoes"]):
        st.markdown(f"**Questão {i+1})** {q['pergunta']}")
        
        # Embaralha as alternativas de forma fixa por sessão para evitar colar
        alternativas = q["alternativas"].copy()
        
        # Oferece as 6 opções de resposta
        respostas_aluno[q["id"]] = st.radio(
            f"Selecione uma resposta para a Questão {i+1}:", 
            alternativas, 
            index=None,
            key=f"q_{q['id']}"
        )
        st.markdown("---")

    if st.button("Finalizar e Enviar Atividade de Recuperação", use_container_width=True):
        # Validação se respondeu todas
        total_respondido = sum(1 for r in respostas_aluno.values() if r is not None)
        if total_respondido < 10:
            st.error("⚠️ Responda todas as 10 questões antes de enviar!")
        else:
            # Corrige a prova
            acertos = 0
            detalhes = []
            for q in st.session_state["aluno"]["questoes"]:
                resp = respostas_aluno[q["id"]]
                correta = q["correta"]
                is_correto = resp == correta
                if is_correto:
                    acertos += 1
                detalhes.append({
                    "funcao": q["funcao"],
                    "resposta": resp,
                    "correta": correta,
                    "resultado": "Acerto" if is_correto else "Erro"
                })
            
            tempo_gasto = round((time.time() - st.session_state["aluno"]["inicio"]) / 60)
            tempo_texto = f"{tempo_gasto} min" if tempo_gasto > 0 else "Menos de 1 min"
            status = "RECUPERADO" if acertos >= 7 else "NÃO RECUPERADO"
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            codigo = "REC" + str(random.randint(100000, 999999))

            # Grava no banco local
            registro = {
                "id": codigo,
                "nome": st.session_state["aluno"]["nome"],
                "turma": st.session_state["aluno"]["turma"],
                "nota": acertos,
                "status": status,
                "tempo": tempo_texto,
                "data Hora": data_hora,
                "detalhes": detalhes
            }
            st.session_state["historico_notas"].append(registro)
            st.session_state["aluno"]["resultado_final"] = registro
            mudar_etapa("resultado")

# --- TELA 4: RESULTADO INDIVIDUAL ---
elif st.session_state["etapa"] == "resultado":
    res = st.session_state["aluno"]["resultado_final"]
    
    if res["nota"] >= 7:
        st.balloons()
        st.success(f"🎉 Parabéns, {res['nome']}! Você alcançou a nota necessária para recuperação!")
    else:
        st.error(f"📚 Estude um pouco mais, {res['nome']}! Você obteve {res['nota']}/10 e precisa de pelo menos 7 acertos para a recuperação.")
        
    st.subheader("📋 Comprovante de Realização")
    st.write(f"**Estudante:** {res['nome']}")
    st.write(f"**Turma:** {res['turma']}")
    st.write(f"**Nota Final:** **{res['nota']}/10**")
    st.write(f"**Status:** **{res['status']}**")
    st.write(f"**Tempo Gasto:** {res['tempo']}")
    st.write(f"**Código de Segurança:** `{res['id']}`")
    st.write(f"**Data e Hora:** {res['data Hora']}")
    
    st.markdown("---")
    st.info("🚨 O seu computador registrou esta prova de recuperação. Novas tentativas estão bloqueadas nesta máquina.")
    
    if st.button("Fazer Logoff (Sair)", use_container_width=True):
        st.session_state["etapa"] = "identificacao"
        st.rerun()

# --- PORTAL DO PROFESSOR (LINK DISCRETO) ---
st.markdown("--- ")
with st.expander("🔑 Portal do Professor (Privado)"):
    st.write("Acesso reservado ao docente de Química para monitoramento de notas e auditoria de gabaritos.")
    senha = st.text_input("Senha do Portal:", type="password", key="senha_docente")
    
    if senha == "quimica2026":
        st.success("Acesso concedido!")
        
        hist = st.session_state["historico_notas"]
        
        if len(hist) == 0:
            st.info("Aguardando a realização dos primeiros testes pelos alunos de Química.")
        else:
            # Métricas
            df = pd.DataFrame(hist)
            df_display = df[["id", "data Hora", "nome", "turma", "nota", "status", "tempo"]].copy()
            df_display.columns = ["ID", "Data e Hora", "Estudante", "Turma", "Nota Final", "Status", "Tempo Gasto"]
            
            st.subheader("📊 Estatísticas Gerais")
            c1, c2, col3, c4 = st.columns(4)
            c1.metric("Alunos Avaliados", len(df))
            c2.metric("Alunos Recuperados", len(df[df['nota'] >= 7]))
            col3.metric("Alunos Reprovados", len(df[df['nota'] < 7]))
            c4.metric("Média Geral da Turma", f"{df['nota'].mean():.1f}/10")
            
            st.subheader("📋 Tabela Consolidada de Notas")
            st.dataframe(df_display, use_container_width=True)
            
            # Exportador CSV direto do Python (perfeito!)
            csv_data = df_display.to_csv(index=False, sep=";").encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Notas em Formato Excel (CSV)",
                data=csv_data,
                file_name="notas_recuperacao_quimica_3ano.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Ver detalhes das respostas de cada um (auditoria)
            st.subheader("🔎 Auditoria de Respostas por Aluno")
            aluno_sel = st.selectbox("Selecione um aluno para auditar:", df["nome"].tolist())
            aluno_dados = df[df["nome"] == aluno_sel].iloc[0]
            
            st.write(f"**Estudante:** {aluno_dados['nome']} | **Turma:** {aluno_dados['turma']} | **Nota:** {aluno_dados['nota']}/10")
            
            for index, r in enumerate(aluno_dados["detalhes"]):
                simbolo = "✅" if r['resultado'] == 'Acerto' else "❌"
                st.write(f"Q{index+1}) Função **{r['funcao']}** | Resposta: {r['resposta']} | Gabarito: {r['correta']} - {simbolo}")
                
            if st.button("⚠️ Excluir Histórico Local Geral"):
                st.session_state["historico_notas"] = []
                st.warning("Banco de dados limpo com sucesso!")
                st.rerun()
    elif senha != "":
        st.error("Senha inválida!")
