"""
	Program: Implementation of RWR
"""

import csv
import networkx as nx
import operator

#Count the cooccurences of an entity and hashtag
entTagCount = dict()

#Pairwise tags cooccurence count
coOccCount = dict()

#Entity and tags count
entityCount = dict()
tagCount = dict()

#P(E/H)
probEH = dict()

#P(H/E)
probHE = dict()

#P(hj/hk)
pCoOcc = dict()

def preProcess():
	with open("politics_train.csv", "r") as file:
		reader = csv.reader(file)
		next(reader, None)

		for row in reader:
			rowTags = [r.strip() for r in row[7].split(",")]
			if("" in rowTags):
				rowTags.remove("")
			entities = [r.strip()[1:-1] for r in row[10].split(",")]

			#Entity count
			for entity in entities:
				if(entity in entityCount):
					entityCount[entity] += 1
				else:
					entityCount[entity] = 1

			#Tag count
			for tag in rowTags:
				if(tag in tagCount):
					tagCount[tag] += 1
				else:
					tagCount[tag] = 1

			#Tag co-occurence count
			for i in range(len(rowTags)):
				for j in range(i + 1, len(rowTags)):
					if(((rowTags[i], rowTags[j]) in coOccCount) or ((rowTags[j], rowTags[i]) in coOccCount)):
						coOccCount[(rowTags[i], rowTags[j])] += 1
					else:
						coOccCount[(rowTags[i], rowTags[j])] = 1

			#Entity tag count
			for entity in entities:
				for tag in rowTags:
					if((entity, tag) in entTagCount):
						entTagCount[(entity, tag)] += 1
					else:
						entTagCount[(entity, tag)] = 1

	#P(E/H) and P(H/E)
	for u, v in entTagCount.items():
		probEH[u] = float(v) / tagCount[u[1]]
		probHE[(u[1], u[0])] = float(v) / entityCount[u[0]]

	#P(hj/hk)
	for u, v in coOccCount.items():
		pCoOcc[u] = float(v) / tagCount[u[1]]
		pCoOcc[(u[1], u[0])] = float(v) / tagCount[u[0]]

def rwr(entities):
	preProcess()

	rowTags = set()
	for u, v in entTagCount.items():
		if(u[0] in entities):
			rowTags.add(u[1])
	rowTags = list(rowTags)

	DG = nx.DiGraph()
	DG.add_nodes_from(entities)
	DG.add_nodes_from(rowTags)

	#Tag co-occurence edges
	for i in range(len(rowTags)):
		for j in range(i + 1, len(rowTags)):
			if((rowTags[i], rowTags[j]) in pCoOcc):
				edgeIJ = pCoOcc[(rowTags[i], rowTags[j])]
				edgeJI = pCoOcc[(rowTags[j], rowTags[i])]
				DG.add_weighted_edges_from([(rowTags[i], rowTags[j], edgeIJ), (rowTags[j], rowTags[i], edgeJI)])

	#Entity-tag edges
	for i in range(len(entities)):
		for j in range(len(rowTags)):
			if((rowTags[j], entities[i]) in entTagCount):
				pHE = probHE[(rowTags[j], entities[i])]
				pEH = probEH[(entities[i], rowTags[j])]
				DG.add_weighted_edges_from([(entities[i], rowTags[j], pHE), (rowTags[j], entities[i], pEH)])

	#Add a personalization vector
	persVector = dict()
	for tag in rowTags:
		persVector[tag] = 0
	for entity in entities:
		persVector[entity] = 1

	#RWR
	res = nx.pagerank(DG, alpha = 0.75, personalization = persVector)
	res = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
	return res




