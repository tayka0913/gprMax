# Copyright (C) 2015-2019: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.
from gprMax.updates import CPUUpdates
from gprMax.updates import SubGridsUpdates
from gprMax.updates import GPUUpdates
from gprMax.utilities import timer


def create_solver(sim_config):
    """Returns the configured solver."""
    if sim_config.cpu:
        from gprMax.Grid import FDTDGrid
        G = FDTDGrid()
        updates = CPUUpdates(G)

    elif sim_config.gpu:
        from gprMax.Grid import GPUGrid
        G = GPUGrid()
        updates = GPUUpdates(G)
    else:
        raise NotImplementedError

    solver = Solver(updates, iterator)

    return solver


class Solver:

    """Generic solver for Update objects"""

    def __init__(self, updates, iterator):
        """Context for the model to run in. Sub-class this with contexts
        i.e. an MPI context.

        Args:
            updates (Updates): updates contains methods to run FDTD algorithm
            iterator (iterator): can be range() or tqdm()
        """
        self.updates = updates
        self.iterator = iterator

    def solve(self):
        """Time step the FDTD model."""
        tsolvestart = timer()

        for iteration in self.iterator:

            self.updates.store_outputs(iteration)
            self.updates.store_snapshots(iteration)
            self.updates.update_magnetic()
            self.updates.update_magnetic_pml()
            self.updates.update_magnetic_sources(iteration)
            self.updates.update_electric_a()
            self.updates.update_electric_pml()
            self.updates.update_electric_sources(iteration)
            self.updates.update_electric_b()

        tsolve = timer() - tsolvestart
        return tsolve
