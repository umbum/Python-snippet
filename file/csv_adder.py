import csv


month = '11'

w = open("/Users/user/source/data/차액정산{}월_일반등급.csv".format(month), 'w', newline='')
writer = csv.writer(w)

diff_f = open("/Users/user/source/data/차액정산{}월.csv".format(month), 'r', encoding='utf-8')
diff_reader = csv.reader(diff_f)
total_f = open("/Users/user/source/data/총매출{}월.csv".format(month), 'r', encoding='utf-8')
total_reader = csv.reader(total_f)

result = {}

for line in diff_reader:
    if line[2] == 'scale4':
        pass
    
    key = line[1] + '-' + line[3]
    if result.get(key) is None:
        result[key] = [0, 0]

    result[key][0] += int(line[4])
    result[key][1] += int(line[5])

for k, v in result.items():
    print(k, v)

print("---------------")

result2 = {}

for line in total_reader:
    key = line[1] + '-' + line[2]

    if result.get(key) is not None:
        total = int(line[3]) - int(result[key][0])
        comm = int(line[4]) - int(result[key][1])
    else:
        total = int(line[3])
        comm = int(line[4])

    result2[key] = [total, comm]

for k, v in result2.items():
    print(k, v)
    writer.writerow([*k.split('-'), 'scale4', *v])


w.close()
diff_f.close()
total_f.close