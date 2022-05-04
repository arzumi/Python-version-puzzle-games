"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


# Your solve method MUST be a recursive function (i.e. it must make
# at least one recursive call to itself)
# You may NOT change the interface to the solve method.
class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if seen is None:
            seen = set()
        if puzzle.is_solved():
            return [puzzle]
        elif puzzle.fail_fast() is True:
            seen.add(f'{puzzle}')
            return []

        result = [puzzle]
        seen.add(f'{puzzle}')
        extensions = puzzle.extensions()
        for item in extensions:
            if f'{item}' not in seen:
                seen.add(f'{item}')
                temp = self.solve(item, seen)
                if temp:
                    result.extend(temp)
                    return result
        return []


# Hint: You may find a Queue useful here.
class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if seen is None:
            seen = set()
        if puzzle.is_solved():
            return [puzzle]
        elif puzzle.fail_fast():
            seen.add(f'{puzzle}')
            return []

        puzzle_path = Queue()
        start = [puzzle]
        puzzle_path.enqueue(start)
        while not puzzle_path.is_empty():
            temp = puzzle_path.dequeue()
            temp_extensions = temp[-1].extensions()
            for extension in temp_extensions:
                if f'{extension}' in seen:
                    continue   # go to the next iteration
                seen.add(f'{extension}')
                result = _bfshelper(extension, temp, puzzle_path)
                if result:
                    return result
                # if not extension.fail_fast():
                #     temp2 = temp.copy()
                #     temp2.append(extension)
                #     if extension.is_solved():
                #         return temp2
                #     else:
                #         puzzle_path.enqueue(temp2)

        return []


def _bfshelper(temp_extension: Puzzle, temp1: List[Puzzle],
               path: Queue) -> Optional[List[Puzzle]]:
    """This is a helper function for Bfs Solver"""
    if not temp_extension.fail_fast():
        temp2 = temp1.copy()
        temp2.append(temp_extension)
        if temp_extension.is_solved():
            return temp2
        else:
            path.enqueue(temp2)
    return None


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
