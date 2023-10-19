import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from models.rice_model import RiceModel
from models.pakchoi_model import PakchoiModel

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
        else:
            st.write("No data available for the selected SubPot.")




