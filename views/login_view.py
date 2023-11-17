from PIL import Image
import streamlit as st

class LoginView:
    def __init__(self, user_model):
        self.user_model = user_model

    def render(self):
        image = Image.open('assets/logo.png')
        st.image(image.resize((350, 125)))
        st.title('Login')

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if self.user_model.authenticate(username, password):
                st.success('Login successful!')
                return True
            else:
                st.error('Invalid username or password.')
        return False
