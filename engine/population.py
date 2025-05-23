from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Any, Callable, List


@dataclass
class Individual:
    """Container for a candidate in the population."""

    id: int
    genome: Any
    fitness: float | None = None


class Population:
    """Simple evolutionary population."""

    def __init__(self, individuals: List[Individual]):
        self.individuals: List[Individual] = individuals
        self.generation: int = 0

    def evaluate(self, fitness_fn: Callable[[Any], float]) -> None:
        """Assign fitness to each individual."""
        for ind in self.individuals:
            ind.fitness = fitness_fn(ind.genome)

    def select_top(self, k: int) -> List[Individual]:
        """Return top-k individuals by fitness (lower is better)."""
        return sorted(self.individuals, key=lambda x: x.fitness or float('inf'))[:k]

    def tournament_select(self, k: int) -> Individual:
        """Tournament selection."""
        competitors = random.sample(self.individuals, k)
        return min(competitors, key=lambda x: x.fitness or float('inf'))

    def evolve(
        self,
        mutate_fn: Callable[[Any], Any],
        crossover_fn: Callable[[Any, Any], Any],
        fitness_fn: Callable[[Any], float],
        population_size: int,
        generations: int,
        tournament_size: int = 2,
        elite_size: int = 1,
    ) -> Individual:
        """Run a simple (mu + lambda) evolution loop."""

        self.evaluate(fitness_fn)
        for _ in range(generations):
            next_individuals: List[Individual] = []
            # Elitism: carry over best individuals
            elites = self.select_top(elite_size)
            next_individuals.extend(
                [Individual(id=i, genome=e.genome, fitness=e.fitness) for i, e in enumerate(elites)]
            )
            # Generate offspring
            while len(next_individuals) < population_size:
                p1 = self.tournament_select(tournament_size)
                p2 = self.tournament_select(tournament_size)
                child_genome = crossover_fn(p1.genome, p2.genome)
                child_genome = mutate_fn(child_genome)
                next_individuals.append(Individual(id=len(next_individuals), genome=child_genome))
            self.individuals = next_individuals
            self.evaluate(fitness_fn)
            self.generation += 1
        return self.select_top(1)[0]
