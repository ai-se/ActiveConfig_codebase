
def validate(solution):
    if sum(solution) == 0: return False
    if solution[0] != 1: return False
    if solution[1] != 1: return False
    if solution[2] != 1: return False
    if sum([solution[3], solution[4]]) != 1: return False
    if solution[4] == 1 and solution[5] != 1: return False
    if solution[4] == 0 and sum(solution[5:10]) != 0: return False
    if solution[4] == 1 and solution[6] != 1: return False
    if solution[6] == 1 and sum([solution[7], solution[8]]) != 1: return False
    if solution[10] != 1: return False
    if solution[10] == 1 and sum([solution[11], solution[12]]) != 1: return False
    if solution[13] != 1: return False
    if solution[14] != 1: return False
    if solution[19] == 1 and solution[15] != 1: return False
    if solution[16] != 1: return False
    if solution[16] == 1 and solution[17] != 1: return False
    if solution[16] == 1 and solution[18] != 1: return False
    if solution[20] == 1 and solution[21] != 1: return False
    if solution[20] == 1 and solution[22] != 1: return False
    if solution[22] == 1 and sum([solution[23], solution[24]]) != 1: return False
    if solution[20] == 0 and sum(solution[21:25]) != 0: return False
    return True



filename = "./BDBJ_AllMeasurements.csv"
lines = open(filename, "r").readlines()[1:]
content = []
for line in lines:
    temp = line.replace("Y","1").replace("N","0").replace("\r\n", "")
    temp = map(int, temp.split(",")[:-1])
    assert(validate(temp) is True), "Something is wrong"

