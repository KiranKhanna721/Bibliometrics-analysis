import pandas as pd
import csv
from graphviz import Digraph
import igraph as ig
import itertools as itr
import streamlit as st
from PIL import Image


def visualisation(G_coauthor,val,box):
    weigh=val.degree()
    visual_style = {}
    visual_style["bbox"] = (box,box)
    visual_style["vertex_size"] = weigh
    visual_style["vertex_label_size"] = 8
    visual_style["edge_width"]=0.5
    i = val.community_infomap()
    pal = ig.drawing.colors.ClusterColoringPalette(len(i))
    val.vs['color'] = pal.get_many(i.membership)
    edgelist = val.get_edgelist()
    source_nodes = [edge[0] for edge in edgelist]
    colors = ["black" if source_nodes[i] == 0 else val.vs['color'][source_nodes[i]] for i in range(val.ecount())]
# Set the color attribute for each edge
    val.es["color1"] = colors
    return val , visual_style


def app():
    st.header("Coupling_Centrality Measures")
    publications_df=pd.read_excel('Data.xlsx')
    publications_df = publications_df.rename(columns={'Author(s) ID':'AuthID','Cited by':'Cited_by', 'Document Type':'DocType','Open Access':'Access', 'Publication Stage':'Stage','Source title':'SourceTitle','Language of Original Document':'Language','Abbreviated Source Title':'AbbreviatedST','PubMed ID':'PubMedID',
                                                  'References':'Ref'})
    publications_df = publications_df.sort_values('Cited_by',ascending=False)
    st.write(publications_df[0:10][['SourceTitle','Ref','Cited_by']])
    new = publications_df.loc[pd.notnull(publications_df['Ref']), ['SourceTitle', 'Ref']][0:100]
    new['Ref'] = new['Ref'].str.split(';')
    journal_cits_df = new[['SourceTitle', 'Ref']].explode('Ref')
    bibcoupling_per_cr = journal_cits_df.groupby('Ref').apply(lambda x: list(itr.combinations(x['SourceTitle'], 2)))
    grouped_by_journal = publications_df.groupby('Ref')
    grouped_by_journal.size().sort_values(ascending=False)
    bibcouplings = bibcoupling_per_cr.explode().dropna() #Explode all combinations of two sources citing the same reference.
    G_Couple_cited = ig.Graph.TupleList(
      edges=bibcouplings,
      vertex_name_attr='SourceTitle',
      directed=False
      )
    weigh=G_Couple_cited.degree()
    box=2000
    G_Couple_cited,visual_style=visualisation(G_Couple_cited,G_Couple_cited,box)
    p3 = ig.plot(G_Couple_cited,vertex_label=G_Couple_cited.vs['SourceTitle'],vertex_frame_width=1,vertex_frame_color='grey', vertex_color = G_Couple_cited.vs['color'],edge_color = G_Couple_cited.es["color1"] , **visual_style)
    p3.save("temp2.png")
    image2 = Image.open("temp2.png")
    st.image(image2, width=1000)
    st.write("the Coupling network using the top 100 cited journal details, from which we get the Coupling network graph shown above. The graph we generated contains 37 vertices and 609 edges where each node is a Source Title and the links depend on the multiple reference links. The size of each node depends on the degree centrality of each journal's source title, which is the number of neighbouring nodes each node contains which determines which  journal has more coupling strength throughout the chosen dataset.")
    G_Couple_cited.vs['degree'] = G_Couple_cited.degree()
    highest_degree_50 = sorted(G_Couple_cited.vs, key=lambda v: v['degree'], reverse=True)
    new = publications_df.loc[pd.notnull(publications_df['Ref']), ['SourceTitle', 'Ref']]
    new['Ref'] = new['Ref'].str.split(';')
    journal_cits_df = new[['SourceTitle', 'Ref']].explode('Ref')
    bibcoupling_per_cr = journal_cits_df.groupby('Ref').apply(lambda x: list(itr.combinations(x['SourceTitle'], 2)))
    grouped_by_journal = publications_df.groupby('Ref')
    grouped_by_journal.size().sort_values(ascending=False)
    bibcouplings = bibcoupling_per_cr.explode().dropna() #Explode all combinations of two sources citing the same reference.
    G_Couple = ig.Graph.TupleList(
      edges=bibcouplings,
      vertex_name_attr='SourceTitle',
      directed=False
      )
    G_Couple.vs['degree'] = G_Couple.degree()
    highest_degree = sorted(G_Couple.vs, key=lambda v: v['degree'], reverse=True)
    G_Couple.vs['betweenness'] = G_Couple.betweenness()
    highest_betweenness_node=sorted(G_Couple.vs, key=lambda v: v['betweenness'], reverse=True)[:5]
    G_Couple.vs['pagerank'] = G_Couple.pagerank()
    sorted(G_Couple.vs, key=lambda v: v['pagerank'], reverse=True)[:5]
    G_Couple.vs['evcent'] = G_Couple.evcent()
    evcent=sorted(G_Couple.vs, key=lambda v: v['evcent'], reverse=True)[:5]
    G_Couple.vs['close'] = G_Couple.closeness()
    close=sorted(G_Couple.vs, key=lambda v: v['close'], reverse=True)[:5]
    G_Couple.vs['Degree'] = G_Couple.degree()
    degree=sorted(G_Couple.vs, key=lambda v: v['Degree'], reverse=True)[:10]
    A,B,C,D,E,F=[],[],[],[],[],[]
    for n in range(0,10):
        a = degree[n]['SourceTitle']
        b = degree[n]['degree']
        c = degree[n]['betweenness']
        d = degree[n]['pagerank']
        e = degree[n]['evcent']
        f = degree[n]['close']
        A.append(a)
        B.append(b)
        C.append(c)
        D.append(d)
        E.append(e)
        F.append(f)

    data={'SourceTitle':A,'Degree_Centrality':B,'Betweeness_Centrality':C,'Pagerank':D,'Eigen Vector Centrality':E,'Closeness Centrality':F}
    df = pd.DataFrame(data)
    st.write(df)

    