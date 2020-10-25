# -*- coding: utf-8 -*-

import pandas as pd

df_entities = pd.read_csv(r"chemprot_training_entities.tsv",sep='\t',names=["DOC ID","Term Number", "Attribute Type","Start Position", "End Position", "Name"])

df_relations = pd.read_csv(r"chemprot_training_relations.tsv",sep='\t',names=["DOC ID","Relation ID", "Relation Type","Relation Name", "Term 1", "Term 2"])

df_gold_relations = pd.read_csv(r"chemprot_relations.csv",names=["Group","Eval","CHEMPROT Relations"])
#for index, row in df_relations.iterrows():
docid_relation = 10047461
terms = []
term_types = []
start = []
end = []
name = []

for index,row in df_entities.iterrows():
    if(docid_relation == int(row['DOC ID'])):
        terms.append(row['Term Number'])
        term_types.append(row['Attribute Type'])
        start.append(row['Start Position'])
        end.append(row['End Position'])
        name.append(row['Name'])
     
df_result = pd.DataFrame(columns=['DOC ID','Relation ID', 'Relation Type',"Relation Name", "Term 1", "Term 2"])
g=0
for index,row in df_relations.iterrows():
    relation_attrs = ""
    if(int(row['DOC ID']) == 10047461):
        df_result.loc[g]= row
        for index1,row1 in df_gold_relations.iterrows():
            if(row['Relation ID'] == row1['Group']):
                relation_attrs += row1['CHEMPROT Relations'].strip()
        relations = relation_attrs.split('|')
        relations.remove(row['Relation Name'])
        for row2 in relations:
            g += 1
            df_result.loc[g] = {'DOC ID':row['DOC ID'],'Relation ID':row['Relation ID'],'Relation Type':row['Relation Type'],"Relation Name":row2, "Term 1":row['Term 1'], "Term 2":row['Term 2']}
        g+=1
        
        
###############################################################

#df_relations['Term 1']




import pandas as pd
df_entities = pd.read_csv(r"chemprot_training_entities.tsv",sep='\t',names=["DOC ID","Term Number", "Attribute Type","Start Position", "End Position", "Name"])

df_relations = pd.read_csv(r"chemprot_training_relations.tsv",sep='\t',names=["DOC ID","Relation ID", "Relation Type","Relation Name", "Term 1", "Term 2"])

df_gold_relations = pd.read_csv(r"chemprot_relations.csv",names=["Group","Eval","CHEMPROT Relations"])

df_automated_data= pd.read_csv(r"automated_dataset1.csv")




#dfpart1 = df_relations.iloc[1205:2000,:]
dfpart1 = df_automated_data.iloc[100:2000,:]

DATASET_final=dfpart1.copy(deep='True')

DATASET_final['abstract']=['']*len(DATASET_final)


#DATASET=pd.DataFrame()
#DATASET_final=pd.DataFrame()

X1=[]
Y1=[]
REL=[]
DATA=[]
def checkEnt(ID,T1,T2,rel) :
    x=""
    y=""
    print(t1,t2)
    row=[]
    k=1
    for index, row in df_entities.iterrows():
        if row['DOC ID']==ID and row['Term Number']==T1 :
            x=row['Name']
            break
        
    for index, row in df_entities.iterrows():
        if row['DOC ID']==ID and row['Term Number']==T2  :
            y=row['Name']
            break
#            print(x)        
#    X1.append(x)
#    Y1.append(y)
#    REL.append(rel)

#    print("x=",X1)
#    print("y=",Y1)
    
    return x +" is " + rel + " of " +y
i=0
for index, row in dfpart1.iterrows():
    print("index",index)
#    print(row['DOC ID'],row['Term 1'],row['Term 2'])
    id=row['DOC ID']
    rel=row['Relation Name']
    t1 = row['Term 1'].split(":")[1]
    t2 = row['Term 2'].split(":")[1]
    
    
#    print(t1,t2,rel)
    print(checkEnt(id,t1,t2,rel))
    DATASET_final.abstract.iloc[i]=checkEnt(id,t1,t2,rel)
    i=i+1
    
    
    
DATASET_final.to_csv('dataset_table_mixedraj.csv',index=False)
    
    

#DATASET["Entity_1"] =X1
#DATASET["Entity_2"] =Y1
#DATASET["REL"] =REL
#
#DATASET.to_csv('dataset_table2.csv',index=False)
#
#
#
#entity1=""
#entity2=""
#relation=""
#template1 = entity1 +"is"+ relation + "of" + entity2
#


    

    
   










        