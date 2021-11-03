# -*- coding:utf-8 -*-
#@Time : 2021/10/29 0029 9:29
#@Author: Joword
#@File : utils.py
#@Description: a module of data processing, include merge, clean and so on.

import pandas as pd
from read_data import pmid_path,evidences

def pmid_groupby(arg:str):
	evidences = pd.read_table(arg+".txt",sep='\t',dtype='str',encoding='utf-8')
	df1 = pd.DataFrame(pd.DataFrame(evidences).groupby(['variant_id'],as_index=False)['submitter','publication'].agg(lambda x:x.str.cat(sep='|')),dtype='str')
	return df1

def make_chgvs():
	u'''将del和dup不跟碱基，ins后跟碱基
	:return:
	'''
	with open(path,"r+") as file:
		with open("chgvs_index.txt","w+") as g:
			next(file)
			g.write("variantId\tchr\tstart\tstop\tref\talt\tgene\ttranscript\tchgvs\n")
			lines = [i.strip().split("\t") for i in file.readlines()]
			for line in lines:
				if len(line[8].split("alt: "))>1:
					if len(line[8].split("alt: ")[1].replace(" )","").split("del"))>1:
						g.write("\t".join([line[i] for i in range(0, 8)]+[str(line[7] + ":" + line[8].split("alt: ")[1].replace(" )","").split("del")[0] + "del")])+"\n")
					elif len(line[8].split("alt: ")[1].replace(" )","").split("dup"))>1:
						g.write("\t".join([line[i] for i in range(0, 8)]+[str(line[7] + ":" + line[8].split("alt: ")[1].replace(" )","").split("dup")[0] + "dup")])+"\n")
					else:
						g.write("\t".join([line[i] for i in range(0, 8)] + [str(line[7] + ":" + line[8].split("alt: ")[1].replace(" )",""))]) + "\n")
				elif len(line[8].split("alt: "))==1:
					if len(line[8].split("del")) >1 and len(line[8].split("ins"))==1:
						g.write("\t".join([line[i] for i in range(0, 8)]+[str(line[7]+":"+line[8].split("del")[0]+"del")])+"\n")
					elif len(line[8].split("dup"))>1 and len(line[8].split("ins"))==1:
						g.write("\t".join([line[i] for i in range(0, 8)]+[str(line[7]+":"+line[8].split("dup")[0]+"dup")])+"\n")
					elif len(line[8].split("del")) >1 and len(line[8].split("ins"))>1:
						g.write("\t".join([line[i] for i in range(0, 8)] + [str(line[7] + ":" + line[8].split("del")[0] + "del")+"ins"+line[8].split("ins")[1]]) + "\n")
					else:
						g.write("\t".join([line[i] for i in range(0, 8)] + [str(line[7] + ":" + line[8])]) + "\n")
				else:
					g.write("\t".join([line[i] for i in range(0, 8)]+[str(line[7]+":"+line[8])])+"\n")