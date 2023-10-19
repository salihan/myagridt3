# app.py

from models.user_model import UserModel
# from models.home_model import HomeModel
from models.pakchoi_model import PakchoiModel
# from models.rice_model import RiceModel
from views.login_view import LoginView
# from views.home_view import HomeView
from models.home_model2 import HomeModel2
from views.home2_view import Home2View
# from views.rice_view import RiceView
from views.report_view import ReportView
import streamlit as st

# Instantiate models
user_model = UserModel("admin", "password")
# home_model = HomeModel()
home_model2 = HomeModel2()
# rice_model = RiceModel()
pakchoi_model = PakchoiModel()

# Instantiate views
login_view = LoginView(user_model)
home2_view = Home2View(home_model2)
# rice_view = RiceView(rice_model)
report_view = ReportView(home_model2)


# Set up Streamlit app
def main():
    st.sidebar.title("MyAgriDT")

    # Display login/logout based on user authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        if login_view.render():
            st.session_state.authenticated = True
    else:
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.experimental_rerun()

        # Highlight the selected button
        selected_button = st.sidebar.radio(
            "Navigation",
            ("🏠Home", "🌾Report", "📋Action Plan")
        )

        # Render views based on the selected button
        if selected_button == "🏠Home":
            # Apply style for the selected button
            st.markdown(
                '<style>.css-1m8ugwa-Button:nth-child(1){background-color: #f63366 !important; color: white;}</style>',
                unsafe_allow_html=True)
            home2_view.render()
        elif selected_button == "🌾Report":
            # Apply style for the selected button
            st.markdown(
                '<style>.css-1m8ugwa-Button:nth-child(2){background-color: #f63366 !important; color: white;}</style>',
                unsafe_allow_html=True)
            # rice_view.render()
            report_view.render()


if __name__ == '__main__':
    st.set_page_config(
        page_title='MyAgriDt',
        layout='wide',
        page_icon='🥦'
    )

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # reduce spaces on content area
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                        padding-left: 3rem;
                        padding-right: 3rem;
                    }
            </style>
            """, unsafe_allow_html=True)

    # metrics_style = """
    #         <style>
    #             .css-ocqkz7 {
    #                 border: 2px solid #007ACC;
    #                 border-radius: 5px;
    #                 padding: 10px;
    #             }
    #         </style>
    #     """
    # st.markdown(metrics_style, unsafe_allow_html=True)

    main()
