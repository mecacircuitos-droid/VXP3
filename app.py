import streamlit as st

from vxp.styles import XP_CSS
from vxp.toolbar import render_toolbar
from vxp.ui import init_state, route, apply_nav


def main() -> None:
    # Objetivo: réplica visual VXP (Windows XP clásico) en XGA 1024×768 (4:3)
    st.set_page_config(page_title="Chadwick-Helmuth VXP", layout="wide")
    init_state()
    apply_nav()

    st.markdown(XP_CSS, unsafe_allow_html=True)

    # Cabecera (como el original)
    st.session_state.setdefault("vxp_aircraft", "AS350B1")
    st.session_state.setdefault("vxp_aircraft_id", "Untitled")
    title = f"Chadwick-Helmuth VXP  —  {st.session_state.vxp_aircraft}   ID: {st.session_state.vxp_aircraft_id}"

    # Ventana principal fija 1024×768
    st.markdown("<div class='vxp-mainframe'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='vxp-main-titlebar'>"
        f"<div class='vxp-main-title'>{title}</div>"
        "<div class='vxp-winbtns'>"
        "<div class='vxp-winbtn'>_</div>"
        "<div class='vxp-winbtn'>□</div>"
        "<div class='vxp-winbtn'>✕</div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Menú superior
    st.markdown(
        "<div class='vxp-main-menubar'>"
        "<span class='vxp-menu-item'>File</span>"
        "<a class='vxp-menu-item' href='?nav=viewlog'>View Log</a>"
        "<a class='vxp-menu-item' href='?nav=test_au'>Test AU</a>"
        "<a class='vxp-menu-item' href='?nav=settings'>Settings</a>"
        "<a class='vxp-menu-item' href='?nav=help'>Help</a>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Cuerpo: iconbar izquierda + "desktop" (MDI)
    st.markdown("<div class='vxp-main-body'>", unsafe_allow_html=True)

    st.markdown("<div class='vxp-leftdock'>", unsafe_allow_html=True)
    render_toolbar(interactive=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='vxp-desktop'>", unsafe_allow_html=True)
    route()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end main-body

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
