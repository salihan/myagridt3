import streamlit as st
from models.farm_model import get_telemetries
import pandas as pd
import plotly.graph_objects as go

class FarmView:
    def render(self):
        st.title("Farm Telemetries Live Transmission")

        # Define user interface components
        device_unique_id = st.selectbox("Device Unique ID", ["UPMSO1001", "UPMSO2001"])
        # telemetry_type_code = st.multiselect(
        #     "Telemetry Type Code (optional)",
        #     ["waterPh", "waterOrp", "waterTemperature", "waterEc", "waterSr", "waterSalinity", "waterTds"],
        #     ["waterPh"]  # Default selection
        # )
        telemetry_type_code = st.selectbox(
            "Telemetry Type Code",
            ["waterPh", "waterOrp", "waterTemperature", "waterEc", "waterSr", "waterSalinity", "waterTds"]
        )

        # Date pickers for date_start and date_end
        date_start = st.date_input("Start Date (optional)", None)
        date_end = st.date_input("End Date (optional)", None)

        if st.button("Fetch Telemetries"):
            self.fetch_telemetries(device_unique_id, telemetry_type_code, date_start, date_end)

    def fetch_telemetries(self, device_unique_id, telemetry_type_code, date_start, date_end):
        fig = go.Figure()
        try:
            telemetries = get_telemetries(device_unique_id, telemetry_type_code, date_start, date_end)

            if telemetries:
                # Create a DataFrame from the API response
                df = pd.DataFrame(telemetries['data'])

                st.subheader(f"Telemetry: {telemetry_type_code}")

                if not df.empty:
                    col = st.columns([2, 1])
                    with col[0]:
                        # Convert 'readingAt' to datetime
                        df['Datetime'] = pd.to_datetime(df['readingAt'])
                        # df.set_index('readingAt', inplace=True)

                        fig.add_trace(go.Scatter(x=df['Datetime'], y=df['value']))
                        st.plotly_chart(fig)
                        # st.line_chart(df, x="Datetime", y="value", width=400, height=400)
                    with col[1]:
                        st.write(df[['readingAt', 'value']])
                else:
                    st.write(f"No data available for {telemetry_type_code}.")
            else:
                st.error("No telemetry data available for the specified parameters.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
