from os import listdir
from os.path import join
import csv

entries = {}

directory = "./primate_image/train/labels/"

for fname in listdir(directory):
    label = fname.split('.')[0]
    entries[label] = []

    with open(join(directory, fname)) as f:
        lines = f.readlines()
        for l in lines:
            try:
                (_, v1, v2, v3, v4) = l[:-1].split(' ')
                entries[label].append([v1, v2, v3, v4])
            except ValueError:
                print(label) #to see which data is missing


print(len(entries.keys()))
print(list(entries.items())[0])

csv_entries = []

with open('./allcsv.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        csv_entries.append(row) #every row tuple

print(csv_entries[0])

idx = {label: 0 for label in entries.keys()}
to_print = {label: False for label in entries.keys()} #bounding box, no landmarks


for i in range(0, len(csv_entries)-1, 3):
    label = csv_entries[i][3].split('.')[0]

    if label not in entries.keys():
        continue

    left = csv_entries[i]
    right = csv_entries[i+1]
    mouth = csv_entries[i+2]
    (lx, ly) = (left[1], left[2])
    (rx, ry) = (right[1], right[2])
    (mx, my) = (mouth[1], mouth[2])

    entry = [lx, ly, rx, ry, mx, my]

    i = idx[label]
    try:
        entries[label][i] += entry
        to_print[label] = True
        idx[label] += 1
    except IndexError:
        print(label)
        pass

print(entries['2240'])

def write_to_file(entries, f):
    for k,v in entries.items():
        if not to_print[k]:
            continue

        f.write(f'# {k}\n')
        for e in v:
            if len(e) != 10:
                continue
            rep = ' '.join(e)
            f.write(f'{rep}\n')
        f.write('\n')

f = open('out.txt', 'w')

write_to_file(entries, f)
