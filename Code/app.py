import os
import csv
import RWR

def similarDesc(row):
	return

def similarContent(row):
	return

def domainLink(row):
	return

def RWR(row):
	entities = [r.strip()[1:-1] for r in row[10].split(",")]
	res = RWR.rwr(entities)
	return res

def LTRes(row):
	return

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