import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel
from models.farm_model import get_telemetries
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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
        st.dataframe(df_home.iloc[:, 0:5])

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
                    <div class="card" style="width: auto;">
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
                    <div class="card" style="width: auto;">
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
                    <div class="card" style="width: auto;">
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
                    <div class="card" style="width: auto;">
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
                    <div class="card" style="width: auto;">
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

            groupedPot = df_pakchoi.groupby('Pot')[['Plant Height(mm)', 'Longest Leaf']].mean()

            # Create a Matplotlib figure and axis
            fig, ax = plt.subplots(figsize=(6, 3))

            # Set the background color of the Matplotlib plot to #F0F8EA
            ax.set_facecolor('#F0F8EA')
            fig.set_facecolor('#F0F8EA')

            # Plot the results
            groupedPot.plot(kind='bar', ax=ax)
            plt.title('Average Plant Height and Longest Leaf by Pot')
            plt.xlabel('Pot')
            plt.ylabel('Average Value')
            plt.xticks(rotation=0)  # Rotate x-axis labels if needed
            plt.legend(loc='best')  # Show the legend

            # Display the Matplotlib plot in your Streamlit app
            st.pyplot(fig)


            groupedSubPot = df_pakchoi.groupby('SubPot')[['Plant Height(mm)', 'Longest Leaf']].mean()

            # Create a Matplotlib figure and axis
            fig, ax = plt.subplots(figsize=(6, 3))

            # Set the background color of the Matplotlib plot to #F0F8EA
            ax.set_facecolor('#F0F8EA')
            fig.set_facecolor('#F0F8EA')

            # Plot the results
            groupedSubPot.plot(kind='bar', ax=ax)
            print(groupedSubPot)
            plt.title('Average Plant Height and Longest Leaf by Sub-Pot')
            plt.xlabel('Sub-Pot')
            plt.ylabel('Average Value')
            # Define the x-label locations and labels (show every second label)
            x_labels = groupedSubPot.index[::2]  # Select every second label
            x_locations = range(0, len(groupedSubPot), 2)  # Corresponding x-locations
            # Set the x-labels and their positions
            plt.xticks(x_locations, x_labels)
            plt.xticks(rotation=0)  # Rotate x-axis labels if needed
            plt.xticks(fontsize=6)
            plt.legend(loc='best')  # Show the legend

            # Display the Matplotlib plot in your Streamlit app
            st.pyplot(fig)

            # fig = go.Figure()
            # fig.add_trace(go.Bar(x=groupedPot.index,
            #                      y=groupedPot['Plant Height(mm)'],
            #                      name='Average Plant Height (mm)'))
            # fig.add_trace(go.Bar(x=groupedPot.index,
            #                      y=groupedPot['Longest Leaf'],
            #                      name='Average Longest Leaf'))
            #
            # fig.update_layout(barmode='group',
            #                   xaxis_title='Pot',
            #                   yaxis_title='Average Value',
            #                   title='Average Plant Height and Longest Leaf by Pot')
            #
            # iplot(fig)


            # col111, col222 = st.columns(2)
            # with col111:
            #     fig = go.Figure()
            #     fig.add_trace(go.Scatter(x=df_filterpot_pakchoi['Date'], y=df_filterpot_pakchoi['Plant Height(mm)'], name='Plant Height', mode='lines',
            #                              line=dict(color='blue')))
            #     fig.add_trace(go.Scatter(x=df_filterpot_pakchoi['Date'], y=df_filterpot_pakchoi['Longest Leaf'], name='Longest Leaf', mode='lines',
            #                              line=dict(color='green'), yaxis='y2'))
            #
            #     fig.update_layout(
            #         title='Plant Height and Longest Leaf (mm) Progress',
            #         xaxis_title='Date',
            #         yaxis_title='Plant Height',
            #         yaxis2=dict(
            #             title='Longest Leaf',
            #             overlaying='y',
            #             side='right'
            #         )
            #     )
            #     st.plotly_chart(fig)
            #
            # with col222:
            #     # st.line_chart(df_filtersubpot_pakchoi, x='Date', y=['pH', 'EC'])
            #     fig2 = go.Figure()
            #     fig2.add_trace(
            #         go.Scatter(x=df_filterpot_pakchoi['Date'], y=df_filterpot_pakchoi['pH'],
            #                    name='pH', mode='lines',
            #                    line=dict(color='orange')))
            #     fig2.add_trace(go.Scatter(x=df_filterpot_pakchoi['Date'], y=df_filterpot_pakchoi['EC'],
            #                              name='EC', mode='lines',
            #                              line=dict(color='purple'), yaxis='y2'))
            #
            #     fig2.update_layout(
            #         title='pH and EC Over Time',
            #         xaxis_title='Date',
            #         yaxis_title='pH',
            #         yaxis2=dict(
            #             title='EC',
            #             overlaying='y',
            #             side='right'
            #         )
            #     )
            #     st.plotly_chart(fig2)


        # col = st.columns(3)
        # with col[0]:
        #
        #     if selected_farm == "Pok Choy Hydroponics":
        #         with col[1]:
        #             df_pakchoi = pd.DataFrame(pakchoi_model.get_actual_data())
        #             # df_pakchoi = df_pakchoi.rename(columns=df_pakchoi.iloc[0]).drop(df_pakchoi.index[0])
        #             # st.write(df_pakchoi)
        #             select_pot = st.selectbox("Select Pot", df_pakchoi['Pot'].unique())
        #         with col[2]:
        #             df_filterpot_pakchoi = df_pakchoi[df_pakchoi['Pot'] == select_pot]
        #             select_subpot = st.selectbox("Select SubPot", df_filterpot_pakchoi['SubPot'].unique())
        #             df_filtersubpot_pakchoi = df_filterpot_pakchoi[df_filterpot_pakchoi['SubPot'] == select_subpot]
        # # st.write(df_filtersubpot_pakchoi)
        # st.subheader("Growth Information:")
        # col1, col2, col3 = st.columns(3)
        #
        # if not df_filtersubpot_pakchoi.empty:
        #     # Convert the columns to numeric
        #     numeric_columns = ['Leaves Count', 'Longest Leaf', 'Plant Height(mm)', 'pH', 'EC']
        #     # df_filtersubpot_pakchoi[numeric_columns] = df_filtersubpot_pakchoi[numeric_columns].apply(pd.to_numeric)
        #     df_filtersubpot_pakchoi.loc[:, numeric_columns] = df_filtersubpot_pakchoi.loc[:, numeric_columns].apply(
        #         pd.to_numeric)
        #
        #     initial_data = df_filtersubpot_pakchoi[numeric_columns].iloc[0]
        #     latest_data = df_filtersubpot_pakchoi[numeric_columns].iloc[-1]
        #
        #     # Convert the difference to an accepted data type (string)
        #     leaves_count_diff = str(latest_data['Leaves Count'] - initial_data['Leaves Count'])
        #
        #     col1.metric("Latest Leaves Count", latest_data['Leaves Count'], leaves_count_diff)
        #     col2.metric("Longest Leaf", f"{latest_data['Longest Leaf']} mm")
        #     col3.metric("Plant Height", f"{latest_data['Plant Height(mm)']} mm")
        #     st.subheader("Nutrient Information")
        #     col11, col22, col33 = st.columns(3)
        #     #--- loc -2 temporary because I spotted empty value for the latest data especially these two ---
        #     col11.metric("pH", f"{df_filtersubpot_pakchoi['pH'].iloc[-2]}")
        #     col22.metric("EC", f"{df_filtersubpot_pakchoi['EC'].iloc[-2]}")
        #
        #     df_filtersubpot_pakchoi['Date'] = pd.to_datetime(df_filtersubpot_pakchoi['Date'], format='%d/%m/%Y', errors='coerce',
        #                                         infer_datetime_format=True)
        #
        #     col111, col222 = st.columns(2)
        #     with col111:
        #         fig = go.Figure()
        #         fig.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Plant Height(mm)'], name='Plant Height', mode='lines',
        #                                  line=dict(color='blue')))
        #         fig.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Longest Leaf'], name='Longest Leaf', mode='lines',
        #                                  line=dict(color='green'), yaxis='y2'))
        #
        #         fig.update_layout(
        #             title='Plant Height and Longest Leaf (mm) Progress',
        #             xaxis_title='Date',
        #             yaxis_title='Plant Height',
        #             yaxis2=dict(
        #                 title='Longest Leaf',
        #                 overlaying='y',
        #                 side='right'
        #             )
        #         )
        #         st.plotly_chart(fig)
        #
        #     with col222:
        #         # st.line_chart(df_filtersubpot_pakchoi, x='Date', y=['pH', 'EC'])
        #         fig2 = go.Figure()
        #         fig2.add_trace(
        #             go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['pH'],
        #                        name='pH', mode='lines',
        #                        line=dict(color='orange')))
        #         fig2.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['EC'],
        #                                  name='EC', mode='lines',
        #                                  line=dict(color='purple'), yaxis='y2'))
        #
        #         fig2.update_layout(
        #             title='pH and EC Over Time',
        #             xaxis_title='Date',
        #             yaxis_title='pH',
        #             yaxis2=dict(
        #                 title='EC',
        #                 overlaying='y',
        #                 side='right'
        #             )
        #         )
        #         st.plotly_chart(fig2)
        #
        #
        # else:
        #     st.write("No data available for the selected SubPot.")
        #



