import numpy as np
import pandas as pd
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community.quality import modularity
from collections import defaultdict
from collections import Counter
from analysis_scripts import compute_analytics, graph_loader, projected_graph, rings, metrics
import sys
import argparse
import os.path as op


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

p = argparse.ArgumentParser()
p.add_argument("--data_path", type=str, required=True, help="Path to xyz file to analyze.")
p.add_argument("--output", type=str, required=True, help="Path + file name for output df (end in csv).")
p.add_argument("--min_dir", type=str, required=False, help="Path to xyz files of lowest energy structures.")
p.add_argument("--single", type=str2bool, required=False, nargs="?", const=True, default=False, 
                help="A switch for extracting descriptors for a single structure")
p.add_argument("--reference_path", type=str, required=False, help="Path to xyz file considered a reference.")
p.add_argument("--verbose", type=str2bool, required=False, help="Debug output")
args = p.parse_args()

if args.verbose:
    print("data path: ", args.data_path)
    print("reference path: ", args.reference_path)
    print("min_dir path: ", args.min_dir)
cluster_list, energy, comments = graph_loader.read_lines(args.data_path)

actual_energy = []
predicted_energy = []
for e in energy:
    #print("E: ", e)
    if len(e) == 2:
        actual_energy.append(e[0])
        predicted_energy.append(e[1])
    elif len(e) == 1:
        actual_energy.append(e[0])

if args.verbose:
    print(str(len(cluster_list))+' clusters found')
    print('comments: ', comments)
    print('actual_energy: ', actual_energy)
    print('predicted_energy: ', predicted_energy)

a = [compute_analytics.graph_analytics(x) for x in cluster_list]
a = np.swapaxes(a, 0, 1)
similarity_list, projected_similarity_list=[],[]
trimers,tetramers,pentamers,hexamers=[],[],[],[]
degrees=[]
cluster_idx=[]

if args.verbose:
    for k in a:
        print (k)
        if len(k) != len(cluster_list):
            print("len error for k!")

if args.single:

    for i, cluster in enumerate(cluster_list):
        cluster_size = int(int(len(cluster))/3)
        try:
            graph, node_labels, edges = graph_loader.load_graph(cluster)
            proj = projected_graph.project_oxygen_role_based_graph(graph)
            tri, tet, pent, hexa = rings.enumerate_rings(proj)
            trimers.append(tri)
            tetramers.append(tet)
            pentamers.append(pent)
            hexamers.append(hexa)
            cluster_idx.append(i)
        except:
            print('error')

    #if len(similarity_list) != len(cluster_list):
    #    print("len error for similarity_list!")
    #if len(projected_similarity_list) != len(cluster_list):
    #    print("len error for projected_similarity_list!")
    if len(trimers) != len(cluster_list):
        print("len error for trimers!")
    if len(tetramers) != len(cluster_list):
        print("len error for tetramers!")
    if len(pentamers) != len(cluster_list):
        print("len error for pentamers!")
    if len(hexamers) != len(cluster_list):
        print("len error for hexamers!")
    if len(cluster_idx) != len(cluster_list):
        print("len error for cluster_idx!")
    #if len(degrees) != len(cluster_list):
    #    print("len error for degrees!")


    
    if comments != []:
        if args.verbose:
            print("TESTME: 0", comments, len(comments))
            print("TESTME: 0", a)
        d = {'Id':cluster_idx, 'Nodes': a[0], 'Edges': a[1], 'Diameter': a[2],
             'Dangling Hydrogens': a[3], 'Average Shortest Path Length': a[4],
             'filename': comments,
             'Trimers': trimers, 'Tetramers': tetramers, 'Pentamers': pentamers,
             'Hexamers': hexamers}
    else:
        if args.verbose:
            print("TESTME: 1", a)
        d = {'Id':cluster_idx, 'Nodes': a[0], 'Edges': a[1], 'Diameter': a[2],
             'Dangling Hydrogens': a[3], 'Average Shortest Path Length': a[4],
             #'Actual Energy': actual_energy,
             'Trimers': trimers, 'Tetramers': tetramers, 'Pentamers': pentamers,
             'Hexamers': hexamers}
    
    df = pd.DataFrame(d)
    
    df['Cluster Size'] = df['Nodes']/3
    df['H-bonds'] = df['Edges']-(df['Cluster Size']*2)
    
    df.to_csv(args.output, index=False)

