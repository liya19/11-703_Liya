import numpy as np
import random


class Individ:
    def __init__(self):
        # Объявляем атрибут "А" нашего индивида (это будет сама строка 010..101)
        self.A = np.random.randint(0, 2, 30)
        # Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
        self.fit = 0
        # Эта функция нашего индивида как раз отвечает за подсчёт "живучести" (считает сумму)

    def fitness(self):
        summa = 0
        for i in range(30):
            summa = summa + self.A[i]
            self.fit = summa


class Population:
    def __init__(self):
        # храним популяцию
        self.B = []
        for i in range(10):
            c = Individ()
            self.B.append(c)

    def info(self):
        for i in range(10):
            for j in range(30):
                print(self.B[i].A[j],
                      end="")
            print("=",
                  end="")
            self.B[
                i].fitness()
            print(self.B[i].fit)


pop1 = Population()
print("информация о стартовой популяции")
pop1.info()

Mother = Individ()
Father = Individ()
Son1 = Individ()  # 10 родителей и 10 их детей (по два сына у каждой из пяти пар родителей).
Son2 = Individ()
ParAndSons = []

for j in range(
        20):
    ParAndSons.append(
        Individ())
print("\n")
#  ЕСТЕСТВЕННЫЙ ОТБОР!!!11
print("естественный отбор")
# ограничение в 60 поколений.
for p in range(60):
    # За них мы должны успеть вырастить целое поколение мутантов-переростков.
    # Мы всегда можем увеличить количество поколений и увеличить вероятность нахождения ответа.
    # Или уменьшить, если наш механизм скрещиваний очень крутой, и мы очень быстро (за 20-30 поколений) находим ответ.
    for i in range(10):
        for j in range(30):
            ParAndSons[i].A[j] = pop1.B[i].A[j]

    # Счётчик для реализации небанального скрещивания
    tt = 0
    # берём 5 пар родителей
    for s in range(0, 10, 2):
        for j in range(
                30):
            #мамы последние 5 индивид популяции
            Mother.A[j] = pop1.B[tt + 5].A[
                j]
            Father.A[j] = pop1.B[random.randint(0, 9)].A[
                j]
        tt = tt + 1
        ran = random.random()

        #скрещивание
        if (ran > 0.8):
            for n in range(5):
                # Берём первые 5 элементов у папы и у мамы (для сына1 и сына2 соответственно).
                Son1.A[n] = Father.A[n]
                Son2.A[n] = Mother.A[n]

            for n in range(5,
                           30):  # берём остальные 25 элементов у мамы и у папы для сына1 и сына2 соответственно (крест-накрест)

                Son1.A[n] = Mother.A[n]
                Son2.A[n] = Father.A[n]

        if ((ran > 0.6) & (ran <= 0.8)):  # Тот же самый крест-накрест, только теперь самого тривиального вида.
            for n in range(15):  # Первые 15 у папы и вторые 15 у мамы для сына1.
                Son1.A[n] = Father.A[n]  # И первые 15 у мамы и вторые 15 у папы для сына2.
                Son2.A[n] = Mother.A[n]
            for n in range(16, 30):
                Son1.A[n] = Mother.A[n]
                Son2.A[n] = Father.A[n]

        if ((ran < 0.6) & (
                ran >= 0.4)):  # Крест накрест. Зеркален первому методу скрещивания. (только не первые 5 элементов берём, а последние)
            for n in range(25):
                Son1.A[n] = Father.A[n]
                Son2.A[n] = Mother.A[n]
            for n in range(25, 30):
                Son1.A[n] = Mother.A[n]
                Son2.A[n] = Father.A[n]

        if ((ran < 0.4) & (ran >= 0.3)):  # Срединный крест-накрест + инверсия.
            for n in range(15):
                Son1.A[n] = Father.A[14 - n]
                Son2.A[n] = Mother.A[14 - n]
            for n in range(15, 30):
                Son1.A[n] = Mother.A[44 - n]
                Son2.A[n] = Father.A[44 - n]

        if (ran < 0.3):  # Тут берём для сына1 первые 15 элементов папы + первые 15 элементов мамы.
            for n in range(15):  # А для сына2 берём вторые 15 элементов мамы + вторые 15 элементов папы.
                Son1.A[n] = Father.A[n]
                Son1.A[n + 15] = Mother.A[n]
                Son2.A[n] = Mother.A[n + 15]
                Son2.A[n + 15] = Father.A[n + 15]

        for i in range(
                30):  # Тут мы закидываем наших получившихся в результате скрещивания s-той пары родителей Сына1 и Сына2 во вторую половину массива "Отцы и дети".
            ParAndSons[10 + s].A[i] = Son1.A[i]
            ParAndSons[11 + s].A[i] = Son2.A[i]

    for r in range(17, 18):  # Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
        for w in range(
                30):  # Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
            if random.random() < 0.00001:  # Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
                if ParAndSons[r].A[w] == 1:  # инвертируем каждую из его 30 нулей и единиц.
                    ParAndSons[r].A[
                        w] = 0
                if ParAndSons[r].A[w] == 0:
                    ParAndSons[r].A[w] = 1

    for i in range(
            20):
        ParAndSons[
            i].fitness()

    for m in range(len(ParAndSons) - 1, 0,
                   -1):  # Ранжирование (методом пузырька). Лёгкие всплывают наверх, а тяжёлые оказываются внизу.
        for b in range(
                m):
            if ParAndSons[b].fit > ParAndSons[
                b + 1].fit:
                mem = ParAndSons[
                    b]
                ParAndSons[b] = ParAndSons[b + 1]
                ParAndSons[b + 1] = mem

    for i in range(10):
        for j in range(30):  # Тут мы перебрасываем лучших из массива "отцов и детей" (т.е. последние 10 индивидов)
            pop1.B[i].A[j] = ParAndSons[i + 10].A[j]

    pop1.info()

