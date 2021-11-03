# -*- coding:utf-8 -*-
#@Time : 2021/10/29 0029 9:28
#@Author: Joword
#@File : Literature.py

import pandas as pd
from utils import pmid_groupby
from read_data import evidences,pmid_path

PATH = './data/'
TEMP_PATH = './data/process_result/'

class Literature(object):
	
	def __init__(self,path:str):
		self.path=path
		self.pmid_groupby = [pmid_groupby(pmid_path+i) for i in evidences]
		self.pmids_merge = self.filter_dup
	
	@property
	def filter_dup(self):
		u'''合并各个证据项间的结果并去重
		:return:file
		'''
		df0 = pd.DataFrame(pd.concat(self.pmid_groupby, axis=0))
		df1 = pd.DataFrame(df0.groupby(['variant_id'], as_index=False)['submitter', 'publication'].agg(lambda x: x.str.cat(sep='|')))
		# df1['publication'] = df1['publication'].apply(lambda x:", ".join(list(set(str(x).split(", ")))))
		# df1['submitter'] = df1['submitter'].apply(lambda x:", ".join(list(set(str(x).split(", ")))))
		df1.to_csv(TEMP_PATH+"pmid_temp_result.txt",sep='\t',index=None)
		return df1
	
	def pmid_clean(self):
		u'''文献数据清洗，主要合并多个证据项间相同的文献与submitter
		:return: list
		'''
		with open(TEMP_PATH+"pmid_temp_result.txt","r+") as file:
			with open(PATH+"user_pmids.txt","w+") as g:
				next(file)
				g.write("variantId\tsubmitter\tpmids\n")
				lines = [i.strip().split("\t") for i in file.readlines()]
				for line in lines:
					if len(line[1].split("|")) > 1:
						# 多个数据
						if len(set(line[1].split("|"))) == 1:
							line[1] = "".join(list(set(line[1].split("|"))))
							line[2] = ", ".join(list(set(line[2].split("|"))))
						elif len(set(line[1].split("|"))) > 1:
							list1=[{line[1].split("|")[i]:line[2].split("|")[i]} for i in range(0,len(line[1].split("|")))]
							temp = {}
							for i in line[1].split("|"):
								pmids = []
								for j in list1:
									if i == list(j.keys())[0]:
										pmids.append(list(j.values())[0])
										temp[i] = ", ".join(list(set(pmids)))
							line[1] = "|".join(list(temp.keys()))
							line[2] = "|".join(list(temp.values()))
						g.write("\t".join(line) + "\n")
					else:
						# 单个数据对应单/多文献
						if len(line[2].split("|")) > 1:
							line[2] = ", ".join(line[2].split("|"))
						g.write("\t".join(line) + "\n")

# if __name__ == '__main__':
# 	test = Literature(pmid_path)
# 	test.pmid_clean()