import streamlit as st

from vxp.styles import XP_CSS
from vxp.toolbar import render_toolbar
from vxp.ui import init_state, route, apply_nav


def main():
    # Objetivo: estética VXP original (Windows XP / industrial) en 1024x768 (4:3)
    st.set_page_config(page_title="Chadwick-Helmuth VXP", layout="wide")

    init_state()

    # Navegación por querystring: ?nav=viewlog / help / etc.
    apply_nav()

    st.markdown(XP_CSS, unsafe_allow_html=True)

    # Metadatos de cabecera (como el original)
    st.session_state.setdefault("vxp_aircraft", "BO105")
    st.session_state.setdefault("vxp_aircraft_id", "N74678D")

    title = f"Chadwick-Helmuth VXP  —  {st.session_state.vxp_aircraft}   ID: {st.session_state.vxp_aircraft_id}"

    # ----- MAIN SHELL (ventana principal) -----
    st.markdown("<div class='vxp-mainframe'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='vxp-main-titlebar'>"
        f"<div>{title}</div>"
        "<div class='vxp-winbtns'>"
        "<div class='vxp-winbtn'>_</div>"
        "<div class='vxp-winbtn'>□</div>"
        "<div class='vxp-winbtn'>✕</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='vxp-main-menubar'>"
        "<span>File</span>"
        "<a href='?nav=viewlog'>View Log</a>"
        "<a href='?nav=test_au'>Test AU</a>"
        "<a href='?nav=settings'>Settings</a>"
        "<a href='?nav=help'>Help</a>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='vxp-main-body'>", unsafe_allow_html=True)

    # Left dock: smart icon bar
    st.markdown("<div class='vxp-leftdock'>", unsafe_allow_html=True)
    render_toolbar(interactive=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Desktop: child windows
    st.markdown("<div class='vxp-desktop'>", unsafe_allow_html=True)
    route()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end main-body

    # Status bar
    st.markdown(
        "<div class='vxp-statusbar'>"
        "<div>READY</div>"
        "<div>DISPLAY: 1024×768 (4:3)</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # end mainframe


if __name__ == "__main__":
    main()
