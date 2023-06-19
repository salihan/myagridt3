# app.py

from models.user_model import UserModel
from models.home_model import HomeModel
from models.rice_model import RiceModel
from views.login_view import LoginView
from views.home_view import HomeView
from views.rice_view import RiceView
import streamlit as st

# Instantiate models
user_model = UserModel("admin", "password")
home_model = HomeModel()
rice_model = RiceModel()

# Instantiate views
login_view = LoginView(user_model)
home_view = HomeView(home_model)
rice_view = RiceView(rice_model)


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
            ("Home", "Rice Dashboard")
        )

        # Render views based on the selected button
        if selected_button == "Home":
            # Apply style for the selected button
            st.markdown(
                '<style>.css-1m8ugwa-Button:nth-child(1){background-color: #f63366 !important; color: white;}</style>',
                unsafe_allow_html=True)
            home_view.render()
        elif selected_button == "Rice Dashboard":
            # Apply style for the selected button
            st.markdown(
                '<style>.css-1m8ugwa-Button:nth-child(2){background-color: #f63366 !important; color: white;}</style>',
                unsafe_allow_html=True)
            rice_view.render()


if __name__ == '__main__':
    st.set_page_config(
        page_title='MyAgriDt',
        layout='wide',
        page_icon=':rocket:'
    )

    main()
