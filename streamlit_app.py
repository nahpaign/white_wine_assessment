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
    free_so2 = st.sidebar.text_input("free sulfur dioxide", placeholder=">= 1")
    ttl_so2 = st.sidebar.text_input("total sulfur dioxide", placeholder=">= 1")
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
    st.title("Welcome to White Wine Quality Assessment!")

    if st.session_state.get('input_features'):  # only runs if dict is non-empty
        try:
            prediction = get_prediction(**st.session_state['input_features'])

            if prediction >= 8:
                st.success("🏆 **Excellent!** World-class wine!")
                st.markdown("## 🍾🥂🌟")
                st.balloons()
            elif prediction >= 6:
                st.info("👍 **Not Bad!** A solid, enjoyable wine.")
                st.markdown("## 🍷😊")
            elif prediction >= 5:
                st.warning("😐 **Meh.** Drinkable, but nothing special.")
                st.markdown("## 🍶🤷")
            else:
                st.error("🤢 **Gross!** Pour it down the drain.")
                st.markdown("## 🪣😬")

            st.markdown(f"**Predicted Quality Score:** `{prediction:.2f} / 10`")

        except (ValueError, KeyError):
            st.warning("⚠️ Please enter valid numeric values for all fields.")

def main():
    if 'input_features' not in st.session_state:
        st.session_state['input_features'] = {}
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()