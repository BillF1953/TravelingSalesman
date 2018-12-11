
"""CSCI 538 Project Traveling Salesman
   Tyler Forrester  December 10th 2018"""

import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)
np.random.seed(1)


def get_first_tour(num_cities):
    """

    :param num_cities: Number of vertexs in graph
    :return: Random Tour of Graph
    """
    return (np.random.choice(num_cities, num_cities, replace=False))


def get_tour_distance(tour, points):
    """

    :param tour:[4,2,3,1]
    :return: Measures the Euclidean distance of the tour
    """
    distance = 0
    for i in range(len(tour) - 1):
        distance += np.linalg.norm((points[tour[i]] - points[tour[i + 1]]))
    distance += np.linalg.norm(points[tour[0]] - points[tour[len(tour) - 1]])

    return distance


def test_swap(i, j, old_tour, best_distance, points):
    """
    Function which swaps points and tests if the new tour is better than that old tour.
    In this variation the tour is
    :param i: Start of swap index
    :param j: End of swap index
    :param old_tour: The current tour
    :param best_distance: The current lowest distance founds
    :param points: 2-D points to measure euclidean distance
    :return: The current shortest tour and it's distance.
    """
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
    """

    :param tour: The random tour
    :param points: Location in Euclidean space
    :return: Best tour and distance
    """
    num_vertices = len(tour)
    max_distance = get_tour_distance(tour, points)

    for i in range(num_vertices - 1):
        for j in range(i + 1, num_vertices):
            tour, distance = test_swap(i, j, tour, max_distance, points)

            max_distance = distance

            logging.debug("Tour {} Distance {}".format(tour, distance))

    return tour, max_distance





if __name__ == "__main__":

    # generate random ten city graph.
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
