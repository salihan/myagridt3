import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from annotated_text import annotated_text, annotation
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import random
from st_aggrid import AgGrid
from PIL import Image

class RiceView:
    def __init__(self, rice_model):
        self.rice_model = rice_model

    def render(self):
        df_raw_rice = self.rice_model.get_data()
        totplot = df_raw_rice['Plot'].nunique()
        # print(df_raw_rice.columns)

        # selected_week = st.sidebar.selectbox("Select Week", df_raw_rice['week'].unique())
        # df_rice = df_raw_rice[df_raw_rice['week'] == selected_week]
        # Get unique weeks from the dataframe
        unique_weeks = df_raw_rice['week'].unique()

        # Add "All Weeks" as the default option at the beginning
        unique_weeks = ["All Weeks"] + list(unique_weeks)

        # Create the select box with the default option set to "All Weeks"
        selected_week = st.sidebar.selectbox("Select Week", unique_weeks)

        # Filter the dataframe based on the selected week
        if selected_week == "All Weeks":
            df_rice = df_raw_rice  # Show all data
        else:
            df_rice = df_raw_rice[df_raw_rice['week'] == selected_week]  # Filter data by selected week

        cc = st.columns([1,2])
        with cc[0]:
            image = Image.open('assets/padi.jpeg')
            st.image(image.resize((400, 300)), caption="Rice with sufficient nutrients")
            ccc = st.columns(2)
            with ccc[0]:
                annotated_text("", annotation("Size: 2 ha", "", font_family="Comic Sans MS", border="2px solid green"),
                               "", annotation(f"Total Plot: **{totplot}**", "", font_family="Comic Sans MS",
                                              border="2px solid green"), )
                st.markdown("""
                                    <style>
                                    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
                                        gap: 0.5rem;
                                    }
                                    </style>
                                    """, unsafe_allow_html=True)
                annotated_text("Avg. Plant Height: ", ("120", "cm", "#8ef"), )
                annotated_text("Avg. No. of Tiller: ", ("10", "", "#afa"), )
                annotated_text("Avg. No. of Unfilled Grain: ", ("504", ""), )

            with ccc[1]:
                annotated_text("",
                               annotation("Yield Goal: 50", "kg", font_family="Comic Sans MS", border="2px solid #8FD834"),
                               "", annotation("Estimated Yield: 45", "kg", font_family="Comic Sans MS",
                                              border="2px solid #72CC50"), )
                st.metric("Yield", "45 kg", "-5 kg")


        with cc[1]:

            # Create a dataframe with WeightGrain distribution over Plot and SubPlot
            df_weight_grain = df_rice.groupby(['Plot', 'SubPlot'])['WeightGrain'].mean().reset_index()

            # # Create the WeightGrain distribution chart
            # fig = px.bar(df_weight_grain, x='Plot', y='WeightGrain', color='SubPlot',
            #              labels={'WeightGrain': 'Weight Grain', 'Plot': 'Plot', 'SubPlot': 'SubPlot'},)
            #
            # # Change the color theme
            # # fig.update_traces(marker_color=px.colors.sequential.Viridis)
            # fig.update_layout(height=300, margin=dict(l=0, r=10, t=30, b=0), font=dict(size=10, color="RebeccaPurple"))
            # Combine Plot and SubPlot labels for x-axis
            df_weight_grain['x_labels'] = df_weight_grain['Plot'].astype(str) + '-' + df_weight_grain['SubPlot'].astype(
                str)

            # Create a bar chart for each SubPlot within each Plot
            fig = go.Figure()

            for plot in df_weight_grain['Plot'].unique():
                df_plot = df_weight_grain[df_weight_grain['Plot'] == plot]
                fig.add_trace(go.Bar(x=df_plot['x_labels'], y=df_plot['WeightGrain'], name=f'Plot {plot}'))

            # Customize the chart layout
            fig.update_layout(
                barmode='group',
                xaxis_title='Plot-SubPlot',
                yaxis_title='Weight Grain',
                showlegend=True
            )

            # Set the default expander state to expanded
            expander = st.expander("WeightGrain Mean Distribution", expanded=True)

            # Display the chart inside the expander
            with expander:
                st.plotly_chart(fig)

            # Create a dataframe with soil nutrient data over Plot
            df_soil_nutrients = df_rice.groupby('Plot')[['N', 'K', 'Mg', 'Ca']].mean().reset_index()

            # Create a bar chart for soil nutrient data
            fig2 = go.Figure()

            for nutrient in ['N', 'K', 'Mg', 'Ca']:
                fig2.add_trace(go.Bar(x=df_soil_nutrients['Plot'], y=df_soil_nutrients[nutrient], name=nutrient))

            # Customize the chart layout
            fig2.update_layout(
                barmode='group',
                xaxis_title='Plot',
                yaxis_title='Soil Nutrient Level',
                title='Soil Nutrients over Plot',
                showlegend=True
            )

            # Set the default expander state to expanded
            expander = st.expander("Soil Nutrients Mean")

            # Display the chart inside the expander
            with expander:
                st.plotly_chart(fig2)


            data = pd.DataFrame({
                'Plot': ['1', '2', '3', '4', '5', '6', '7', '8'],
                'Yield': [8.5, 7.2, 6.8, 9.1, 10.1, 11.2, 12.3, 14.4],
                'Latitude': [3.0080, 3.0120, 3.0192, 3.0090, 3.0154, 3.0220, 3.0154, 3.0220],
                'Longitude': [101.6399, 101.6392, 101.6443, 101.6495, 101.6367, 101.6360, 101.6500, 101.6485]
            })

            # Create a function to generate the map
            def generate_map():
                # Create a folium map centered around the average latitude and longitude
                center_lat, center_long = data['Latitude'].mean(), data['Longitude'].mean()
                # Customize the folium map object to hide labels
                map_plot = folium.Map(
                    location=[center_lat, center_long],
                    zoom_start=15,
                    control_scale=True,
                    no_touch=True,
                    prefer_canvas=True
                )

                # Add markers for each sub-area
                for _, row in data.iterrows():
                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=f"Plot: {row['Plot']} \nYield: {row['Yield']}",
                        icon=folium.Icon(color='blue')
                    ).add_to(map_plot)

                # Return the folium map object
                return map_plot

            # Create an expander for the map visualization
            with st.expander("Map of Rice Plots"):
                # Generate and display the map using folium_static
                folium_static(generate_map())

            # Group the data by 'Plot' and calculate the sum of 'WeightGrain'
            weight_grain_sum = df_rice.groupby('Plot')['WeightGrain'].sum().reset_index()
            # Create a pie chart using plotly express
            fig = px.pie(weight_grain_sum, values='WeightGrain', names='Plot')

            with st.expander("WeightGrain Distribution over Plot"):
                st.plotly_chart(fig)


        tab1, tab2, tab3, tab4  = st.tabs(["All Data :seedling:", "Plot at Risk :camping:",  "Growth :chart:", "teest"])

        with tab1:
            col = st.columns([1,2])
            with col[0]:
                average_weight_grain = df_rice.groupby('Plot')['WeightGrain'].mean().reset_index()

                # Function to determine 'at_risk' based on average weight grain
                def determine_risk(weight_grain):
                    if weight_grain < 3.0:
                        return 'high risk'
                    elif weight_grain > 3.0 and weight_grain < 4.0:
                        return 'no'
                    else:
                        return 'low'

                # Apply the function to add 'at_risk' column
                average_weight_grain['at_risk'] = average_weight_grain['WeightGrain'].apply(determine_risk)

                # Display the result with styling
                styled_average_weight_grain = average_weight_grain.style.apply(
                    lambda row: [
                        'color: red' if row['at_risk'] == 'high risk'
                        else 'color: green' if row['at_risk'] == 'no' else 'color: blue'
                        for _ in row
                    ], axis=1
                )

                # Display the styled DataFrame
                st.dataframe(styled_average_weight_grain)

            with col[1]:
                # Allow the user to select a plot
                selected_plot = st.selectbox("Select a plot to see subplots:", average_weight_grain['Plot'])

                # Check if a plot is selected
                if selected_plot:
                    # Filter the df_rice DataFrame for the selected plot
                    selected_data = df_rice[df_rice['Plot'] == selected_plot][
                        ['SubPlot', 'plantHeight', 'NoOfTiller', 'NoOfPanicle', 'SPAD', 'NoOfSpikelet', 'NoOfFilledGrain']]

                    # Display the selected data
                    st.write(selected_data)

        with tab2:
            df_risk = average_weight_grain[average_weight_grain['at_risk'] == 'high risk']

            # Define a function to provide recommendations based on risk level
            def get_recommendation():
                high_risk_recommendations = [
                    'Increase fertilizer application and improve soil moisture',
                    'Implement pest control measures and monitor closely',
                    'Optimize irrigation practices and provide adequate drainage',
                    'Consider using resistant crop varieties and adjust planting density'
                ]
                return random.choice(high_risk_recommendations)

            # Add the 'recommendation' column to df_risk
            df_risk['recommendation'] = df_risk['at_risk'].apply(lambda x: get_recommendation())

            st.write(df_risk)

        with tab3:
            cctab3 = st.columns(3)
            with cctab3[0]:
                # Group the data by 'Plot' and calculate the mean of 'plantHeight'
                average_height = df_rice.groupby('Plot')['plantHeight'].mean()

                # Create a bar plot of average plantHeight over Plot
                plt.figure(figsize=(10, 6))
                average_height.plot(kind='bar')
                plt.xlabel('Plot')
                plt.ylabel('Average plantHeight')
                plt.title('Average plantHeight over Plot')
                plt.xticks(rotation=45)
                st.pyplot(plt)

            with cctab3[1]:
                # Group the data by 'Plot' and calculate the mean of 'plantHeight'
                average_NoOfTiller = df_rice.groupby('Plot')['NoOfTiller'].mean()

                # Create a bar plot of average plantHeight over Plot
                plt.figure(figsize=(10, 6))
                average_NoOfTiller.plot(kind='bar')
                plt.xlabel('Plot')
                plt.ylabel('Average NoOfTiller')
                plt.title('Average NoOfTiller over Plot')
                plt.xticks(rotation=45)
                st.pyplot(plt)

            with cctab3[2]:
                # Group the data by 'Plot' and calculate the mean of 'plantHeight'
                average_NoOfFilledGrain = df_rice.groupby('Plot')['NoOfFilledGrain'].mean()

                # Create a bar plot of average plantHeight over Plot
                plt.figure(figsize=(10, 6))
                average_NoOfFilledGrain.plot(kind='bar')
                plt.xlabel('Plot')
                plt.ylabel('Average NoOfFilledGrain')
                plt.title('Average NoOfFilledGrain over Plot')
                plt.xticks(rotation=45)
                st.pyplot(plt)

        with tab4:
            st.write('tab4')
            # Group the data by 'Plot' and calculate the mean of 'WeightGrain'
            average_weight_grain = df_rice.groupby('Plot')['WeightGrain'].mean().reset_index()

            # Function to determine 'at_risk' based on average weight grain
            def determine_risk(weight_grain):
                if weight_grain < 3.0:
                    return 'high risk'
                elif weight_grain > 3.0 and weight_grain < 4.0:
                    return 'no'
                else:
                    return 'low'

            # Apply the function to add 'at_risk' column
            average_weight_grain['at_risk'] = average_weight_grain['WeightGrain'].apply(determine_risk)

            # Display the result with styling
            styled_data = average_weight_grain.style.apply(
                lambda row: [
                    'color: red' if row['at_risk'] == 'high risk'
                    else 'color: green' if row['at_risk'] == 'no' else 'color: blue'
                    for _ in row
                ], axis=1
            )

            # Convert the styled DataFrame to a regular DataFrame
            data = pd.DataFrame(styled_data.data)

            # Display the DataFrame using ag-Grid
            grid_result = AgGrid(data, fit_columns_on_grid_load=True)

            # Get the selected rows from the grid_result object
            selected_rows = grid_result['selected_rows']

            # Get the selected plots
            selected_plots = [row['Plot'] for row in selected_rows]

            # Filter the df_rice DataFrame for the selected plots
            filtered_data = df_rice[df_rice['Plot'].isin(selected_plots)]

            # Display the additional information for the selected plots
            if len(filtered_data) > 0:
                st.subheader("Additional Information for Selected Plots")
                st.dataframe(filtered_data[['Plot', 'plantHeight', 'NoOfTiller', 'NoOfPanicle', 'SPAD', 'NoOfSpikelet',
                                            'NoOfFilledGrain']])
            else:
                st.info("No data available for the selected plots.")
