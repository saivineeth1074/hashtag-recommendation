import os, sys
import csv
import requests

f = open("entities.csv", "w")
if(not f):
    print("Cant create new csv file.")
    sys.exit(0)

writer = csv.writer(f, delimiter=',')
writer.writerow(["Id", "Section", "Title", "Timestamp", "URL", "Description", "Content", "Tags", "SpotEntities", "SpotTopEntities", "LabelEntites", "LabelTopEntities"])

with open("politics_data.csv", "r") as file:
    count = 0

    reader = csv.reader(file)
    for row in reader:
        #Header row
        if(count == 0):
            count += 1
            continue
        elif(count == 950):
            break

        url = "https://api.dandelion.eu/datatxt/nex/v1/"
        parameters = {
            "token" : "ec49ad6d0620425fa303bbb38cbdef65",
            "top_entities" :"20",
            "text": row[6]
        }

        #REST API call
        resp = requests.get(url, params=parameters)
        Json = resp.json()

        spotEntities = []
        spotTopEntities = []
        labEntities = []
        labTopEntities = []

        #Get all the entities in the post
        try:
            for entity in Json["annotations"]:
                spotEntities.append(entity["spot"])
                labEntities.append(entity["label"])
            spotEntities = list(set(spotEntities))            
            labEntities = list(set(labEntities))
        except:
            print(row[0], resp.content)
            pass

        #Get the top entities in the post
        try:
            for entity in Json["topEntities"]:
                Id = entity["id"]

                #Search for the entity name in the annotations key
                for ent in Json["annotations"]:
                    if(ent["id"] == Id):
                        spotTopEntities.append(ent["spot"])
                        labTopEntities.append(ent["label"])
                        break
            spotTopEntities = list(set(spotTopEntities))
            labTopEntities = list(set(labTopEntities))
        except:
            print(row[0], resp.content)
            pass

        newRow = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(spotEntities)[1:-1], str(spotTopEntities)[1:-1], str(labEntities)[1:-1], str(labTopEntities)[1:-1]]
        writer.writerow(newRow)
        count += 1
f.close()