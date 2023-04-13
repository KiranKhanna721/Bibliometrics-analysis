import streamlit as st
import pandas as pd
import csv
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import itertools as itr
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
    st.header("Coauthor_Centrality Measures")
    publications_df=pd.read_excel('Data.xlsx')
    publications_df = publications_df.rename(columns={'Author(s) ID':'AuthID','Cited by':'Cited_by', 'Document Type':'DocType','Open Access':'Access', 'Publication Stage':'Stage','Source title':'SourceTitle','Language of Original Document':'Language','Abbreviated Source Title':'AbbreviatedST','PubMed ID':'PubMedID',
                                                  'References':'Ref'})
    st.subheader("Dataset Top 5 rows")
    st.write(publications_df.head())
    publications_df_cited= publications_df.sort_values('Cited_by',ascending=False)
    st.subheader("Sorted graph based on cittion counts")
    st.write(publications_df_cited[0:5][['SourceTitle','Ref','Cited_by']])
    publications_df_cited['AU_split'] = publications_df_cited['Authors'].fillna("").str.split(', ')
    coauth = publications_df_cited['AU_split'][1:50].apply(lambda authors: list(itr.combinations(authors, 2))) #first hundred journals
    coauthors1 = coauth.explode().dropna()
    G_coauthor_cited = ig.Graph.TupleList(
      edges=coauthors1.to_list(),
      vertex_name_attr='author',
      directed=False
      )
    box=1000
    G_coauthor_cited,visual_style=visualisation(G_coauthor_cited,G_coauthor_cited,box)
    p = ig.plot(G_coauthor_cited,vertex_label=G_coauthor_cited.vs['author'],vertex_frame_width=1,vertex_frame_color='grey', vertex_color = G_coauthor_cited.vs['color'],edge_color = G_coauthor_cited.es["color1"] , **visual_style)
    p.save("temp.png")
    image = Image.open("temp.png")
    st.image(image, width=700)
    st.write("The above graph describes the properties of a graph generated through social network analysis of authors and their co-authorship connections in a chosen dataset. The graph has 334 nodes (authors) and 1201 edges (co-authorship connections), and the size and color of each node correspond to the degree centrality and cluster membership of the author, respectively. The graph reveals that most authors work with only a few journals and that very few authors are connected to top-cited journals outside of their main working journals.")
    publications_df['AU_split'] = publications_df['Authors'].fillna("").str.split(', ')
    coauth = publications_df['AU_split'].apply(lambda authors: list(itr.combinations(authors, 2)))
    coauthors1 = coauth.explode().dropna()
    G_coauthor = ig.Graph.TupleList(
      edges=coauthors1.to_list(),
      vertex_name_attr='author',
      directed=False
      )
    G_coauthor.degree()
    G_coauthor.vs['degree'] = G_coauthor.degree()
    yaxis=list(range(0,len(G_coauthor.vs['degree'])))
    fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
    ax.set_xticks(np.arange(0, max(yaxis), 50))
    ax.set_yticks(np.arange(0, max(yaxis), 5000))
    ax.scatter(G_coauthor.vs['degree'], yaxis, s=6)
    st.subheader("Degree centrality")
    st.pyplot(fig)
    st.write(" This is the Scatter plot of degree centrality for co-authorship networks. We have plotted the graph with X-axis as the degree value and Y-axis as the node numbers. As we can see, the majority of authors work with a small number of people, whereas it is rare that authors work with more people. The highest degree in the above graph is 455 for the author Konge L.")
    highest_degree = sorted(G_coauthor.vs, key=lambda v: v['degree'], reverse=True)
    highest_degree_node = G_coauthor.vs[G_coauthor.degree().index(max(G_coauthor.degree()))]
    neighbors = highest_degree_node.neighbors()
    neighbors_including_highest_degree_node = neighbors + [highest_degree_node]
    highest_degree_subgraph = G_coauthor.subgraph(neighbors_including_highest_degree_node)
    box=2000
    highest_degree_subgraph,visual_style=visualisation(G_coauthor,highest_degree_subgraph,box)
    p1 = ig.plot(highest_degree_subgraph,vertex_label=highest_degree_subgraph.vs['author'],vertex_frame_width=1,vertex_frame_color='grey', vertex_color = highest_degree_subgraph.vs['color'],edge_color =highest_degree_subgraph.es["color1"] , **visual_style)
    p1.save("temp1.png")
    image1 = Image.open("temp1.png")
    st.subheader("Highest degree node and its neighbours (Connected nodes)")
    st.image(image1, width=700)
    st.write("To get a closer insight we chose the most important author with the highest degree centrality and plotted a co-authorship network where all the authors he is connected with are only shown. The network gives insight into who the most important author is from the whole data and who all are connected to the person via co-authorship as shown in above graph.")
    st.write("Number of vertices in largest connected component:", highest_degree_subgraph.vcount())
    st.write("Number of edges in largest connected component:", highest_degree_subgraph.ecount())
    st.write("Degree of the largest connected component:", highest_degree_node.degree())
    st.write("Name of the largest degree author :", highest_degree_node["author"])
    G_coauthor.vs['betweenness'] = G_coauthor.betweenness()
    highest_betweenness_node=sorted(G_coauthor.vs, key=lambda v: v['betweenness'], reverse=True)[:5]
    highest_betweenness_node = G_coauthor.vs[G_coauthor.betweenness().index(max(G_coauthor.betweenness()))]
    highest_betweenness_subgraph = G_coauthor.subgraph(highest_betweenness_node.neighbors())
    st.subheader("Betweeness Centrality")
    st.write("Betweenness centrality defines the importance of any node based on the number of times it occurs in the shortest paths between other nodes.")
    st.write("Number of vertices in largest betweenness connected component:", highest_betweenness_subgraph.vcount())
    st.write("Number of edges in largest betweenness  connected component:", highest_betweenness_subgraph.ecount())
    st.write("Degree of the largest betweenness connected component:", highest_betweenness_node.degree())
    st.write("Name of the largest betweenness author :", highest_betweenness_node["author"])
    G_coauthor.vs['pagerank'] = G_coauthor.pagerank()
    sorted(G_coauthor.vs, key=lambda v: v['pagerank'], reverse=True)[:5]
    G_coauthor.vs['evcent'] = G_coauthor.evcent()
    evcent=sorted(G_coauthor.vs, key=lambda v: v['evcent'], reverse=True)[:5]
    G_coauthor.vs['close'] = G_coauthor.closeness()
    close=sorted(G_coauthor.vs, key=lambda v: v['close'], reverse=True)[:5]
    G_coauthor.vs['Degree'] = G_coauthor.degree()
    degree=sorted(G_coauthor.vs, key=lambda v: v['Degree'], reverse=True)[:10]
    A,B,C,D,E,F=[],[],[],[],[],[]
    for n in range(0,10):
        a = degree[n]['author']
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
    data={'Author':A,'Degree_Centrality':B,'Betweeness_Centrality':C,'Pagerank':D,'Eigen Vector Centrality':E,'Closeness Centrality':F}
    df = pd.DataFrame(data)
    st.write(df)


    
