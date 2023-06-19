import streamlit as st
import pandas as pd

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
        st.title('Farm Name: MyAgriDt')

        df_home = self.home_model.get_data()
        # Apply cell styles to the DataFrame
        styled_df = df_home.style.apply(self.style_cell, axis=1)

        # Display the styled DataFrame in Streamlit
        st.write(styled_df, unsafe_allow_html=True)

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
