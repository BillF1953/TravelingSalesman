import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)
np.random.seed(1)


def get_first_tour(num_cities):
    return (np.random.choice(num_cities, num_cities, replace=False))


def get_tour_distance(tour, points):
    """

    :param tour:[4,2,3,1]
    :return:
    """
    distance = 0
    for i in range(len(tour) - 1):
        distance += np.linalg.norm((points[tour[i]] - points[tour[i + 1]]))
    distance += np.linalg.norm(points[tour[0]] - points[tour[len(tour) - 1]])

    return distance


def test_swap(i, j, old_tour, best_distance, points):
    new_tour = np.copy(old_tour)

    rev_end = i - 1

    if rev_end < 0:
        rev_end = None

    new_tour[i:(j + 1)] = new_tour[j: rev_end: -1]
    new_distance = get_tour_distance(new_tour, points)

    logging.debug("New Tour {} Old Tour {} i: {} j: {} "
                  "New Distance {} Best Distance{}".format(new_tour,
                                                           old_tour, i, j, new_distance, best_distance))

    if new_distance < best_distance:
        return new_tour, new_distance

    else:
        return old_tour, best_distance


def do2opt(tour, points):
    num_cities = len(tour)
    old_distance = get_tour_distance(tour, points)

    for i in range(num_cities - 1):
        for j in range(i + 1, num_cities):
            tour, distance = test_swap(i, j, tour, old_distance, points)
            # if distance == old_distance:
            #     return tour, distance

            old_distance = distance

            logging.debug("Tour {} Distance {}".format(tour, distance))

    return tour, old_distance


if __name__ == "__main__":
    num_cities = 10
    points = np.random.randint(0, 1000, size=(num_cities, 2))
    logging.debug(points)
    starting_tour = get_first_tour(num_cities)
    print(do2opt(starting_tour, points))

    # get_distance
    # perform cut
    # reverse cut
    # test_distance
    #
