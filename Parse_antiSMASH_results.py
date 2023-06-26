import json
import os
from os import listdir
import csv

#Get functions of mibig compounds

mibig_filepath = "D:/Projects/SAF microbiome/Analyses/Antifungal compunds/mibig_json_2.0/"
mibig_files = [mibig_filepath + f for f in listdir(mibig_filepath)]

mibig_functions = {}

for f in mibig_files:
    file_object = open(f)
    data = json.load(file_object)
    
    mibig_id = data['cluster']['mibig_accession']
    
    clusters = data['cluster']['compounds']
    
    for compound in clusters:
        compound_name = compound['compound']
        if 'chem_acts' in compound.keys():
            mibig_functions[compound_name]  = compound['chem_acts']
            
#Analyse antismash results

results_directory = "D:/Projects/SAF microbiome/Analyses/Antifungal compunds/Pratyay - antismash runs/4.4.22/Bacteria_json/SAF_18_json/SAF_18_B_json/"

csv_file_rows = []
files_list = [os.path.join(results_directory,x) for x in os.listdir(results_directory) if x.endswith('json')]

for folder in files_list:
    f = open(folder)
    data = json.load(f)
    
    #organism_name = (data['input_file'][:-8]).replace('_', ' ')  
    organism_name = data['input_file']
    
    bgc_clusters = []
    for x in data['records']:
        if len(x['areas'])!=0:
            bgc_clusters.append(x)
    
       
    for cluster in bgc_clusters:
        
        subclusters = [x for x in cluster['areas']]
        
        for n in range(len(subclusters)):
            cluster_length = subclusters[n]['end'] - subclusters[n]['start']
            cluster_types = ', '.join(subclusters[n]['products'])
            known_cluster = ''
            blast_score = ''
            known_cluster_functions = ''
            
            mibig_results = cluster['modules']['antismash.modules.clusterblast']['knowncluster']['results'][n]['ranking']
            if len(mibig_results)>0:
                known_cluster = mibig_results[0][0]['description']
                blast_score = mibig_results[0][1]['blast_score']
                
            if known_cluster in mibig_functions.keys():
                known_cluster_functions = mibig_functions[known_cluster]
                
                    
            cluster_row = [organism_name, bgc_clusters.index(cluster), cluster_types, known_cluster, known_cluster_functions]
            csv_file_rows.append(cluster_row)
            
    f.close()
            

with open("D:/Projects/SAF microbiome/Analyses/Antifungal compunds/Pratyay - antismash runs/4.4.22/Bacteria_json/SAF_18_json/SAF_18_B_json/results.csv", 'w+', encoding='utf-16') as csvfile: 
    csv_headers = ['Organism name','Cluster index', 'Cluster type', 'Known cluster', 'Known cluster functions']
    writer = csv.writer(csvfile)
    writer.writerow(csv_headers)
    writer.writerows(csv_file_rows)
    
csvfile.close()


        
        
    
    

    
    

    
    
    
    