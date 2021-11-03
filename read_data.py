# -*- coding:utf-8 -*-
#@Time : 2021/10/29 0029 9:26
#@Author: Joword
#@File : read_data.py

import pandas as pd

PATH = './data/'
pmid_path = './data/pmid/'

pmids = PATH + "user_pmids.txt"
information = PATH + "informations.txt"
evidences = ['user_pm3bp2','user_pp1bs4','user_pp4bp5','user_ps3bs3','user_ps4','user_ps2pm6']

variants = pd.read_excel(PATH+"孕前耳聋变异-20211027.xlsx",sheet_name="SNV (2)")[['变异ID','#Chr','Start','Stop','Ref','Call','Gene Symbol','Transcript','cHGVS','pHGVS']]
clinvar = pd.read_table(PATH+"clinvar.txt",sep='\t')
