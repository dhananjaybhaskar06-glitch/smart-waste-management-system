import streamlit as st

def load_theme():

    st.markdown("""
    <style>

    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .stApp{
        background: linear-gradient(
            135deg,
            #0B1120,
            #111827,
            #1E293B
        );
    }

    .main-title{
        text-align:center;
        font-size:3rem;
        font-weight:800;
        color:white;
        margin-bottom:5px;
    }

    .subtitle{
        text-align:center;
        color:#94A3B8;
        font-size:1.1rem;
        margin-bottom:20px;
    }

    .metric-card{
        background:#1E293B;
        padding:20px;
        border-radius:18px;
        border:1px solid #334155;
        box-shadow:0 8px 20px rgba(0,0,0,.35);
        text-align:center;
        color:white;
    }

    .metric-card h1{
        margin:0;
        font-size:2rem;
    }

    .metric-card h3{
        margin-bottom:10px;
        color:#CBD5E1;
    }

    </style>
    """, unsafe_allow_html=True)