import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel
import plotly.graph_objects as go

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

        column = st.columns(2)
        with column[0]:
            st.dataframe(df_home.iloc[:, 0:5])
        with column[1]:
            # Coordinates
            latitude = 2.992193566444384
            longitude = 101.72348426648746
            # latlong = pd.DataFrame({'LAT': [latitude], 'LON': [longitude]})
            # st.map(latlong)
            # Define the iframe HTML
            map_html = f'<iframe width="100%" height="350" src="https://www.openstreetmap.org/export/embed.html?bbox={longitude},{latitude},{longitude},{latitude}&layer=mapnik" frameborder="0"></iframe>'
            expander = st.expander("Farm Location", expanded=False)
            with expander:
                st.write(map_html, unsafe_allow_html=True)

        # ---------------------------
        def dataframe_with_selections(df):
            df_with_selections = df.copy()
            df_with_selections.insert(0, "Select", False)
            edited_df = st.data_editor(
                df_with_selections,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                disabled=df.columns,
            )
            selected_indices = list(np.where(edited_df.Select)[0])
            selected_rows = df[edited_df.Select]
            return {"selected_rows_indices": selected_indices, "selected_rows": selected_rows}

        # selection = dataframe_with_selections(df_home)
        # st.write("Your selection:")
        # st.write(selection)
        # ---------------------------

        farm_names = df_home["Farm Name"].tolist()
        col = st.columns(3)
        with col[0]:
            selected_farm = st.selectbox('Farm Name:', farm_names)
            df_selected_farm = df_home[df_home["Farm Name"] == selected_farm]
            if selected_farm == "Pok Choy Hydroponics":
                with col[1]:
                    df_pakchoi = pd.DataFrame(pakchoi_model.get_actual_data())
                    # df_pakchoi = df_pakchoi.rename(columns=df_pakchoi.iloc[0]).drop(df_pakchoi.index[0])
                    # st.write(df_pakchoi)
                    select_pot = st.selectbox("Select Pot", df_pakchoi['Pot'].unique())
                with col[2]:
                    df_filterpot_pakchoi = df_pakchoi[df_pakchoi['Pot'] == select_pot]
                    select_subpot = st.selectbox("Select SubPot", df_filterpot_pakchoi['SubPot'].unique())
                    df_filtersubpot_pakchoi = df_filterpot_pakchoi[df_filterpot_pakchoi['SubPot'] == select_subpot]
        # st.write(df_filtersubpot_pakchoi)
        st.subheader("Growth Information:")
        col1, col2, col3 = st.columns(3)

        if not df_filtersubpot_pakchoi.empty:
            # Convert the columns to numeric
            numeric_columns = ['Leaves Count', 'Longest Leaf', 'Plant Height(mm)', 'pH', 'EC']
            df_filtersubpot_pakchoi[numeric_columns] = df_filtersubpot_pakchoi[numeric_columns].apply(pd.to_numeric)

            initial_data = df_filtersubpot_pakchoi[numeric_columns].iloc[0]
            latest_data = df_filtersubpot_pakchoi[numeric_columns].iloc[-1]

            # Convert the difference to an accepted data type (string)
            leaves_count_diff = str(latest_data['Leaves Count'] - initial_data['Leaves Count'])

            col1.metric("Latest Leaves Count", latest_data['Leaves Count'], leaves_count_diff)
            col2.metric("Longest Leaf", f"{latest_data['Longest Leaf']} mm")
            col3.metric("Plant Height", f"{latest_data['Plant Height(mm)']} mm")
            st.subheader("Nutrient Information")
            col11, col22, col33 = st.columns(3)
            #--- loc -2 temporary because I spotted empty value for the latest data especially these two ---
            col11.metric("pH", f"{df_filtersubpot_pakchoi['pH'].iloc[-2]}")
            col22.metric("EC", f"{df_filtersubpot_pakchoi['EC'].iloc[-2]}")

            col111, col222 = st.columns(2)
            with col111:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Plant Height(mm)'], name='Plant Height', mode='lines',
                                         line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['Longest Leaf'], name='Longest Leaf', mode='lines',
                                         line=dict(color='green'), yaxis='y2'))

                fig.update_layout(
                    title='Plant Height and Longest Leaf (mm) Progress',
                    xaxis_title='Date',
                    yaxis_title='Plant Height',
                    yaxis2=dict(
                        title='Longest Leaf',
                        overlaying='y',
                        side='right'
                    )
                )
                st.plotly_chart(fig)

            with col222:
                # st.line_chart(df_filtersubpot_pakchoi, x='Date', y=['pH', 'EC'])
                fig2 = go.Figure()
                fig2.add_trace(
                    go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['pH'],
                               name='pH', mode='lines',
                               line=dict(color='orange')))
                fig2.add_trace(go.Scatter(x=df_filtersubpot_pakchoi['Date'], y=df_filtersubpot_pakchoi['EC'],
                                         name='EC', mode='lines',
                                         line=dict(color='purple'), yaxis='y2'))

                fig2.update_layout(
                    title='pH and EC Over Time',
                    xaxis_title='Date',
                    yaxis_title='pH',
                    yaxis2=dict(
                        title='EC',
                        overlaying='y',
                        side='right'
                    )
                )
                st.plotly_chart(fig2)


        else:
            st.write("No data available for the selected SubPot.")




