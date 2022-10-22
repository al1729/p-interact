data = []

value_matrix = []
for i in range(6):
    x = [0] * 6
    value_matrix.append(x)

temp = 0

with open("/Users/aguo/Desktop/P-Interact Stuff/p-interact/sentence-transformers/gridsearch_cosinedist.txt") as file:
    for line in file:
        if line != "\n":
            temp += 1

            l_strip = line.rstrip()
            l_strip = l_strip.split(": ")

            cos_dist = l_strip[1]
            
            line_vals = l_strip[0][:-4]
            line_vals = line_vals.split('_')
            
            # 0.2x + 0.8 = y -> x = 5y - 4
            freq_pen = float(line_vals[2])
            freq_index = int(5 * freq_pen - 4)
            pres_pen = float(line_vals[3])
            pres_index = int(5 * pres_pen -4)
            
            value_matrix[freq_index][pres_index] = value_matrix[freq_index][pres_index] + float(cos_dist)


for i in range(6):
    for j in range(6):
        value_matrix[i][j] = value_matrix[i][j] / 5
        print(value_matrix[i][j])


print(value_matrix)
print(temp)