XP_CSS = r"""
<style>
/* Hide Streamlit chrome */
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu { display:none !important; }
footer { visibility:hidden; }

/* App background */
html, body, [data-testid="stAppViewContainer"]{
  background:#bfbfbf;
  font-family: Tahoma, "MS Sans Serif", Verdana, Arial, sans-serif;
  font-size:14px;
  font-weight:700;
}

/* Remove Streamlit padding so we can draw a fixed 1024x768 workspace */
.block-container{
  padding:0 !important;
  max-width:none !important;
}

/* ---------- MAIN VXP SHELL (1024x768) ---------- */
.vxp-mainframe{
  width:1024px;
  height:768px;
  margin:0 auto;
  background:#c0c0c0;
  border:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
  position:relative;
  overflow:hidden;
}

.vxp-main-titlebar{
  height:26px;
  background: linear-gradient(90deg, #0a246a 0%, #3a6ea5 100%);
  color:#ffffff;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 8px;
  font-weight:900;
  letter-spacing:0.2px;
  box-sizing:border-box;
}

.vxp-winbtns{ display:flex; gap:4px; }
.vxp-winbtn{
  width:18px; height:16px;
  background:#d4d0c8;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#000;
  font-weight:900;
  font-size:12px;
  line-height:12px;
}
.vxp-winbtn:active{
  border-top:2px solid #404040;
  border-left:2px solid #404040;
  border-right:2px solid #ffffff;
  border-bottom:2px solid #ffffff;
}

.vxp-main-menubar{
  height:22px;
  background:#d4d0c8;
  border-top:1px solid #ffffff;
  border-bottom:1px solid #808080;
  display:flex;
  align-items:center;
  gap:18px;
  padding:0 8px;
  box-sizing:border-box;
  font-weight:700;
  font-size:13px;
}

.vxp-main-menubar span{
  color:#000;
  padding:2px 6px;
}

.vxp-main-menubar a{
  color:#000;
  text-decoration:none;
  padding:2px 6px;
}
.vxp-main-menubar a:hover{
  background:#0a246a;
  color:#fff;
}

.vxp-main-body{
  position:absolute;
  left:0; right:0;
  top:48px;   /* 26 + 22 */
  bottom:22px;/* status bar */
  display:flex;
  overflow:hidden;
}

.vxp-leftdock{
  width:90px;
  background:#d4d0c8;
  border-right:2px solid #808080;
  box-shadow: inset 1px 1px 0px #ffffff;
  padding:6px 4px;
  box-sizing:border-box;
}

.vxp-desktop{
  position:relative;
  flex:1;
  background:#c0c0c0;
  overflow:hidden;
  padding:8px;
  box-sizing:border-box;
}

.vxp-statusbar{
  position:absolute;
  left:0; right:0; bottom:0;
  height:22px;
  background:#d4d0c8;
  border-top:2px solid #808080;
  box-shadow: inset 1px 1px 0px #ffffff;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 8px;
  box-sizing:border-box;
  font-size:12px;
  font-weight:700;
}

/* ---------- CHILD WINDOWS ---------- */
.vxp-win{
  position:absolute;
  background:#c0c0c0;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
  box-sizing:border-box;
}

.vxp-win-caption{
  height:22px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 6px;
  box-sizing:border-box;
  font-weight:900;
  font-size:13px;
}
.vxp-win-caption.active{
  background: linear-gradient(90deg, #0a246a 0%, #3a6ea5 100%);
  color:#fff;
}
.vxp-win-caption.inactive{
  background:#7f7f7f;
  color:#fff;
}

.vxp-win-content{
  padding:10px 10px 8px 10px;
  box-sizing:border-box;
}

/* little close box (visual only) */
.vxp-closebox{
  width:18px;
  height:16px;
  background:#d4d0c8;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#000;
  font-weight:900;
  font-size:12px;
  line-height:12px;
}

/* Modal overlay */
.vxp-dim{
  position:absolute;
  left:0; top:0; right:0; bottom:0;
  background: rgba(0,0,0,0.10);
  z-index:40;
}
.vxp-modal{ z-index:50; }

/* ---------- STREAMLIT WIDGET SKIN (classic 3D) ---------- */
.stButton > button{
  background:#c0c0c0 !important;
  color:#000 !important;
  border-top:2px solid #ffffff !important;
  border-left:2px solid #ffffff !important;
  border-right:2px solid #404040 !important;
  border-bottom:2px solid #404040 !important;
  border-radius:0px !important;
  font-weight:900 !important;
  font-size:18px !important;
  padding:12px 14px !important;
  letter-spacing:0.2px;
}
.stButton > button:active{
  border-top:2px solid #404040 !important;
  border-left:2px solid #404040 !important;
  border-right:2px solid #ffffff !important;
  border-bottom:2px solid #ffffff !important;
}

.vxp-smallbtn .stButton > button{
  font-size:16px !important;
  padding:8px 14px !important;
  width:120px !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[role="combobox"]{
  border-radius:0px !important;
  border-top:2px solid #ffffff !important;
  border-left:2px solid #ffffff !important;
  border-right:2px solid #404040 !important;
  border-bottom:2px solid #404040 !important;
  background:#ffffff !important;
  font-weight:700 !important;
}

/* Monospace panel */
.vxp-mono{
  font-family:"Courier New", Courier, monospace;
  font-size:13px;
  white-space:pre;
  background:#efefef;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  padding:10px;
  box-sizing:border-box;
}

/* Toolbar (pixel icons) */
.vxp-toolbar-img{ width:81px; padding:0; margin:0; }
.vxp-imgbtn{ display:block; margin:6px 0; text-decoration:none; }
.vxp-imgbtn img{
  width:81px;
  height:auto;
  image-rendering: pixelated;
}
.vxp-imgbtn.disabled{ opacity:0.75; pointer-events:none; }

/* Checkmarks */
.vxp-check{
  font-size:22px;
  font-weight:900;
  color:#008000;
  padding-top:10px;
}
</style>
"""
