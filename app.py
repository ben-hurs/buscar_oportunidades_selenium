import streamlit as st
import pandas as pd
from buscar_links import TRIBUNAIS, buscar_em_tribunal
from busca_detalhes_processos import buscar_detalhes_processos

st.set_page_config(layout="wide")
st.title("🔍 Consulta de Processos Judiciais")

nome = st.text_input("Digite o nome da parte (ex: jbs)")

if st.button("Buscar"):
    if not nome:
        st.warning("Por favor, digite um nome.")
    else:
        todos_links = []
        for tribunal in TRIBUNAIS:
            st.write(f"🔎 Buscando em: {tribunal}")
            links = buscar_em_tribunal(nome, tribunal)
            st.write(f"✅ {len(links)} link(s) encontrado(s) em {tribunal}")
            todos_links.extend(links)

        if not todos_links:
            st.warning("Nenhum processo encontrado.")
        else:
            st.write(f"🔗 Total de links coletados: {len(todos_links)}")
            st.write("⏳ Coletando detalhes dos processos...")

            resultados = buscar_detalhes_processos(todos_links[:20])  # limitar para teste

            df_resumo = pd.DataFrame([{
                "Número": r["numero_processo"],
                "Classe": r["classe"],
                "Assunto": r["assunto"],
                "Foro": r["foro"],
                "Vara": r["vara"],
                "Valor da Ação": r["valor_acao"]
            } for r in resultados])

            st.success(f"✅ {len(resultados)} processos coletados com sucesso.")
            st.dataframe(df_resumo, use_container_width=True)

            for r in resultados:
                with st.expander(f"📄 Detalhes do processo {r['numero_processo']}"):
                    st.write("📌 Classe:", r["classe"])
                    st.write("📌 Assunto:", r["assunto"])
                    st.write("📌 Foro:", r["foro"])
                    st.write("📌 Vara:", r["vara"])
                    st.write("📌 Valor da Ação:", r["valor_acao"])
                    st.write("👥 Partes:")
                    for parte in r.get("partes", []):
                        st.write(f"- {parte['tipo']}: {parte['nome']}")