else:


    for i, cluster in enumerate(cluster_list):
        cluster_idx.append(i)
        cluster_size = int(int(len(cluster))/3)
        if args.reference_path:
            xyzfile= args.reference_path
        else:
            xyzfile= op.join(args.min_dir, f'W{cluster_size}_geoms_all_lowestE.xyz')
        base_cluster_list,_ = graph_loader.read_lines_base(xyzfile)
        #load lowest energy structure from the full list
        G_base,_,_ = graph_loader.load_graph(base_cluster_list[0][2:]) 
        proj_G_base = projected_graph.project_oxygen_role_based_graph(G_base)
        try:
           #Similarity of full graph
           G_variable,_,_ = graph_loader.load_graph(cluster)
           similarity_list.append(compute_analytics.calculate_similarity(G_base, G_variable))
           #Similarity of oxygen projected graph
           proj_G_variable = projected_graph.project_oxygen_role_based_graph(G_variable)
           projected_similarity_list.append(compute_analytics.calculate_similarity(proj_G_base, proj_G_variable))
           tri, tet, pent, hexa = rings.enumerate_rings(proj_G_variable)
           trimers.append(tri)
           tetramers.append(tet)
           pentamers.append(pent)
           hexamers.append(hexa)
           degs=[v for k,v in proj_G_variable.degree()]
           degrees.append(np.mean(degs))
        except:
           #disconnected graphs fail test and get s values of -1
           projected_similarity_list.append(-1)
           similarity_list.append(-1)

    if len(similarity_list) != len(cluster_list):
        print("len error for similarity_list!")
    if len(projected_similarity_list) != len(cluster_list):
        print("len error for projected_similarity_list!")
    if len(trimers) != len(cluster_list):
        print("len error for trimers!")
    if len(tetramers) != len(cluster_list):
        print("len error for tetramers!")
    if len(pentamers) != len(cluster_list):
        print("len error for pentamers!")
    if len(hexamers) != len(cluster_list):
        print("len error for hexamers!")
    if len(degrees) != len(cluster_list):
        print("len error for degrees!")

    
    if comments != []:
        d = {'Id':cluster_idx,
             'Nodes': a[0], 'Edges': a[1], 'Diameter': a[2],
             'Dangling Hydrogens': a[3], 'Average Shortest Path Length': a[4],
             'daa': a[5], 'dda': a[6], 'da': a[7], 'aa': a[8], 'dd': a[9], 
             'ddaaa': a[10], 'ddaa': a[11], 'a': a[12], 'd': a[13],
             'Wiener Index': a[14], 'N Communities': a[15], 'Modularity': a[16], 
             'Similarity': similarity_list,'Projected Similarity': projected_similarity_list,
             'Trimers': trimers, 'Tetramers': tetramers, 'Pentamers': pentamers,
             'Hexamers': hexamers, 'Degree': degrees}
        if len(comments) == len(cluster_list):
            d['comments']=comments
    else:
        d = {'Id':cluster_idx,
             'Nodes': a[0], 'Edges': a[1], 'Diameter': a[2],
             'Dangling Hydrogens': a[3], 'Average Shortest Path Length': a[4],
             'daa': a[5], 'dda': a[6], 'da': a[7], 'aa': a[8], 'dd': a[9], 
             'ddaaa': a[10], 'ddaa': a[11], 'a': a[12], 'd': a[13],
             'Wiener Index': a[14], 'N Communities': a[15], 'Modularity': a[16], 
             'Similarity': similarity_list,'Projected Similarity': projected_similarity_list,
             'Trimers': trimers, 'Tetramers': tetramers, 'Pentamers': pentamers,
             'Hexamers': hexamers, 'Degree': degrees}
    if len(actual_energy) == len(cluster_list):
        d['Actual Energy']=actual_energy
    if len(predicted_energy) == len(cluster_list):
        d['Predicted Energy']=predicted_energy
    
    df = pd.DataFrame(d)
    
    df['Cluster Size'] = df['Nodes']/3
    df['H-bonds'] = df['Edges']-(df['Cluster Size']*2)
    df['H-bond Percent'] = df['H-bonds']/df['Edges']
    df['Unsaturation'] = df['H-bonds']/df['Dangling Hydrogens']
    df['daa Percent'] = df['daa']/df['Nodes']
    df['dda Percent'] = df['dda']/df['Nodes']
    if len(actual_energy) == len(cluster_list) and len(predicted_energy) == len(cluster_list):
        df['Absolute Error per Water'] = ((df['Actual Energy']-df['Predicted Energy'])/df['Cluster Size']).apply(lambda x: np.abs(x))
        df['Percent Error']=((df['Actual Energy']-df['Predicted Energy'])/df['Actual Energy']).apply(lambda x: 100*np.abs(x))
    df['H-bond Saturation']=(df['H-bonds']/df['Cluster Size'].apply(lambda x: x*4)).apply(lambda x: x*2)
    
    #print(df["Similarity"])
    df.to_csv(args.output, index=False)
    #df2=df[["Similarity","Projected Similarity"]]
    #df2.to_csv(args.output, index=False)
