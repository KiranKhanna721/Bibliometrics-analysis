import numpy as np
import streamlit as st
import pandas as pd
import app1
import app2
import about




def main():
    st.title("Bibliometric Analysis of Simulations in Medical Field")
    PAGES = {
        "About":about,
        "Coauthor_Centrality Measures":app1,
        "Coupling_Centrality Measures.":app2,
    }
    st.sidebar.title('Bibliometric Analysis of Simulations in Medical Field')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()
    


if __name__ == '__main__':
    main()   
