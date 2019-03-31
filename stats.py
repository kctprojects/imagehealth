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
        row_key = str.join(',', row[0:2])
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

def print_keys(data):
    print("{}: {}".format(len(data), [d[0] for d in data]))

def invert_scores(scores):
    return [100 - s for s in scores]

def get_scores(csv, ca, ci, ce, ch):
    ages = get_data(csv, "Population,Age characteristics", "[^\(]*$")
    age_weights = [4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5, 4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5]
    age_scores = invert_scores(score_hoods(ages, age_weights))

    income = get_data(csv, "Income,Income of households in 2015", '.*,000.*')
    income_weights = [r for r in range(50, 29, -1)]
    income_scores = invert_scores(score_hoods(income, income_weights))

    education = get_data(csv, 'Education,Highest certificate, diploma or degree')
    education_weights = [50+44, 56+51, 56+51, 58+52, 58+52, 58+52, 62+57, 62+60, 62+60, 62+60]
    ed_scores = score_hoods(education, education_weights)

    race = get_data(csv, 'Visible minority,Visible minority population')
    race_weights = [78, 82, 71, 82, 78, 78, 82, 78, 82, 82, 78, 78, 77]
    race_scores = score_hoods(race, race_weights)

    housing = get_data(csv, 'Housing,Household characteristics', '.*Spending.*')
    housing_weights = [1.5,1]
    housing_scores = score_hoods(housing, housing_weights)
    
    total = [(a + i + e + r + h) / 5 for a, i , e, r, h in zip(age_scores, income_scores, ed_scores, race_scores, housing_scores)]
    return total

with open("2016_profiles_cleaned.csv","r") as file:
    csv = csvfy(file)
    props = {str.join(', ', row[0:2]) for row in csv}

    codes = get_data(csv, "Neighbourhood Information,Neighbourhood Information")
    print(codes[0])
    print(min(codes[0][1]))

    print(get_scores(csv, 0, 0, 0, 0))