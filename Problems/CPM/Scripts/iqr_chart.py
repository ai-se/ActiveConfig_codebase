def list_files():
    log_directory = "../Logs"
    import os
    files = [file for file in os.listdir(log_directory) if file[-4:]==".txt"]
    return files

def get_median_iqr(filename):
    f = open(filename, "r")
    data = []
    for i, line in enumerate(f):
        if i == 0: continue
        content = line.split(",")
        if content[-1].replace("\n", "") == "base_line": content[-1] = "Baseline"
        elif content[-1].replace("\n", "") == "random_where": content[-1] = "Random"
        elif content[-1].replace("\n", "") == "exemplar_where": content[-1] = "Exemplar"
        elif content[-1].replace("\n", "") == "east_west_where": content[-1] = "East-West"
        data.append([content[0], float(content[1]), float(content[2]), content[-1].replace("\n", "")])
    return data

def get_template():
    filename = "iqr_chart_template.txt"
    return open(filename, "r").readlines()

def transforming_data(filename):
    filename = "../Logs/" + filename
    lines = get_median_iqr(filename)
    from collections import defaultdict
    content = defaultdict(list)
    for i, line in enumerate(lines):
        if line[-1] in content.keys(): content[line[-1]].append([round(line[1], 2), round(line[2], 2)])
        else: content[line[-1].replace(" ", "")] = [[round(line[1],2), round(line[2], 2)]]

    return content


def get_data():
    template_lines = {"apache": [10, 11, 12, 13], "BDBC": [14, 15, 16, 17], "BDBJ": [18, 19, 20, 21],
                      "SQL": [22, 23, 24, 25], "LLVM": [26, 27, 28, 29], "X264": [30, 31, 32, 33]}
    template = get_template()
    files = list_files()
    for file in files:
        data = transforming_data(file)
        line_numbers = template_lines[file[:-4].split("_")[1]]
        for line_number in line_numbers:
            temp = [t.replace(" ", "") for t in template[line_number].split("&")]
            dd = [d for sublist in data[temp[1]] for d in sublist]
            newline = template[line_number].split("&")
            for i, (l, m) in enumerate(zip(newline[2:], dd)):
                newline[2+i] = m
            newline[-1] = str(newline[-1]) + " \\\ "
            template[line_number] = " & ".join([str(b) for b in newline])

    for t in template:
        print t


    # for t in template:
    #     print t

filename = "../Logs/cpm_BDBJ.txt"
# print get_median_iqr(filename)
# # get_template()
get_data()