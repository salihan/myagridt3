import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel
from models.farm_model import get_telemetries
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime

rice_model = RiceModel()
pakchoi_model = PakchoiModel()


class Home2View:
    def __init__(self, home_model2):
        self.home_model2 = home_model2

    @staticmethod
    def style_cell(row):
        estimated_yield = row['Estimated Yield']
        yield_goal = row['Yield goal']

        if pd.notnull(estimated_yield) and pd.notnull(yield_goal):
            ratio = float(estimated_yield) / float(yield_goal)

            if ratio < 0.5:
                return ['color: red'] * len(row)
            elif ratio >= 0.5 and ratio < 0.8:
                return ['color: orange'] * len(row)
            else:
                return ['color: green'] * len(row)

        return [''] * len(row)

    def render(self):
        st.title('Farms')

        data = self.home_model2.get_actual_data()
        df_home = pd.DataFrame(data)
        df_home = df_home.iloc[:, 0:6]

        # Function to apply styling based on 'Risk Level'
        def style_risk_level(val):
            color = 'red' if val == 'High Risk' else ''
            return f'color: {color}'

        # Apply styling to the entire DataFrame
        styled_df = df_home.style.applymap(style_risk_level, subset=['Risk Level'])

        # Display the styled DataFrame
        st.dataframe(styled_df, hide_index=True)

        st.markdown("""
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                    """, unsafe_allow_html=True)

        st.divider()
        farm_names = df_home["Farm Name"].tolist()
        selected_farm = st.selectbox('Farm Name:', farm_names)
        df_selected_farm = df_home[df_home["Farm Name"] == selected_farm]

        #for now we hardcode this since only pakchoi data is available
        if selected_farm == "Pok Choy Hydroponics":
            df_pakchoi = pd.DataFrame(pakchoi_model.get_actual_data())
            bil_pot = len(df_pakchoi['Pot'].unique())
            bil_subpot = len(df_pakchoi['SubPot'].unique())
            bil_crop = bil_subpot * bil_pot
            plant_height_mean = df_pakchoi['Plant Height(mm)'].mean()
            longest_leaves_mean = df_pakchoi['Longest Leaf'].mean()
            leaves_count_mean = df_pakchoi['Leaves Count'].mean()

            # Pot1
            df_pakchoi_pot1 = df_pakchoi[df_pakchoi['Pot'] == 1]
            pot1_ph_mean = df_pakchoi_pot1['pH'].mean()
            pot1_EC_mean = df_pakchoi_pot1['EC'].mean()

            telemetery1 = get_telemetries("UPMSO1001", "waterTemperature")
            df_telemetery1 = pd.DataFrame(telemetery1['data'])
            df_telemetery1['value'] = pd.to_numeric(df_telemetery1['value'], downcast="float")
            pot1_watertemp_mean = round(df_telemetery1['value'].mean(), 2)

            pot1_plant_height_mean = df_pakchoi_pot1['Plant Height(mm)'].mean()
            pot1_longest_leaves_mean = df_pakchoi_pot1['Longest Leaf'].mean()
            pot1_leaves_count_mean = df_pakchoi_pot1['Leaves Count'].mean()

            # Pot2
            df_pakchoi_pot2 = df_pakchoi[df_pakchoi['Pot'] == 2]
            pot2_ph_mean = df_pakchoi_pot2['pH'].mean()
            pot2_EC_mean = df_pakchoi_pot2['EC'].mean()

            telemetery2 = get_telemetries("UPMSO2001", "waterTemperature")
            df_telemetery2 = pd.DataFrame(telemetery2['data'])
            df_telemetery2['value'] = pd.to_numeric(df_telemetery2['value'], downcast="float")
            pot2_watertemp_mean = round(df_telemetery2['value'].mean(), 2)

            pot2_plant_height_mean = df_pakchoi_pot2['Plant Height(mm)'].mean()
            pot2_longest_leaves_mean = df_pakchoi_pot2['Longest Leaf'].mean()
            pot2_leaves_count_mean = df_pakchoi_pot2['Leaves Count'].mean()

            col = st.columns([1, 2])

            with col[0]:
                st.markdown(
                    f"""
                    <div class="card text-dark bg-light" style="width: auto;">
                      <div class="card-header">
                        Featured
                      </div>
                      <div class="card-body">
                          <div class="row">
                            <div class="col">
                                <strong>Number of Pots:</strong><br>
                                <strong>Number of Sub pots:</strong><br>
                                <strong>Number of Crop:</strong>
                            </div>
                            <div class="col text-right">
                                {bil_pot}<br>
                                {bil_subpot}<br>
                                {bil_crop}<br>                                    
                            </div>
                          </div>
                        </div>
                    </div><br>                
                    """, unsafe_allow_html=True
                )
                st.markdown(
                    f"""
                    <div class="card text-dark bg-light" style="width: auto;">
                      <div class="card-header">
                        Growth in Average
                      </div>
                      <div class="card-body">
                          <div class="row">
                            <div class="col">
                                <strong>Plant Height (mm):</strong><br>
                                <strong>Leaf Length (mm):</strong><br>
                                <strong>Number of Leaves:</strong>
                            </div>
                            <div class="col text-right">
                                {round(plant_height_mean, 2)}<br>
                                {round(longest_leaves_mean, 2)}<br>
                                {int(round(leaves_count_mean, 0))}<br>                                    
                            </div>
                          </div>
                        </div>
                    </div>                
                    """, unsafe_allow_html=True
                )

            with col[1]:
                latitude = 2.992193566444384
                longitude = 101.72348426648746
                st.markdown(
                    f"""
                    <div class="card text-dark bg-light" style="width: auto;">
                      <div class="card-header">
                        Location
                      </div>
                      <div class="card-body">
                          <iframe width="100%" height="350" src="https://www.openstreetmap.org/export/embed.html?bbox={longitude},{latitude},{longitude},{latitude}&layer=mapnik" frameborder="0"></iframe>
                      </div>
                    </div>                
                    """, unsafe_allow_html=True
                )

            secondcol = st.columns(2)
            with secondcol[0]:
                st.markdown(
                    f"""
                    <div class="card text-dark bg-light" style="width: auto;">
                      <div class="card-header">
                        Sub-Pot 1
                      </div>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item">Average pH: <strong> {pot1_ph_mean:.2f} </strong></li>
                        <li class="list-group-item">Average EC: <strong> {pot1_EC_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Water Temperature: <strong> {pot1_watertemp_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Plant Height (mm): <strong> {pot1_plant_height_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Longest Leaves (mm): <strong> {pot1_longest_leaves_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Number of Leaves: <strong> {int(pot1_leaves_count_mean)} </strong></li>
                      </ul>
                    </div>                
                    """, unsafe_allow_html=True
                )

            with secondcol[1]:
                st.markdown(
                    f"""
                    <div class="card text-dark bg-light" style="width: auto;">
                      <div class="card-header">
                        Sub-Pot 2
                      </div>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item">Average pH: <strong> {pot2_ph_mean:.2f} </strong></li>
                        <li class="list-group-item">Average EC: <strong> {pot2_EC_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Water Temperature: <strong> {pot2_watertemp_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Plant Height (mm): <strong> {pot2_plant_height_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Longest Leaves (mm): <strong> {pot2_longest_leaves_mean:.2f} </strong></li>
                        <li class="list-group-item">Average Number of Leaves: <strong> {int(pot2_leaves_count_mean)} </strong></li>
                      </ul>
                    </div>                
                    """, unsafe_allow_html=True
                )

            st.divider()


            select_pot = st.selectbox("Select Pot", df_pakchoi['Pot'].unique())
            df_filterpot_pakchoi = df_pakchoi[df_pakchoi['Pot'] == select_pot]
            df_filterpot_pakchoi['Date'] = pd.to_datetime(df_filterpot_pakchoi['Date'], format='%d/%m/%Y',
                                             errors='coerce', infer_datetime_format=True)
            df_telemetery2['Datetime'] = pd.to_datetime(df_telemetery2['readingAt'])

            st.subheader('Nutrients')
            tabPh, tabEC, tabTemp = st.tabs(['Ph','EC','Temperature'])

            with tabPh:
                st.line_chart(df_filterpot_pakchoi, x='Date', y='pH', color='#993399')
            with tabEC:
                st.line_chart(df_filterpot_pakchoi, x='Date', y='EC', color='#669999')
            with tabTemp:
                # st.scatter_chart(df_telemetery2, x='Datetime', y='value')
                # st.bar_chart(df_telemetery2, x='Datetime', y='value')
                figTemp = go.Figure()
                figTemp.add_trace(
                    go.Scatter(x=df_telemetery2['Datetime'], y=df_telemetery2['value'],
                               name='pH', mode='lines', line=dict(color='orange')))
                figTemp.update_layout(
                    title='Temperature Over Time',
                    xaxis_title='Date',
                    yaxis_title='Temp °C',
                )
                st.plotly_chart(figTemp)

            st.divider()
            st.subheader('Growth')

            # Convert 'Date' column to datetime format
            df_pakchoi['Date'] = pd.to_datetime(df_pakchoi['Date'], format='%d/%m/%Y', errors='coerce',
                                                infer_datetime_format=True)

            # Create a Streamlit date range picker
            date_range = st.date_input('Select Date Range:',
                                       value=[(datetime.datetime.now() - datetime.timedelta(days=7)).date(),
                                              datetime.datetime.now().date()])

            # Convert selected date range to datetime format
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

            # Filter data based on the selected date range
            filtered_data = df_pakchoi[(df_pakchoi['Date'] >= start_date) & (df_pakchoi['Date'] <= end_date)]

            # Group the filtered data
            groupedPot = filtered_data.groupby('Pot')[['Plant Height(mm)', 'Longest Leaf']].mean().reset_index()

            # Create a Plotly figure
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=groupedPot['Pot'], y=groupedPot['Plant Height(mm)'],
                name='Plant Height',
                marker_color='#1f77b4',
                hovertemplate='Pot %{x}<br>Plant Height: %{y:.3f} mm'
            ))
            fig.add_trace(go.Bar(
                x=groupedPot['Pot'], y=groupedPot['Longest Leaf'],
                name='Longest Leaf',
                marker_color='#ff7f0e',
                hovertemplate='Pot %{x}<br>Longest Leaf: %{y:.3f} mm'
            ))

            # Update layout
            fig.update_layout(
                title=f'Average Plant Height and Longest Leaf by Pot ({start_date.date()} to {end_date.date()})',
                xaxis_title='Pot',
                yaxis_title='Average Value',
                barmode='group',  # Group bars for each Pot
                template='plotly_dark',  # Set dark mode template
            )

            # Show the Plotly figure in your Streamlit app
            st.plotly_chart(fig, use_container_width=True)

            # Group the data for 'SubPot' within the selected date range
            groupedSubPot = filtered_data.groupby('SubPot')[['Plant Height(mm)', 'Longest Leaf']].mean().reset_index()

            # Create a Plotly figure
            fig = go.Figure()

            # Add bar traces for Plant Height and Longest Leaf
            # Add bar traces for Plant Height and Longest Leaf with custom hover text
            fig.add_trace(go.Bar(
                x=groupedSubPot['SubPot'],
                y=groupedSubPot['Plant Height(mm)'],
                name='Plant Height',
                marker_color='#1f77b4',
                hovertemplate='SubPot %{x}<br>Plant Height: %{y:.3f} mm'
            ))
            fig.add_trace(go.Bar(
                x=groupedSubPot['SubPot'],
                y=groupedSubPot['Longest Leaf'],
                name='Longest Leaf',
                marker_color='#ff7f0e',
                hovertemplate='SubPot %{x}<br>Longest Leaf: %{y:.3f} mm'
            ))

            # Update layout
            fig.update_layout(
                title=f'Average Plant Height and Longest Leaf by Sub-Pot ({start_date.date()} to {end_date.date()})',
                xaxis_title='Sub-Pot',
                yaxis_title='Average Value',
                barmode='group',  # Group bars for each Sub-Pot
                template='plotly_dark',  # Set dark mode template
            )

            # Show the Plotly figure in your Streamlit app
            st.plotly_chart(fig, use_container_width=True)



