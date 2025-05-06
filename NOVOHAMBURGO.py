import pandas as pd
import streamlit as st

# 🌐 Configuração da Página
st.set_page_config(page_title="Dashboard de Quitação", layout="wide")

# 🌟 Estilo customizado para cards
st.markdown("""
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .card h3 {
        margin: 0;
        font-size: 18px;
        color: #6c757d;
    }
    .card p {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# 📂 Carregamento do arquivo
df = pd.read_csv("C:\\Users\\pablo paiva\\PROJETOS\\CÓDIGO\\novohamburgosS.csv")

# 🧮 Funções auxiliares
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def converter_dias_para_meses(dias):
    return dias / 30.44

# 🎛️ Filtros no sidebar
st.sidebar.header("Filtros")
processo_filter = st.sidebar.selectbox("Processo", options=["Todos", "SIM", "NÃO"])
banco_filter = st.sidebar.selectbox("Banco", options=["Todos"] + df["BANCO"].unique().tolist())
profissao_filter = st.sidebar.selectbox("Profissão", options=["Todos"] + df["PROFISSÃO"].unique().tolist())

# 🔍 Aplicar filtros
if processo_filter != "Todos":
    df = df[df["PROCESSO"] == processo_filter]
if banco_filter != "Todos":
    df = df[df["BANCO"] == banco_filter]
if profissao_filter != "Todos":
    df = df[df["PROFISSÃO"] == profissao_filter]

# ✅ Processamento e Métricas
if not df.empty:
    df["QUALIDADE"] = pd.to_datetime(df["QUALIDADE"], format="%d/%m/%Y")
    data_limite = pd.to_datetime("2024-11-30")
    df["DIFERENCA_DIAS"] = (data_limite - df["QUALIDADE"]).dt.days
    media_dias = df["DIFERENCA_DIAS"].mean()
    media_meses = converter_dias_para_meses(media_dias)

    df["PERCENTUAL"] = pd.to_numeric(df["PERCENTUAL"], errors="coerce")

    metricas = {
        "Total de contratos": df["CONTRATO"].nunique(),
        "Média de meses de atraso": round(df["MESES ATRASO BANCÁRIO"].mean(), 1),
        "Saldo devedor médio": formatar_valor(df["SALDO DEVEDOR"].mean()),
        "Maior saldo devedor": formatar_valor(df["SALDO DEVEDOR"].max()),
        "Menor saldo devedor": formatar_valor(df["SALDO DEVEDOR"].min()),
        "Média de desconto concedido": formatar_valor(df["DESCONTO"].mean()),
        "Total de descontos concedidos": formatar_valor(df["DESCONTO"].sum()),
        "Faixa etária mais comum": df["FAIXA ETÁRIA"].mode()[0],
        "Ano do veículo mais comum": df["ANO DO VEÍCULO"].mode()[0],
        "Banco mais frequente": df["BANCO"].mode()[0],
        "Estado civil mais comum": df["ESTADO CIVIL"].mode()[0],
        "Assessoria mais comum": df["ASSESSORIA"].mode()[0],
        "Quantidade da assessoria mais comum": df["ASSESSORIA"].value_counts().max(),
        "Semana com mais quitações": df["SEMANA DA QUITAÇÃO"].mode()[0],
        "Contratos com processo - Sim": df[df["PROCESSO"] == "SIM"].shape[0],
        "Contratos com processo - Não": df[df["PROCESSO"] == "NÃO"].shape[0],
        "Profissão mais comum": df["PROFISSÃO"].mode()[0],
        "Quantidade de contratos da profissão mais comum": df[df["PROFISSÃO"] == df["PROFISSÃO"].mode()[0]].shape[0],
        "Tipo de contrato mais comum": df["TIPO DE CONTRATO"].mode()[0],
        "Média de dias de fechamento até nov/24": f"{media_dias:.0f} dias",
        "Média de meses de fechamento até nov/24": f"{media_meses:.1f} meses",
        "Total do Saldo Devedor": formatar_valor(df["SALDO DEVEDOR"].sum()),
        "Percentual médio do desconto": f"{(df['DESCONTO'].mean() / df['SALDO DEVEDOR'].mean()) * 100:.2f}%",
    }

    st.title("📊 Dashboard de Quitação de Dívidas")

    # 🧱 Layout com cards organizados
    metric_names = list(metricas.keys())
    num_columns = 4
    rows = [metric_names[i:i+num_columns] for i in range(0, len(metric_names), num_columns)]

    for row in rows:
        cols = st.columns(len(row))
        for i, metrica in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                    <div class="card">
                        <h3>{metrica}</h3>
                        <p>{metricas[metrica]}</p>
                    </div>
                """, unsafe_allow_html=True)


    # 📥 Exportação CSV
    resultados_df = pd.DataFrame(metricas.items(), columns=["Métrica", "Valor"])
    csv = resultados_df.to_csv(index=False)
    st.download_button("📥 Baixar CSV", data=csv, file_name="dashboard_quitacao.csv", mime="text/csv")
else:
    st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
