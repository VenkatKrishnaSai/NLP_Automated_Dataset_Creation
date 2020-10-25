#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 00:16:37 2020

@author: venkatkrishnasai
"""

import pandas as pd

# Copy tsv files to dataframes
df_entities = pd.read_csv("chemprot_training_entities.tsv",sep='\t',names=["DOC ID","Term Number", "Attribute Type","Start Position", "End Position", "Name"])

df_relations = pd.read_csv("chemprot_training_relations.tsv",sep='\t',names=["DOC ID","Relation ID", "Relation Type","Relation Name", "Term 1", "Term 2"])

df_gold_relations = pd.read_csv("chemprot_relations.csv",names=["Group","Eval","CHEMPROT Relations"])
     
df_result = pd.DataFrame(columns=['DOC ID','Relation ID', 'Relation Type',"Relation Name", "Term 1", "Term 2"])

df_negating_result = pd.DataFrame(columns=['DOC ID','Relation ID', 'Relation Type',"Relation Name", "Term 1", "Term 2"])

#Initializing indices
g=0
h=0

# Iterate over the relations dataframe to generate new relations
for index,row in df_relations.iterrows():
    relation_attrs = ""
    
    #Method 1( Generate new relations by replacing relation name with other relation names in the same group)
    # Generate approximately 17000 additional relations
    df_result.loc[g]= row
    for index1,row1 in df_gold_relations.iterrows():
        if(row['Relation ID'] == row1['Group']):
            relation_attrs += row1['CHEMPROT Relations'].strip()
    relations = relation_attrs.split('|')
    if row['Relation Name'] in relations:
        relations.remove(row['Relation Name'])
    for row2 in relations:
        g += 1
        df_result.loc[g] = {'DOC ID':row['DOC ID'],'Relation ID':row['Relation ID'],'Relation Type':row['Relation Type'],"Relation Name":row2, "Term 1":row['Term 1'], "Term 2":row['Term 2']}
    g+=1
    
    #Method 2(Generate new relations by replacing relation name with negating relation names of other groups)
    # Generate approximately 61000 additional relations
    relation_negating_attrs = []
    df_negating_result.loc[h]= row
    for index1,row1 in df_gold_relations.iterrows():
        if(index1 <= 4):
            if(row['Relation ID'] != row1['Group']):
                relation_negating_attrs.append(row1['CHEMPROT Relations'].strip())
    for i in range(len(relation_negating_attrs)):
        if(i>0):
            relations = relation_negating_attrs[i].split('|')
            not_attrs = ""
            for j in range(len(relations)):
                not_attrs += 'NOT '+ relations[j]
                if(j != (len(relations)-1)):
                    not_attrs += "|"
                    
            k=df_gold_relations[df_gold_relations['CHEMPROT Relations']== not_attrs].index.values
            if(k.size == 0):
                r,c = df_gold_relations.shape
                df_gold_relations.loc[r] = {'Group':df_gold_relations['Group'][r-1].split(':')[0]+":"+str(int(df_gold_relations['Group'][r-1].split(':')[1])+1),'Eval':'Y','CHEMPROT Relations':not_attrs}
            l=df_gold_relations[df_gold_relations['CHEMPROT Relations']== not_attrs].index.values
            for row3 in relations:
                h += 1
                df_negating_result.loc[h] = {'DOC ID':row['DOC ID'],'Relation ID':df_gold_relations['Group'][l.flat[0]],'Relation Type':row['Relation Type'],"Relation Name":'NOT '+row3, "Term 1":row['Term 1'], "Term 2":row['Term 2']}
            h+=1
         
# Export dataframes to a csv
df_result.to_csv('automated_dataset.csv',index=False)

df_negating_result.to_csv('automated_dataset.csv',index=False)
        
            
        