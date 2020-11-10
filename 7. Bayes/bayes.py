import numpy as np
import pandas as pd

symptom = pd.read_csv('symptom.csv', delimiter=';')
disease_people = pd.read_csv('disease.csv', delimiter=';')

result_disease = ''
disease_percent = []
inspection = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
people_number = disease_people['количество пациентов']
inspection_result_priem = []

for i in range(len(inspection) - 1):
    if (inspection[i] == 1):
        inspection_result_priem = symptom.iloc[i][0]
print("Какие заболевания назвали:", inspection_result_priem)

# какой процент людей болел
for i in range(len(disease_people) - 1):
    disease_percent.append((people_number[i] / 303))

p = 0
p1 = 0
for i in range(len(disease_people) - 1):
    p_c_x = disease_percent[i]
    p_x = 1
    for j in range(1, len(inspection) + 1):
        if (inspection[i] == 1):
            p_x *= symptom.iloc[i][1]
            p_c_x *= 0.5
    p1 = p_c_x / p_x
    if (p < p1):
        p = p1
        result_disease = disease_people.iloc[i][0]
        print(result_disease, disease_percent[i])

print('Итоговое заболевание: ', result_disease)
