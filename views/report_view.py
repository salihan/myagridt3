import streamlit as st
import pandas as pd
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel
import plotly.graph_objects as go
import datetime

rice_model = RiceModel()
pakchoi_model = PakchoiModel()

class ReportView:
    def __init__(self, home_model2):
        self.home_model2 = home_model2

    @staticmethod
    def style_risk_level(val):
        color = 'red' if val == 'High' else ''
        return f'color: {color}'

    @staticmethod
    def style_row(row):
        color = 'red' if 'High' in row.values else ''
        return [f'color: {color}'] * len(row)


    def render(self):
        st.markdown("""
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                            """, unsafe_allow_html=True)

        df_farm = self.home_model2.get_actual_data()
        df_potrisk = self.home_model2.get_pot_risk()

        select_farm_name = df_farm['Farm Name']
        selected_farm_name = st.sidebar.selectbox("Farm Name", select_farm_name)

        # Create an empty Plotly figure
        potfig = go.Figure()
        potfig2 = go.Figure()
        potfig3 = go.Figure()
        potfig4 = go.Figure()
        fig = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()

        average_pH = 0
        average_EC = 0

        if selected_farm_name.strip() == "Rice":
            st.subheader("Farm: Rice")
            df_raw_rice = rice_model.get_data()
            st.write(df_raw_rice)
        elif selected_farm_name.strip() == "Pok Choy Hydroponics":
            st.subheader("Farm: Pak Choy Hydrophonic")

            # Apply styling to the entire DataFrame
            styled_df = df_potrisk.style.apply(self.style_row, axis=1, subset=['Risk Level', 'Risk Level of Plant height',
                                                                                 'Risk Level of longest leaf', 'Risk Level of leaf count',
                                                                                 'Risk Level of pH','Risk Level of Temp', 'Risk Level of EC'])
            st.dataframe(styled_df, hide_index=True)
            st.divider()

            df_pakchoi = pakchoi_model.get_actual_data()
            df_pakchoi['Date'] = pd.to_datetime(df_pakchoi['Date'], format='%d/%m/%Y', errors='coerce', infer_datetime_format=True)
            # st.write(df_pakchoi)

            # Create a Streamlit date range picker
            date_range = st.date_input('Select Date Range:',
                                       value=[(datetime.datetime.now() - datetime.timedelta(days=7)).date(),
                                              datetime.datetime.now().date()])

            # Convert selected date range to datetime format
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])


            select_pot = st.selectbox("Select Pot", df_pakchoi['Pot'].unique())
            df_filterpot_pakchoi = df_pakchoi[df_pakchoi['Pot'] == select_pot]
            df_filterpot_pakchoi_withindate = df_filterpot_pakchoi[
                (df_filterpot_pakchoi['Date'] >= start_date) & (df_filterpot_pakchoi['Date'] <= end_date)]

            # Get the maximum date from the filtered DataFrame
            latest_date = df_filterpot_pakchoi_withindate['Date'].max()
            # Filter the DataFrame to include only the rows with the latest date
            latest_data = df_filterpot_pakchoi_withindate[df_filterpot_pakchoi_withindate['Date'] == latest_date]
            latest_leaves_mean = latest_data['Leaves Count'].mean()
            latest_longleaf_mean = latest_data['Longest Leaf'].mean()
            latest_height_mean = latest_data['Plant Height(mm)'].mean()
            st.write("Latest average Pot data")
            st.markdown(f"""
                <table class="table">
                  <thead>
                    <tr class="bg-warning">
                      <th scope="col">Latest Date</th>
                      <th scope="col">Leaves Count</th>
                      <th scope="col">Longest Leaf (mm)</th>
                      <th scope="col">Plant Height(mm)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="bg-warning">
                      <th scope="row">{latest_date}</th>
                      <td>{latest_leaves_mean}</td>
                      <td>{latest_longleaf_mean}</td>
                      <td>{latest_height_mean}</td>
                    </tr>                    
                  </tbody>
                </table>
            """, unsafe_allow_html=True)
            tab1, tab2 = st.tabs(['Pot Data', 'Pot Scatter Plot'])
            with tab1:
                st.write(df_filterpot_pakchoi_withindate[['Date', 'SubPot', 'EC', 'pH', 'Leaves Count', 'Longest Leaf', 'Plant Height(mm)']])
            with tab2:
                # Reset the index of the DataFrame
                df_filterpot_pakchoi_withindate_reset = df_filterpot_pakchoi_withindate.reset_index(drop=True)

                # Use st.scatter_chart with the reset DataFrame
                st.scatter_chart(
                    data=df_filterpot_pakchoi_withindate_reset,
                    x='Date',
                    y='Plant Height(mm)',
                    size='Leaves Count',
                    color='Longest Leaf',
                    use_container_width=True
                )


            select_subpot = st.selectbox("Select SubPot", df_filterpot_pakchoi['SubPot'].unique())
            df_filtersubpot_pakchoi = df_filterpot_pakchoi[df_filterpot_pakchoi['SubPot'] == select_subpot]
            # Filter data based on the selected date range
            df_filtersubpotdate_actual = df_filtersubpot_pakchoi[(df_pakchoi['Date'] >= start_date) & (df_filtersubpot_pakchoi['Date'] <= end_date)]


            df_target = pakchoi_model.get_target_data()
            df_target['Date'] = pd.to_datetime(df_target['Date'], format='%d/%m/%Y', errors='coerce', infer_datetime_format=True)
            df_filterpot_target = df_target[df_target['Pot'] == select_pot]
            df_filtersubpot_target = df_filterpot_target[df_filterpot_target['SubPot'] == select_subpot]
            df_filtersubpotdate_target = df_filtersubpot_target[(df_pakchoi['Date'] >= start_date) & (df_filtersubpot_target['Date'] <= end_date)]

            # Calculate the average pH
            average_pH = df_filtersubpotdate_actual['pH'].mean()
            average_EC = df_filtersubpotdate_actual['EC'].mean()

            df_prediction = pakchoi_model.get_prediction_data()
            df_prediction['Date'] = pd.to_datetime(df_prediction['Date'], format='%d/%m/%Y', errors='coerce', infer_datetime_format=True)
            df_filterpot_prediction = df_prediction[df_prediction['Pot'] == select_pot]
            df_filtersubpot_prediction = df_filterpot_prediction[df_filterpot_prediction['SubPot'] == select_subpot]
            df_filtersubpotdate_predict = df_filtersubpot_prediction[(df_pakchoi['Date'] >= start_date) & (df_filtersubpot_prediction['Date'] <= end_date)]

            fig.add_trace(go.Scatter(x=df_filtersubpotdate_actual['Date'], y=df_filtersubpotdate_actual['Plant Height(mm)'], mode='markers',
                                     marker=dict(color='LightSkyBlue', size=20, line=dict( color='MediumPurple', width=2)), name='Actual'))
            fig.add_trace(go.Scatter(x=df_filtersubpotdate_target['Date'], y=df_filtersubpotdate_target['Plant Height(mm)'], mode= 'markers', name='Target'))
            fig.add_trace(go.Scatter(x=df_filtersubpotdate_predict['Date'], y=df_filtersubpotdate_predict['Plant Height(mm)'], mode= 'lines+markers', name='Prediction'))

            fig2.add_trace(go.Scatter(x=df_filtersubpotdate_actual['Date'], y=df_filtersubpotdate_actual['Leaves Count'], mode='markers',
                                      marker=dict(color='LightSkyBlue', size=20, line=dict( color='MediumPurple', width=2)),name='Actual'))
            fig2.add_trace(go.Scatter(x=df_filtersubpotdate_target['Date'], y=df_filtersubpotdate_target['Leaves Count'], mode= 'markers', name='Target'))
            fig2.add_trace(go.Scatter(x=df_filtersubpotdate_predict['Date'], y=df_filtersubpotdate_predict['Leaves Count'], mode= 'lines+markers', name='Prediction'))

            fig3.add_trace(go.Scatter(x=df_filtersubpotdate_actual['Date'], y=df_filtersubpotdate_actual['pH'], mode='markers',
                                      marker=dict(color='LightSkyBlue', size=20, line=dict( color='MediumPurple', width=2)), name='Actual'))
            fig3.add_trace(go.Scatter(x=df_filtersubpotdate_target['Date'], y=df_filtersubpotdate_target['pH'], mode= 'markers', name='Target'))
            fig3.add_trace(go.Scatter(x=df_filtersubpotdate_predict['Date'], y=df_filtersubpotdate_predict['pH'], mode= 'lines+markers', name='Prediction'))

            fig4.add_trace(go.Scatter(x=df_filtersubpotdate_actual['Date'], y=df_filtersubpotdate_actual['EC'], mode='markers',
                                      marker=dict(color='LightSkyBlue', size=20, line=dict( color='MediumPurple', width=2)), name='Actual'))
            fig4.add_trace(go.Scatter(x=df_filtersubpotdate_target['Date'], y=df_filtersubpotdate_target['EC'], mode= 'markers', name='Target'))
            fig4.add_trace(go.Scatter(x=df_filtersubpotdate_predict['Date'], y=df_filtersubpotdate_predict['EC'], mode= 'lines+markers', name='Prediction'))


        elif selected_farm_name.strip() == "Eucalyptus":
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
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig2.update_xaxes(title_text='Date')
            fig2.update_yaxes(title_text='Leaves Count')
            fig2.update_layout(title='Leaves Count Comparison', width=800)
            st.plotly_chart(fig2, use_container_width=True)

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
                st.plotly_chart(speedometer_ph, use_container_width=True)

            with col[1]:
                fig3.update_xaxes(title_text='Date')
                fig3.update_yaxes(title_text='pH')
                fig3.update_layout(title='pH Comparison')
                st.plotly_chart(fig3, use_container_width=True)

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
                st.plotly_chart(speedometer_EC, use_container_width=True)

            with col[1]:
                fig4.update_xaxes(title_text='Date')
                fig4.update_yaxes(title_text='EC')
                fig4.update_layout(title='EC Comparison')
                st.plotly_chart(fig4, use_container_width=True)