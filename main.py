# -*- coding:utf-8 -*-
#@Time : 2021/10/29 0029 9:27
#@Author: Joword
#@File : main.py

import pandas as pd
from Literature import Literature
from read_data import evidences,pmid_path,clinvar,information,pmids

class Info(object):
	
	def __init__(self):
		self.literature = Literature(pmid_path)
		self.clinvar = clinvar
	
	def merge(self):
		u'''合并clinvar、user_collect、pmid数据
		:return: file
		'''
		with open(information,"r+") as file:
			with open(pmids,"r+") as pmid:
				with open("result.txt","w+") as f:
					next(file)
					next(pmid)
					f.write("variantId\tchr\tstart\tstop\tref\talt\tsubmitter\tchgvs\tgene\tphgvs\tconsequence\tauto_interpretation\tcriteria_provided\treview_status_star\treview_status\tlof\tclinvar_path\tpmids\n")
					infos = [i.strip().split("\t") for i in file.readlines()]
					literatures = [i.strip().split("\t") for i in pmid.readlines()]
					all_lists,sum_lists = [],[]
					for info in infos:
						for lit in literatures:
							if info[0] == lit[0]:
								info_name_lists,pmid_name_lists = info[6].split("|"),lit[1].split("|")
								single_list,mullist = [],[]
								name_lists = list(set(info_name_lists) & set(pmid_name_lists))
								dict1 = {'vd': info[0], 'chr': info[1], 'start': info[2],'stop': info[3], 'ref': info[4],'alt': info[5],
											'submitter': info[6].split("|")[0],'chgvs': info[7], 'gene': info[8],'phgvs': info[9],
										 	'consequence': info[10].split("|")[0],
											'auto_interpretation':info[11].split("|")[0],
											'criteria_provided':info[12].split("|")[0],
											'review_status_star': "",'review_status': "",'lof': "",'clinvar_path': "",
											'pmids': ""}
								dict_intersection = {lit[1].split("|")[i]:lit[2].split("|")[i] for i in range(0,len(pmid_name_lists)) if lit[1].split("|")[i] in name_lists}
								dict_all = {lit[1].split("|")[i]:lit[2].split("|")[i] for i in range(0,len(lit[1].split("|")))}
								if len(info[6].split("|"))==1 and len(name_lists)>0:
									single_list13,single_list17={},{}
									if len(info)==17:
										dict1['review_status_star'] = info[13]
										dict1['review_status'] = info[14]
										dict1['lof'] = info[15]
										dict1['clinvar_path'] = info[16]
										dict1['pmids'] = dict_intersection[info[6].split("|")[0]]
										single_list17[info[6].split("|")[0]] = dict1
										single_list.append(single_list17)
									elif len(info)==13:
										dict1['pmids'] = dict_intersection[info[6].split("|")[0]]
										single_list13[info[6].split("|")[0]] = dict1
										single_list.append(single_list13)
									all_lists.extend(single_list)
								elif len(info[6].split("|"))>1 and len(name_lists)>0:
									for i in range(0,len(info[6].split("|"))):
										mul_list13, mul_list17 = {}, {}
										if len(info) == 17 and info[6].split("|")[i] in name_lists:
											dict1['review_status_star'] = info[13]
											dict1['review_status'] = info[14]
											dict1['lof'] = info[15]
											dict1['clinvar_path'] = info[16]
											dict1['pmids'] = dict_all[info[6].split("|")[i]]
											mul_list17[info[6].split("|")[i]] = dict1
											mullist.append(mul_list17)
										elif len(info)==13 and info[6].split("|")[i] in name_lists:
											if info[6].split("|")[i] in list(dict_all.keys()):
												dict1['pmids'] = dict_all[info[6].split("|")[i]]
												mul_list13[info[6].split("|")[i]] = dict1
												mullist.append(mul_list13)
										all_lists.extend(mullist)
					f.write("\n".join(["\t".join(list(list(col.values())[0].values())) for col in all_lists]))
								
if __name__ == '__main__':
	test = Info()
	test.merge()