import streamlit as st
from src.inference import get_prediction
from src.config import appconfig


def app_sidebar():
    st.sidebar.header('Wine Attributes')
    fixed_acidity = st.sidebar.text_input("fixed acidity", placeholder=">= 1")
    volatile_acidity = st.sidebar.text_input("volatile acidity")
    citric_acid = st.sidebar.text_input("citric acid")
    residual_sugar = st.sidebar.text_input("residual sugar", placeholder=">= 1")
    chlorides = st.sidebar.text_input("chlorides", placeholder="< 1")
    free_so2 = st.sidebar.text_input("free sulphur dioxide", placeholder=">= 1")
    ttl_so2 = st.sidebar.text_input("total sulphur dioxide", placeholder=">= 1")
    density = st.sidebar.text_input("density", placeholder="g/ml")
    pH = st.sidebar.text_input("pH", placeholder="1-14")
    sulphates = st.sidebar.text_input("sulphates")
    alcohol = st.sidebar.text_input("alcohol", placeholder="in %")
    def get_input_features():
        input_features = {'fixed acidity': float(fixed_acidity),
                          'volatile acidity': float(volatile_acidity),
                          'citric acid': float(citric_acid),
                          'residual sugar': float(residual_sugar),
                          'chlorides': float(chlorides),
                          'free sulfur dioxide': float(free_so2),
                          'total sulfur dioxide': float(ttl_so2),
                          'density': float(density),
                          'pH': float(pH),
                          'sulphates': float(sulphates),
                          'alcohol': float(alcohol)
                         }
        return input_features
    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Assess", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")
    if predict_button:
        st.session_state['input_features'] = get_input_features()
    if reset_button:
        st.session_state['input_features'] = {}
    return None

def app_body():
    title = '<p style="font-family:arial, sans-serif; color:Black; font-size: 40px;"><b> Welcome to White Wine Quality Assessment!</b></p>'
    st.markdown(title, unsafe_allow_html=True)
    default_msg = '**System assessment says:** {}'
    if st.session_state['input_features']:
        quality = get_prediction(**st.session_state['input_features'])
        if quality >= 8:
            st.success(default_msg.format('Excellent choice!'))
        elif quality < 8 and quality >=6:
            st.success(default_msg.format('Not too bad!'))
        elif quality < 6 and quality >= 5:
            st.success(default_msg.format('Mehhhhhhh'))
        else:
            st.warning(default_msg.format('Grossssssssss'))
    return None

def main():
    if 'input_features' not in st.session_state:
        st.session_state['input_features'] = {}
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()