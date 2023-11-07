import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np
import json
from services.util import Utilities
from streamlit_echarts import st_echarts
from datetime import datetime
from models import Dash

class DashView:

    _util = Utilities()
    _user = None

    def __init__(self, p_usuario):
        self._user = p_usuario

    def incluir_view_dashboard(self):
        """
            Montar a tela com os gráfico de usuário e de comparação.

        Args:
            p_usuario (Object): recebe o usuário que será utilizado
        """

        # dataframes de informações do usuário e de todos usuários
        global df_usuario, df_total

        # monta o dataframe com as informações do usuário
        df_usuario = Dash().montar_df_usuario_dash(self._user)
        
        # cria um menu com as opções de visualizar usuário e comparação geral
        opcoes_dash = {'person-fill':'Usuário',
                    'people-fill':'Geral' }
        selecionado = self._util.montar_menu_dash(opcoes_dash)

        if selecionado == 'Usuário':
            self.dash_usuario_logado()

        if selecionado == 'Geral':
            # monta dataframe com a informações de todos usuários
            df_total = Dash().montar_df_total_dash()
            self.dash_geral()

    def dash_usuario_logado(self):
        """
            Função para montar os gráficos com as estatísticas do usuário

        Args:
            p_usuario (Object): usuário que será utilizado
        """
        st.header(f'Estátisticas para: {str(self._user.nome).split(" ")[0]}')

        # caso não existe informação para este usuário, retorna mensagem
        if df_usuario.size == 0:
            st.text('Sem estatisticas para este usuário no momento.')
        else:
            # monta um dataframe com as leituras finalizadas apenas
            df_finalizado = df_usuario.where(df_usuario['data_fim'] != '').dropna()
            # monta um dataframe com apenas uma leitura de cada (caso exista mais de 1 autor)
            df_sem_duplicado = df_finalizado.drop_duplicates(subset=['id_leitura'], keep='first')

            #
            #
            # Cards com métricas 
            #
            #
            col1, col2, col3, col4 = st.columns(4)
            # busca no dataframe o total de livros lidos
            total_leituras = int(df_sem_duplicado['ano_fim'].count())
            # busca no dataframe o total de livros lidos no ano atual
            total_leituras_ano = int(df_sem_duplicado['ano_fim'].where(df_sem_duplicado['ano_fim'] == datetime.now().year).where(df_sem_duplicado['ano_fim'] == df_sem_duplicado['ano_ini']).count())
            # monta o card 1
            col1.metric(label='Total de Livros', value=total_leituras,delta=total_leituras_ano)
            # busca no dataframe o total de livros que foram finalizados apenas no ano posterior ao inicio da leitura
            total_atrasado = int(df_sem_duplicado.where(
                df_finalizado['ano_fim'] != df_finalizado['ano_ini']).count()['ano_ini'])
            # busca no dataframe o total de atrasado no ano atual
            total_atrasado_ano = int(df_sem_duplicado.where(df_finalizado['ano_fim'] != df_finalizado['ano_ini']).where(df_sem_duplicado['ano_fim'] == datetime.now().year).count()['ano_ini'])
            # monta o card 2
            col2.metric(label='Leituras atrasadas',value=total_atrasado, delta=total_atrasado_ano)
            # busca no dataframe o total de autores lidos
            total_autores = int(df_finalizado.groupby('pseud_autor')['pseud_autor'].nunique().count())
            # busca no dataframe o total de autores lidos no ano atual
            total_autores_ano = int(df_finalizado.where(df_finalizado['ano_fim'] == datetime.now().year).where(df_finalizado['ano_fim'] == df_finalizado['ano_ini'])['pseud_autor'].dropna().nunique())
            # monta o card 3
            col3.metric(label='Autores lidos', value=total_autores,delta=total_autores_ano)
            # busca no dataframe livros lidos mais de uma vez
            total_releituras = int(df_sem_duplicado.groupby('nome_livro')['nome_livro'].filter(lambda x: x.count() > 1).nunique())
            # busca no dataframe livros lidos mais de uma vez no ano atual
            total_releituras_ano = int(df_sem_duplicado.groupby('nome_livro').filter(lambda x: x['nome_livro'].count() > 1).where(lambda y: y['ano_ini'] == datetime.now().year).dropna().count()['id_livro'])
            # monta o card 4
            col4.metric(label='Livros relidos', value=total_releituras,delta=total_releituras_ano)

            box_shadow_str = (
                "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
            )
            st.markdown(
                f"""
                <style>
                    div[data-testid="column"] {{
                        background-color: #FFF;
                        border: 1px solid #CCC;
                        padding: 2% 2% 2% 5%;
                        border-radius: 5px;
                        border-left: 0.6rem solid #2f4756 !important;
                        {box_shadow_str}
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

            #
            # Gráfico 1
            # Busca o total de livros lidos por ano (x = ano / y = quantidade) 
            # Exibe em um gráfico de barras
            #
            # Adiciona um expander para que aquele gráfico possa ser minimizado
            with st.expander('Número de livros lidos por ano', expanded=True):
                st.markdown('Gráfico gerado usando dataframe e st.barchart')
                # busca no dataframe e cria um novo apenas com as informações com a quantidade de livros finalizado agrupando pelo ano de inicio
                df_ano = pd.DataFrame(df_sem_duplicado.groupby('ano_ini')['nome_livro'].count())
                df_ano.columns = ['Quantidade Livros']
                df_ano.rename(index={'': 'Não iniciado'}, inplace=True)
                # exibe um gráfico de barras na tela
                st.bar_chart(data=df_ano, height=500, width=768,use_container_width=True)

            #
            # Gráfico 2
            # Busca o total de livros iniciado e finalizados no mesmo mês (x = quantidade / y = ano) 
            # Exibe em um gráfico de dispersão
            #
            # Adiciona um expander para que aquele gráfico possa ser minimizado
            with st.expander('Livros finalizados no mesmo mês', expanded=True):
                st.markdown('Gráfico gerado utilizando altair e st.altair_chart')
                # busca no dataframe e cria um novo apenas com as informações com a quantidade de livros finalizados no mesmo mês
                df_mesmo_mes = pd.DataFrame(df_sem_duplicado.where(df_sem_duplicado['mes_ini'] == df_sem_duplicado['mes_fim']).dropna())
                # monta o gráfico com o mês na vertical e a quantidade de livros na horizontal 
                # o tamanho dos pontos é definido pela quantidade
                chart = alt.Chart(df_mesmo_mes, width=768, padding={'left': 0, 'top': 0, 'bottom': 0, 'right': 50}).mark_circle().encode(
                    alt.Y('mes_fim:Q', type='nominal', title='Mes Finalizado'),
                    alt.X('count(nome_livro)', axis=None),
                    alt.Size('count()', legend=None),
                )
                # exibe um gráfico de dispersão na tela
                st.altair_chart(chart,  use_container_width=True)

            #
            # Gráfico 3
            # Busca o total de livros por formato de leitura 
            # Exibe em um gráfico de pizza
            #
            # Adiciona um expander para que aquele gráfico possa ser minimizado
            with st.expander('Tipo de formato mais utilizado', expanded=True):
                st.markdown('Gráfico gerado utilizando streamlit e st_charts')
                # busca no dataframe as quantidades agrupadas pelo formato
                df_formato = df_sem_duplicado.groupby('formato', as_index=False).count()[['formato','nome_livro']]
                df_formato.columns = ['name', 'value']
                # transforma o dataframe em um json
                json_list = json.loads(json.dumps(
                    list(df_formato.T.to_dict().values())))
                # monta o gráfica de pizza
                options = {
                    "tooltip": {"trigger": "item"},
                    "series": [{
                        "type": "pie",
                        "data": json_list,
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }],
                }
                # exibe o gráfico de pizza na tela
                st_echarts(
                    options=options, height="600px",
                )

            #
            # Gráfico 4
            # Busca o total de livros lidos, separando por mês de inicio
            # Exibe em um gráfico de barras horizontal
            #
            # Adiciona um expander para que aquele gráfico possa ser minimizado
            with st.expander('Número de livros lidos por mês*', expanded=True):
                # cria uma lista com o nome dos meses
                meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                st.markdown('Gráfico gerado utilizado matplotlib e st.pyplot')
                # busca no dataframe e cria um novo agrupado pelo mês
                df_mes = pd.DataFrame(df_sem_duplicado.groupby('mes_ini').count()['nome_livro'])
                df_mes.columns = ['Quantidade Livros']
                meses_encontrados = []
                # busca apenas os meses que existem no dataframe
                for x in df_mes.index.values:
                    meses_encontrados.append(meses[x-1])
                # busca média de livros lidos
                media = np.mean(df_mes['Quantidade Livros'])
                y_pos = np.arange(len(df_mes))
                # monta o gráfico de barras
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.set_yticks(y_pos, labels=meses_encontrados)
                hbars = ax.barh(y_pos, df_mes['Quantidade Livros'], align='center')
                ax.invert_yaxis()
                ax.bar_label(hbars)
                ax.set_xlim(right=15)
                ax.set_xlabel('Quantidade de Livros')
                ax.axvline(media, ls='--', color='r')
                # exibe o gráfico de barras na tela
                st.pyplot(fig, {'transparent': True, 'dpi': 40})
                st.caption(
                    '\* Levando em consideração a data de finalização da leitura.')

    def dash_geral(self):
        """
            Função para montar os gráficos de comparação do usuário com o geral
        """
        # caso não existe informação para este usuário, retorna mensagem
        if df_usuario.size == 0:
            st.text('Sem estatisticas para comparação no momento.')
        else:
            # monta o dataframe do usuário com apenas livros finalizados e sem duplicado
            df_usuario_finalizado = df_usuario.where(df_usuario['data_fim'] != '').dropna()
            df_usuario_sem_duplicado = df_usuario_finalizado.drop_duplicates(
            subset=['id_leitura'], keep='first')
            # monta o dataframe geral de livros finalizado e sem duplicado
            df_total_finalizado = df_total.where(df_total['data_fim'] != '').dropna()
            df_total_sem_duplicado = df_total_finalizado.drop_duplicates(
            subset=['id_leitura'], keep='first')
            
            
            #
            # Gráfico 1
            # Busca o total de livros lidos por ano (x = ano / y = quantidade) 
            # Exibe em um gráfico de area (linha) comparado o usuário com a média geral
            #
            with st.expander('Número de livros lidos por ano', expanded=True):
                st.markdown('Gráfico gerado usando dataframe e st.area_chart')
                df_ano_usuario = pd.DataFrame(df_usuario_sem_duplicado
                                            .groupby('ano_ini')['nome_livro']
                                            .count())
                df_ano_total_temp = pd.DataFrame(df_total_sem_duplicado
                                                .groupby(['ano_ini', 'id_usuario'])['nome_livro']
                                                .count())
                df_ano_total = df_ano_total_temp.groupby('ano_ini').mean().round()
                df_all = pd.merge(df_ano_total, df_ano_usuario,
                                on='ano_ini', how='left')
                df_all.columns = ['Média', 'Você']
                st.area_chart(data=df_all, height=500, width=768,
                            use_container_width=True)#, y=df_ano_total.max())

            #
            # Gráfico 2
            # Busca o total de livros iniciado e finalizados no mesmo mês (x = quantidade / y = ano) 
            # Exibe em um gráfico de dispersão comparando o usuário com o geral
            #
            with st.expander('Livros finalizados no mesmo mês', expanded=True):
                st.markdown('Gráfico gerado utilizando altair e st.altair_chart')
                df_mesmo_mes_usuario = pd.DataFrame(df_usuario_sem_duplicado.where(
                    df_usuario_sem_duplicado['mes_ini'] == df_usuario_sem_duplicado['mes_fim'])
                    .dropna()
                    .groupby('mes_fim')['nome_livro']
                    .count())
                df_mesmo_mes_total_temp = pd.DataFrame(df_total_sem_duplicado.where(
                    df_total_sem_duplicado['mes_ini'] == df_total_sem_duplicado['mes_fim'])
                    .dropna()
                    .groupby(['mes_fim', 'id_usuario'])
                    .count()['nome_livro'])
                df_mesmo_mes_total = df_mesmo_mes_total_temp.groupby('mes_fim').mean().round()
                df_all_temp = pd.merge(df_mesmo_mes_total,df_mesmo_mes_usuario, on='mes_fim', how='left')
                df_all_temp.columns = ['Média', 'Você']
                df_all = pd.DataFrame(df_all_temp.stack().reset_index())
                df_all.columns = ['mes','origin','value']
                chart = alt.Chart(df_all, width=768, height=400, padding={'left': 0, 'top': 0, 'bottom': 0, 'right': 50}).mark_circle().encode(
                        alt.Y('mes', type='nominal', title='Mês Finalizado'),
                        alt.X('value', type='nominal', title='Quantidade'),
                        alt.Color('origin', type='nominal',title='Legenda'),
                        )
                st.altair_chart(chart,  use_container_width=True)
                
            #
            # Gráfico 3
            # Busca o total de livros por formato de leitura 
            # Exibe em um gráfico de pizza
            #
            with st.expander('Tipo de formato mais utilizado', expanded=True):
                st.markdown('Gráfico gerado utilizando streamlit e st_charts')
                df_formato = df_total_sem_duplicado.groupby('formato', as_index=False).count()[
                    ['formato', 'nome_livro']]
                df_formato.columns = ['name', 'value']
                json_list = json.loads(json.dumps(
                    list(df_formato.T.to_dict().values())))
                options = {
                    "tooltip": {"trigger": "item"},
                    "series": [{
                        "type": "pie",
                        "data": json_list,
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }],
                }
                st_echarts(
                    options=options, height="600px",
                )

            #
            # Gráfico 4
            # Busca o total de livros lidos, separando por mês de inicio
            # Exibe em um gráfico de barras horizontal comparando o usuário com a média geral.
            #
            with st.expander('Número de livros lidos por mês*', expanded=True):
                meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun','Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                st.markdown('Gráfico gerado utilizado matplotlib e st.pyplot')
                df_usuario_mes = pd.DataFrame(df_usuario_sem_duplicado.groupby('mes_ini').count()['nome_livro'])
                df_total_mes_temp = pd.DataFrame(df_total_sem_duplicado
                                                .groupby(['mes_ini', 'id_usuario'])['nome_livro']
                                                .count())
                df_total_mes = df_total_mes_temp.groupby('mes_ini').mean().round()
                df_all = pd.merge(df_total_mes, df_usuario_mes,
                                on='mes_ini', how='left')
                df_all.columns = ['Média', 'Você']
                y_pos = np.arange(len(df_all))
                fig, ax = plt.subplots(figsize=(8,4))
                meses_encontrados = []
                for x in df_all.index.values:
                    meses_encontrados.append(meses[x-1])
                ax.set_yticks(y_pos, labels=meses_encontrados)
                ax.invert_yaxis()
                h1 = ax.barh(y_pos, df_all['Média'], align='edge', color='grey')
                h2 = ax.barh(y_pos, df_all['Você'], align='center', color='lightblue')
                ax.bar_label(h1)
                ax.bar_label(h2)
                ax.legend(df_all.columns)
                ax.set_xlabel('Quantidade de Livros')
                st.pyplot(fig, {'transparent': True, 'dpi': 40})
                st.caption(
                    '\* Levando em consideração a data de finalização da leitura.')


