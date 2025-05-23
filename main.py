import sqlite3
import random

from engine.population import Individual, Population
from domains.sql import seeds, fitness, parser


def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE numbers(value INTEGER)")
    conn.executemany("INSERT INTO numbers(value) VALUES(?)", [(i,) for i in range(100)])
    return conn


def mutate(query: str) -> str:
    return query + " "


def crossover(a: str, b: str) -> str:
    mid = len(a) // 2
    return a[:mid] + b[mid:]


if __name__ == "__main__":
    conn = setup_db()
    random.seed(0)
    individuals = [Individual(id=i, genome=q) for i, q in enumerate(seeds.SEEDS)]
    pop = Population(individuals)

    def fitness_fn(q: str) -> float:
        return fitness.evaluate(q, conn)

    best = pop.evolve(mutate, crossover, fitness_fn, population_size=4, generations=2)
    print("Best query:", parser.prettify(best.genome))
    conn.close()
