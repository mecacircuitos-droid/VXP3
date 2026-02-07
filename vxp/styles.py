XP_CSS = r"""
<style>
/* ---- Hide Streamlit chrome ---- */
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu { display:none !important; }
footer { visibility:hidden; }

/* ---- Global look (Windows XP classic-ish) ---- */
html, body, [data-testid="stAppViewContainer"]{
  background:#bfbfbf;
  font-family: "Trebuchet MS", Tahoma, "MS Sans Serif", Verdana, Arial, sans-serif;
  font-size:14px;
  font-weight:700;
}

/* Force 4:3 frame (1024×768) */
.block-container{
  padding:0 !important;
  max-width:1024px !important;
  margin:0 auto !important;
  min-height:768px !important;
}

/* Main content area gets a border like the VXP window */
[data-testid="stAppViewContainer"] .block-container{
  background:#c0c0c0;
  border:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
}

/* ---- Shell (title/menu/status) ---- */
.vxp-shell-titlebar{
  height:26px;
  background: linear-gradient(90deg, #0a246a 0%, #3a6ea5 100%);
  color:#ffffff;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 8px;
  box-sizing:border-box;
  font-weight:900;
  letter-spacing:0.2px;
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

.vxp-shell-menubar{
  height:22px;
  background:#d4d0c8;
  border-top:1px solid #ffffff;
  border-bottom:1px solid #808080;
  display:flex;
  align-items:center;
  gap:14px;
  padding:0 8px;
  box-sizing:border-box;
  font-weight:700;
  font-size:13px;
  color:#000;
}
.vxp-shell-menubar span{ padding:2px 4px; }

.vxp-shell-statusbar{
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

/* ---- Left smart icon bar ---- */
.vxp-toolbar-img{ width:81px; padding:0; margin:0; }
.vxp-imgbtn{ display:block; margin:6px 0; text-decoration:none; }
.vxp-imgbtn img{ width:81px; height:auto; image-rendering: pixelated; }
.vxp-imgbtn.disabled{ opacity:0.75; pointer-events:none; }

/* ---- Desktop host (MDI area) ---- */
/* We create a marker (.vxp-desktop-host) inside a VerticalBlock; style that block as the desktop. */
div[data-testid="stVerticalBlock"]:has(.vxp-desktop-host){
  position:relative;
  height:680px;
  background:#c0c0c0;
  overflow:hidden;
}

/* Common window skin applied to positioned element-containers */
.vxp-win-caption{
  height:22px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 6px;
  box-sizing:border-box;
  font-weight:900;
  font-size:13px;
  color:#fff;
}
.vxp-win-caption.active{ background: linear-gradient(90deg, #0a246a 0%, #3a6ea5 100%); }
.vxp-win-caption.inactive{ background:#7f7f7f; }

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

.vxp-win-pad{ padding:10px 10px 8px 10px; box-sizing:border-box; }

/* ---- Position windows using marker + adjacent sibling (requires :has support) ---- */
/* Select Procedure window */
div[data-testid="stVerticalBlock"]:has(.vxp-desktop-host)
  > div.element-container:has(.vxp-win-marker[data-win="selectproc"]) + div.element-container{
  position:absolute;
  left:0px;
  top:0px;
  width:760px;
  height:610px;
  z-index:10;
  background:#c0c0c0;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
  padding:0;
}

/* Active window (procedure screens) */
div[data-testid="stVerticalBlock"]:has(.vxp-desktop-host)
  > div.element-container:has(.vxp-win-marker[data-win="active"]) + div.element-container{
  position:absolute;
  left:220px;
  top:95px;
  width:680px;
  height:520px;
  z-index:20;
  background:#c0c0c0;
  border-top:2px solid #ffffff;
  border-left:2px solid #ffffff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
  padding:0;
}

/* Make inner VerticalBlocks flush inside the window boxes */
div[data-testid="stVerticalBlock"]:has(.vxp-desktop-host)
  > div.element-container:has(.vxp-win-marker) + div.element-container
  > div[data-testid="stVerticalBlock"]{
  gap:0rem;
}

/* ---- Widgets (classic 3D) ---- */
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

/* Inputs */
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

/* Monospace panels */
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

.vxp-label{ font-weight:900; font-size:15px; }

</style>
"""
