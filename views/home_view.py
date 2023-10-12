import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

class HomeView:
    def __init__(self, home_model):
        self.home_model = home_model

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

        df_home = self.home_model.get_data()

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

        col = st.columns([2, 1])
        with col[0]:
            cols_name = ["Farm_No", "Crop name", "Size", "Actual yield", "Yield goal", "Estimated Yield"]
            # Apply cell styles to the DataFrame
            styled_df = df_home[cols_name].style.apply(self.style_cell, axis=1)
            st.dataframe(styled_df, hide_index=True)

        with col[1]:
            # Add legend
            st.markdown("Legend:")
            st.markdown('<div style="display: flex; align-items: center;">'
                        '<div style="width: 20px; height: 20px; background-color: green; border-radius: 50%;"></div>'
                        '<span style="margin-left: 10px;">Your farm is in a good state and you will highly likely reach your yield goal</span>'
                        '</div>', unsafe_allow_html=True)
            st.markdown('<div style="display: flex; align-items: center;">'
                        '<div style="width: 20px; height: 20px; background-color: orange; border-radius: 50%;"></div>'
                        '<span style="margin-left: 10px;">Your farm needs more nutrition so you can reach your goal</span>'
                        '</div>', unsafe_allow_html=True)
            st.markdown('<div style="display: flex; align-items: center;">'
                        '<div style="width: 20px; height: 20px; background-color: red; border-radius: 50%;"></div>'
                        '<span style="margin-left: 10px;">Your farm has a severe malnutrition problem and is very far from reaching your yield goal</span>'
                        '</div>', unsafe_allow_html=True)

        # farm_number = st.selectbox('Farm number:', df_home.index)
        # df_selected_farm = df_home.loc[farm_number]
        farm_numbers = df_home["Farm_No"].tolist()
        selected_farm_number = st.selectbox('Farm number:', farm_numbers)
        df_selected_farm = df_home[df_home["Farm_No"] == selected_farm_number]

        # image_savename = df_selected_farm["image"]
        image_savename = df_selected_farm.iloc[0]["image"]
        image_path = f'assets/{image_savename}'
        location_savename = df_selected_farm.iloc[0]["mapabove"]
        location_path = f'assets/{location_savename}'
        coll = st.columns(2)
        with coll[0]:
            try:
                image = Image.open(image_path)
                st.image(image, use_column_width="auto", caption="Rice with sufficient nutrients")
            except FileNotFoundError:
                st.error(f"Image file '{image_path}' not found.")
        with coll[1]:
            try:
                image = Image.open(location_path)
                st.image(image, use_column_width="auto", caption="Farm 1 Map Snap")
            except FileNotFoundError:
                st.error(f"Image file '{location_path}' not found.")