# Bibliometric Analysis of Simulations in the Medical Field

A Streamlit app that runs a bibliometric network analysis on a Scopus-style export of publications about simulation in medicine (`Data.xlsx`).

## Pages

- **About:** an introduction to bibliometric analysis and collaboration networks in health innovation
- **Coauthor Centrality Measures:** builds a co-authorship network, ranks papers by citations, computes centrality measures and draws the network with Infomap community colouring
- **Coupling Centrality Measures:** builds a bibliographic-coupling network between source titles from their shared references and visualises it the same way

## Tech stack

Python, Streamlit, pandas, python-igraph, cairocffi, matplotlib

## Getting started

```bash
pip install -r requirements.txt
streamlit run app.py
```
