import csv

def transform(filename):
    return "../" + filename

def read_csv(filename, header=False):
    data = []
    f = open(filename, 'rb')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        if i == 0 and header is False: continue  # Header
        elif i ==0 and header is True:
            H = row
            continue

        data.append([i-1]+[1 if x == "Y" else 0 for x in row[:-1]] + [float(row[-1]) * (10**4)]) # TODO: DecisionTree regressor returns int values. As a work around I multiply all the class values by 10**4
    f.close()
    if header is True: return H, data
    return data


