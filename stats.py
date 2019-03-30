import csv
import re

def row_feature(row):
    return row[3]

def row_hoods(row):
    return row[5:]

def stoi(value):
    if isinstance(value, str):
        return int(value.replace(',', ''))
    else:
        return value

def get_data(csv_reader, key, char=None):
    data = []
    keys = set()
    for row in csv_reader:
        row_key = str.join(', ', row[0:2])
        feature = row_feature(row)
        if row_key == key and (char == None or re.match(char, feature)) and feature not in keys:
            data.append((feature, [stoi(r) for r in row_hoods(row)]))
            keys.add(feature)
    return data

def csvfy(file):
    return [row for row in csv.reader(file, delimiter=',')]

def transpose(matrix):
    trans = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if (len(trans) <= x):
                trans.append([])
            trans[x].append(matrix[y][x])
    return trans

def score_hoods(data, cat_weights):
    weights = [c / sum(cat_weights) for c in cat_weights]
    matrix = [d[1] for d in data]
    trans = transpose(matrix)

    totals = [sum(row) for row in trans]
    fracs = [[(v / t * 100) for v in row] for row, t in zip(trans, totals)]
    scores = [[f * w for f,w in zip(row, weights)] for row in fracs]
    raw = [sum(s) for s in scores]
    return normalize(raw, weights)

def normalize(raw, weights):
    highest = max(weights) * 100
    lowest = min(weights) * 100
    return [round((r - lowest) / (highest - lowest) * 100) for r in raw]

def invert_scores(scores):
    return [100 - s for s in scores]

with open("2016_neighbourhood_profiles.csv","r") as file:
    csv = csvfy(file)
    props = {str.join(', ', row[0:2]) for row in csv}
    ages = get_data(csv, "Population, Age characteristics", "[^\(]*$")
    age_weights = [4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5, 4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5]
    print(invert_scores(score_hoods(ages, age_weights)))

    income = get_data(csv, "Income, Income of households in 2015", '.*,000.*')
    income_weights = [r for r in range(50, 29, -1)]
    print(invert_scores(score_hoods(income, income_weights)))

    #print([v[0] for v in income])