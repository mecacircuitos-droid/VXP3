import streamlit as st
from vxp.ui import init_state, route
from vxp.styles import XP_CSS
from vxp.toolbar import render_toolbar

def main():
    # "wide" + CSS (max-width: 1024) emula mejor el Toughbook XGA 4:3
    st.set_page_config(page_title="VXP Simulator – BO105", layout="wide")
    init_state()

    # Layout general (toolbar a la izquierda, ventana a la derecha)
    st.markdown(XP_CSS, unsafe_allow_html=True)
    # Barra lateral original ~81 px + bordes → dejamos un margen
    left, right = st.columns([0.13, 0.87], gap="small")

    with left:
        # Por ahora solo visual (sin funcionalidad)
        st.markdown("<div class='vxp-toolbar'>", unsafe_allow_html=True)
        render_toolbar(interactive=False)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        route()

if __name__ == "__main__":
    main()
