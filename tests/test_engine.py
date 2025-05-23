import sqlite3
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from engine.population import Individual, Population
from domains.sql import parser, fitness, seeds


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


def test_evolution_cycle():
    conn = setup_db()
    random.seed(0)
    individuals = [Individual(id=i, genome=q) for i, q in enumerate(seeds.SEEDS)]
    pop = Population(individuals)

    def fitness_fn(q: str) -> float:
        return fitness.evaluate(q, conn)

    best = pop.evolve(mutate, crossover, fitness_fn, population_size=4, generations=2)
    assert parser.is_valid_sql(best.genome, conn)
    conn.close()
