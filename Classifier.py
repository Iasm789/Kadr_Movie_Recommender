import numpy as np
from operator import itemgetter


class KNearestNeighbours:
    def __init__(self, data, target, test_point, k):
        self.data = data
        self.target = target
        self.test_point = test_point
        self.k = k
        self.distances = list()
        self.categories = list()
        self.indices = list()
        self.counts = list()
        self.category_assigned = None

    @staticmethod
    def dist(p1, p2):
        """Метод возвращает евклидово расстояние между двумя точками"""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def fit(self):
        """Метод, который выполняет классификацию KNN"""
        # Создаем список кортежей (расстояние, индекс) от тестовой точки до каждой точки в данных
        self.distances.extend([(self.dist(self.test_point, point), i) for point, i in zip(self.data, [i for i in range(len(self.data))])])
        # Отсортируем расстояния в порядке возрастания
        sorted_li = sorted(self.distances, key=itemgetter(0))
        # Извлекаем индексы k ближайших точек из данных
        self.indices.extend([index for (val, index) in sorted_li[:self.k]])
        for i in self.indices:
            self.categories.append(self.target[i])
        self.counts.extend([(i, self.categories.count(i)) for i in set(self.categories)])
        self.category_assigned = sorted(self.counts, key=itemgetter(1), reverse=True)[0][0]
