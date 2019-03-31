import csv
import re
import json
import math

def row_feature(row):
    return row[3]

def row_hoods(row):
    return row[5:]
    #return row[21:24]
    #return row[21:22]

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

NUM_SHIFT_INCREMENTS = 5
def equalize_histo(histo, offset):
    average = sum(histo) / len(histo)
    shifted = [h + (average - h) * (offset / (NUM_SHIFT_INCREMENTS - 1)) for h in histo]
    return shifted

def score_hoods(data, cat_weights, offset, shifter):
    norm_weights = [c / sum(cat_weights) for c in cat_weights]
    weights = shifter(norm_weights, offset)
    matrix = [d[1] for d in data]
    trans = transpose(matrix)
    values = trans

    totals = [sum(row) for row in values]
    fracs = [[(v / t) for v in row] for row, t in zip(values, totals)]
    scores = [[f * w for f,w in zip(row, weights)] for row in fracs]
    scores = [s for s in scores]
    raw = [sum(s) for s in scores]
    return raw

def normalize(raw):
    return [round(r, 2) for r in raw]

def print_keys(data):
    print("{}: {}".format(len(data), [d[0] for d in data]))

def invert_scores(scores):
    return [1 - s for s in scores]

def get_age_scores(csv, offset, shifter):
    ages = get_data(csv, "Population,Age characteristics", "[^\\(]*$")
    age_weights = [4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5, 4,4,4,4,5,5,5,3.5,3.5,5,5,8,8,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5]
    age_weights = [10 - w for w in age_weights]
    age_scores = score_hoods(ages, age_weights, offset, shifter)
    return age_scores

def get_income_scores(csv, offset, shifter):
    income = get_data(csv, "Income,Income of households in 2015", '.*,000.*')
    income_weights = [r for r in range(29, 50)]
    income_scores = (score_hoods(income, income_weights, offset, shifter))
    return income_scores

def get_edu_scores(csv, offset, shifter):
    education = get_data(csv, 'Education,Highest certificate, diploma or degree')
    education_weights = [50+44, 56+51, 56+51, 58+52, 58+52, 58+52, 62+57, 62+60, 62+60, 62+60]
    ed_scores = score_hoods(education, education_weights, offset, shifter)
    return ed_scores

def get_race_scores(csv, offset, shifter):
    race = get_data(csv, 'Visible minority,Visible minority population')
    race_weights = [78, 82, 71, 82, 78, 78, 82, 78, 82, 82, 78, 78, 77]
    race_scores = score_hoods(race, race_weights, offset, shifter)
    return race_scores

def get_housing_scores(csv, offset, shifter):
    housing = get_data(csv, 'Housing,Household characteristics', '.*Spending.*')
    print(housing)
    housing_weights = [1,1.1]
    housing_scores = (score_hoods(housing, housing_weights, offset, shifter))
    return housing_scores

def get_codes(csv):
    codes = get_data(csv, "Neighbourhood Information,Neighbourhood Information")
    return codes[0][1]

def get_names(csv):
    return row_hoods(csv[0])

def find_code(codes, names, name):
    for i in range(len(codes)):
        if re.match(name, names[i]):
            return i
    return -1

def get_score(ages, incomes, edus, races, housings):
    return [(a + i + e + r + h) / 5 for a,i,e,r,h in zip(ages, incomes, edus, races, housings)]

with open("python/2016_profiles_cleaned.csv","r") as file:
    csv = csvfy(file)
    props = {str.join(', ', row[0:2]) for row in csv}

    codes = get_codes(csv)
    names = get_names(csv)
    index = find_code(codes, names, ".*Thorn.*")
    print("{}, {}: {}".format(index, codes[index], names[index]))

    output = {
        "codes": codes,
        "neighbourhoods": names,
        "age": [],
        "income": [],
        "education": [],
        "race": [],
        "housing": []
    }

    def rescale(scores, range):
        #return scores;
        return [round((s - range[0]) / (range[1] - range[0]) * 100, 2) for s in scores]
    
    def range_of(scores):
        return (min(scores), max(scores))

    ar = range_of(get_age_scores(csv, 0, equalize_histo))
    ir = range_of(get_income_scores(csv,0, equalize_histo))
    er = range_of(get_edu_scores(csv, 0, equalize_histo))
    rr = range_of(get_race_scores(csv, 0, equalize_histo))
    hr = range_of(get_housing_scores(csv, 0, equalize_histo))

    for i in range(NUM_SHIFT_INCREMENTS):
        output["age"].append(rescale(get_age_scores(csv, i, equalize_histo), ar))
        output["income"].append(rescale(get_income_scores(csv, -i, equalize_histo), ir))
        output["education"].append(rescale(get_edu_scores(csv, i, equalize_histo), er))
        output["race"].append(rescale(get_race_scores(csv, i, equalize_histo), rr))
        output["housing"].append(rescale(get_housing_scores(csv, -i, equalize_histo), hr))

    mins = []
    maxs = []
    for a in output["age"]:
        for i in output["income"]:
            for e in output["education"]:
                for r in output["race"]:
                    for h in output["housing"]:
                        scores = get_score(a, i, e, r, h)
                        mins.append(min(scores))
                        maxs.append(max(scores))

    output["globalMax"] = max(maxs)
    output["globalMin"] = min(mins)

    print(output)

    with open("docs/scores.js", "w+") as out:
        outjson = json.dumps(output, separators=(',',':'))
        out.write("healthArray = {};".format(outjson))