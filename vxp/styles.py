XP_CSS = r"""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu { display:none !important; }
footer { visibility:hidden; }

html, body, [data-testid="stAppViewContainer"]{
  background:#bfbfbf;
  font-family: Tahoma, "MS Sans Serif", Verdana, Arial, sans-serif;
  font-size:14px;
  font-weight:700;
}
.block-container{
  padding-top:0.25rem;
  padding-bottom:0.75rem;
  /* XGA 4:3 (1024x768) */
  max-width:1024px;
  margin:0 auto;
}
.vxp-frame{
  background:#c0c0c0;
  border:2px solid #404040;
  box-shadow:2px 2px 0px #808080;
  border-radius:2px;
  max-width:1024px;
  min-height:740px;
  margin:0 auto;
}
.vxp-titlebar{
  background: linear-gradient(90deg, #0a246a 0%, #3a6ea5 100%);
  color:#fff;
  padding:6px 10px;
  height:30px;
  font-weight:900;
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.vxp-menubar{
  background:#d4d0c8;
  border-bottom:1px solid #808080;
  padding:4px 10px;
  font-weight:700;
}
.vxp-content{ padding:10px; background:#c0c0c0; }

.stButton > button{
  background:#d4d0c8 !important;
  color:#000 !important;
  border-top:2px solid #fff !important;
  border-left:2px solid #fff !important;
  border-right:2px solid #404040 !important;
  border-bottom:2px solid #404040 !important;
  border-radius:0px !important;
  font-weight:900 !important;
  font-size:16px !important;
  padding:12px 14px !important;
  letter-spacing:0.2px;
}
.stButton > button:active{
  border-top:2px solid #404040 !important;
  border-left:2px solid #404040 !important;
  border-right:2px solid #fff !important;
  border-bottom:2px solid #fff !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input{
  border-radius:0px !important;
  border:2px solid #404040 !important;
  background:#ffffff !important;
  font-weight:700 !important;
}

.vxp-label{ font-weight:900; font-size:15px; }
.vxp-mono{
  font-family:"Courier New", Courier, monospace;
  font-size:13px;
  white-space:pre;
  background:#efefef;
  border:2px solid #808080;
  padding:10px;
}
.vxp-toolbar{
  background:#d4d0c8;
  border:2px solid #808080;
  box-shadow: inset 1px 1px 0px #ffffff;
  padding:8px;
  border-radius:2px;
}
.vxp-sidebtn{
  display:block;
  background:#d4d0c8;
  border-top:2px solid #fff;
  border-left:2px solid #fff;
  border-right:2px solid #404040;
  border-bottom:2px solid #404040;
  text-decoration:none;
  color:#000;
  font-weight:900;
  font-size:13px;
  padding:12px 10px;
  margin-bottom:10px;
}
.vxp-sidebtn:active{
  border-top:2px solid #404040;
  border-left:2px solid #404040;
  border-right:2px solid #fff;
  border-bottom:2px solid #fff;
}
.vxp-sidebtn img{
  width:18px; height:18px;
  vertical-align:middle;
  margin-right:10px;
}
.vxp-strip{
  display:flex; align-items:center; justify-content:space-between;
  margin:4px 0 10px 0;
  font-weight:900;
}
</style>
"""
XP_CSS += r"""
<style>
.vxp-toolbar-img{
  width:81px;
  padding:0;
  margin:0;
}
.vxp-imgbtn{
  display:block;
  margin:6px 0;
  text-decoration:none;
}
.vxp-imgbtn img{
  width:81px;
  height:auto;
  image-rendering: pixelated;
}
.vxp-imgbtn.disabled{
  opacity:0.6;
  pointer-events:none;
}
</style>
"""
