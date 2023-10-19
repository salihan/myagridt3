import streamlit as st
import pandas as pd
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel
import plotly.graph_objects as go

rice_model = RiceModel()
pakchoi_model = PakchoiModel()

class ReportView:
    def __init__(self, home_model2):
        self.home_model2 = home_model2

    def render(self):
        df_farm = self.home_model2.get_actual_data()
        # st.dataframe(df_farm)
        select_farm_name = df_farm['Farm Name']
        selected_farm_name = st.sidebar.selectbox("Farm Name", select_farm_name)

        # Create an empty Plotly figure
        fig = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()

        average_pH = 0
        average_EC = 0

        if selected_farm_name.strip() == "Rice":
            st.subheader("Farm1: Rice")
            df_raw_rice = rice_model.get_data()
            st.write(df_raw_rice)
        elif selected_farm_name.strip() == "Pok Choy Hydroponics":
            st.subheader("Farm 2: Pak Choy")
            df_pakchoi = pakchoi_model.get_actual_data()
            df_pakchoi['Date'] = pd.to_datetime(df_pakchoi['Date'], format='%d/%m/%Y')
            select_pot = st.selectbox("Select Pot", df_pakchoi['Pot'].unique())
            df_filterpot_pakchoi = df_pakchoi[df_pakchoi['Pot'] == select_pot]
            select_subpot = st.selectbox("Select SubPot", df_filterpot_pakchoi['SubPot'].unique())
            df_filtersubpot_pakchoi = df_filterpot_pakchoi[df_filterpot_pakchoi['SubPot'] == select_subpot]


            df_target = pakchoi_model.get_target_data()
            df_target['Date'] = pd.to_datetime(df_target['Date'], format='%d/%m/%Y')
            df_filterpot_target = df_target[df_target['Pot'] == select_pot]
            df_filtersubpot_target = df_filterpot_target[df_filterpot_target['SubPot'] == select_subpot]
            # Calculate the average pH
            average_pH = df_filtersubpot_pakchoi['pH'].mean()
            average_EC = df_filtersubpot_pakchoi['EC'].mean()

            df_prediction = pakchoi_model.get_prediction_data()
            df_prediction['Date'] = pd.to_datetime(df_prediction['Date'], format='%d/%m/%Y')
            df_filterpot_prediction = df_prediction[df_prediction['Pot'] == select_pot]
            df_filtersubpot_prediction = df_filterpot_prediction[df_filterpot_prediction['SubPot'] == select_subpot]

            fig.add_trace(go.Bar(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Plant Height(mm)'], name='Actual'))
            fig.add_trace(go.Bar(x=df_filtersubpot_target['Date'], y=df_filtersubpot_target['Plant Height(mm)'], name='Target'))
            fig.add_trace(go.Bar(x=df_filtersubpot_prediction['Date'], y=df_filtersubpot_prediction['Plant Height(mm)'], name='Prediction'))

            fig2.add_trace(go.Bar(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Leaves Count'], name='Actual'))
            fig2.add_trace(go.Bar(x=df_filtersubpot_target['Date'], y=df_filtersubpot_target['Leaves Count'], name='Target'))
            fig2.add_trace(go.Bar(x=df_filtersubpot_prediction['Date'], y=df_filtersubpot_prediction['Leaves Count'], name='Prediction'))

            fig3.add_trace(go.Bar(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['pH'], name='Actual'))
            fig3.add_trace(go.Bar(x=df_filtersubpot_target['Date'], y=df_filtersubpot_target['pH'], name='Target'))
            fig3.add_trace(go.Bar(x=df_filtersubpot_prediction['Date'], y=df_filtersubpot_prediction['pH'], name='Prediction'))

            fig4.add_trace(go.Bar(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['EC'], name='Actual'))
            fig4.add_trace(go.Bar(x=df_filtersubpot_target['Date'], y=df_filtersubpot_target['EC'], name='Target'))
            fig4.add_trace(go.Bar(x=df_filtersubpot_prediction['Date'], y=df_filtersubpot_prediction['EC'], name='Prediction'))

        elif selected_farm_no == 3:
            st.subheader("Farm 3: Eucalyptus")
        # elif selected_farm_no == 4:
        #     st.subheader("Farm 4: Aqua")
        # elif selected_farm_no == 5:
        #     st.subheader("Farm 5: Rice")
        # elif selected_farm_no == 6:
        #     st.subheader("Farm 6: Pak Choy")
        #
        tab1, tab2, tab3, tab4 = st.tabs(['Plant Height', 'Leaves Count', 'pH', 'EC'])
        with tab1:
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Plant Height(mm)')
            fig.update_layout(title='Plant Height Comparison', width=800)
            st.plotly_chart(fig)

        with tab2:
            fig2.update_xaxes(title_text='Date')
            fig2.update_yaxes(title_text='Leaves Count')
            fig2.update_layout(title='Leaves Count Comparison', width=800)
            st.plotly_chart(fig2)

        with tab3:
            col = st.columns([1, 2])

            with col[0]:
                speedometer_ph = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=average_pH,
                    title="Average pH",
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 14]},
                        'bar': {'color': "royalblue"},
                        'steps': [
                            {'range': [0, 7], 'color': "lightgreen"},
                            {'range': [7, 10], 'color': "yellow"},
                            {'range': [10, 14], 'color': "red"}
                        ],
                    }
                ))
                speedometer_ph.update_layout(height=400, width=300)
                st.plotly_chart(speedometer_ph)

            with col[1]:
                fig3.update_xaxes(title_text='Date')
                fig3.update_yaxes(title_text='pH')
                fig3.update_layout(title='pH Comparison')
                st.plotly_chart(fig3)

        with tab4:
            col = st.columns([1, 2])

            with col[0]:
                speedometer_EC = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=average_EC,
                    title="Average EC",
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [0, 40]},
                        'bar': {'color': "royalblue"},
                        'steps': [
                            {'range': [0, 10], 'color': "lightgreen"},
                            {'range': [11, 29], 'color': "yellow"},
                            {'range': [30, 40], 'color': "red"}
                        ],
                    }
                ))
                speedometer_EC.update_layout(height=400, width=300)
                st.plotly_chart(speedometer_EC)

            with col[1]:
                fig4.update_xaxes(title_text='Date')
                fig4.update_yaxes(title_text='EC')
                fig4.update_layout(title='EC Comparison')
                st.plotly_chart(fig4)