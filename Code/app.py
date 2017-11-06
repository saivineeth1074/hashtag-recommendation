"""
	Program: main code to recommend hashtags given a post (end-to-end code)
"""

import os
import csv
import RWR
import LTModel
import domainLink

def similarDesc(row):
	return

def similarContent(row):
	return

def domainLink(row):
	res = domainLink.domain("politics.csv",5)
	return res

def RWR(row):
	entities = [r.strip()[1:-1] for r in row[10].split(",")]
	res = RWR.rwr(entities)
	return res

def LTRes(row):
	entities = [r.strip()[1:-1] for r in row[10].split(",")]
	res = LTModel.LT(entities)
	return res

if(__name__ == "__main__"):
	with open("politics_test.csv", "r") as file:
		reader = csv.reader(file)
		next(reader, None)
		for row in reader:
			descRes = similarDesc(row)
			contentRes = similarContent(row)
			domainRes = domainLink(row)
			rwrRes = RWR(row)
			ltRes = LTRes(row)
			break
