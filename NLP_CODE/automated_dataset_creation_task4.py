#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:25:56 2020

@author: venkatkrishnasai
"""

# -- coding: utf-8 --

import psycopg2


# Donot change this function
def getOpenConnection(user='postgres', password='12345678', dbname='NLPDatasetDB'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


con = getOpenConnection()
cursor = con.cursor()

#	"DRUG_NAME_POE", "ENDDATE", "GSN", "PROD_STRENGTH", "STARTDATE", "DIAGNOSIS")
    
#finding boundaries to find the interval for range partition
 
    
cursor.execute('select * from "MIMICTable"')
 
rows = cursor.fetchall()

con.commit()

output_data = []

# Relations between Drug and Diagnosis Disease
for r in rows :
    output_data.append(r[0]+" Cures "+r[5])
    
import csv           

with open('automated_dataset3.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    tsv_output.writerow(output_data)