import search
import copy

""" state = (N, M, antennas, forbidden, covered)
M,N
antennas = ((type, (x,y)), ...)
forbidden = ((x,y), ...)
covered = ((x,y), ...)
"""

""" Problem:
A : maximum number of antennas
P : maximum allowed power
"""

class state():
    """This class represents a state for the city class problem"""
    def __init__(self, N, M, A, P, forbidden=[]):
        self.N = N
        self.M = M
        self.A = A  # Maximum number of allowed antennas
        self.P = P  # Maximum allowed power
        self.forbidden = forbidden
        self.antennas = []
        self.covered = [[0]*M for i in range(N)]

    def legal_position(self, pos):
        return pos not in self.forbidden

    def total_power(self):
        return sum([a[0] for a in self.antennas])

    def cover_squares(self, antenna, increment=1):
        for x in range(max(0, antenna[1][0] - antenna[0] +1), min(self.N, antenna[1][0] + antenna[0])):
            for y in range(max(0, antenna[1][1] - antenna[0] +1), min(self.M, antenna[1][1] + antenna[0])):
                self.covered[x][y] += increment

    def num_covered(self):
        return sum([1 if self.covered[x][y] >= 1 else 0 for x in range(self.N) for y in range(self.M)])

    def num_over_covered(self):
        return sum([self.covered[x][y]-1 for x in range(self.N) for y in range(self.M) if self.covered[x][y]>1])

    def add_antenna(self, antenna, index=0):
        if not self.legal_position(antenna[1]) or len(self.antennas) >= self.A or self.total_power()+antenna[0] > self.P\
                or antenna[1][0] < 0 or antenna[1][0] >= self.N or antenna[1][1] < 0 or antenna[1][1] >= self.M:
            return False
        self.antennas.insert(index,antenna)
        self.cover_squares(antenna)
        return True

    def remove_antenna(self, index):
        self.cover_squares(self.antennas[index],-1)
        return self.antennas.pop(index)

    def move_antenna(self, index, x, y):
        antenna = self.remove_antenna(index)
        return self.add_antenna((antenna[0], (x,y)), index)

    def change_antenna_power(self, index, power):
        antenna = self.remove_antenna(index)
        return self.add_antenna((power, antenna[1]), index)

    def print_state(self):
        for s in self.covered:
            print(s)



class city_antenna(search.Problem):

    """
    Solves the city antenna problem. Assignment 2. Tècniques intel·ligència artificial 2018
    """

    def __init__(self, initial):

        search.Problem.__init__(self, initial)

    def actions(self, state):
        """
        Given a state returns all legal actions
        """
        """Add antenna"""
        if len(state.antennas) < state.A and state.total_power() < state.P:
            max_power = min(4, max(0, state.P-state.total_power())) + 1
            add = ['add_antenna(({0},({1},{2})))'.format(p,x,y) for p in range(1,max_power) for x in range(state.N) for y in range(state.M)
                   if (x,y) not in state.forbidden and state.covered[x][y] == 0]
        else:
            add=[]

        """Move an antenna"""
        move = ['move_antenna({0},{1},{2})'.format(i, x, y) for i in range(len(state.antennas)) for x in range(state.N) for y in range(state.M)
                if (x,y) not in state.forbidden and (x,y) != state.antennas[i][1]]

        """Change antenna power"""
        power = ['change_antenna_power({0},{1})'.format(i, p) for i in range(len(state.antennas)) for p in range(1,5) if p != state.antennas[i][0]]

        return add + move + power

    def result(self, state, action):
        """
        Call the function
        """
        new_state = copy.deepcopy(state)
        if eval('new_state.'+action):
            return new_state
        else:
            return False

    def value(self, state):
        mcovered = state.num_covered()  # /(state.N*state.M)
        over_covered = state.num_over_covered()/state.num_covered() if state.num_covered() > 0 else 0
        antennas_used = len(state.antennas)/state.A
        power_used = state.total_power()/state.P
        return mcovered - over_covered - antennas_used - power_used


initial = state(2, 8, 120, 120)
problem = city_antenna(initial)

print("Initial sate")
print(initial.forbidden)
problem.initial.print_state()
sol=search.hill_climbing(problem)

print("")
print("Final sate")
sol.state.print_state()
print(sol.state.antennas)
print(sol.solution())


"""
a = state(9, 9, 12, 12, ())
print(a.add_antenna((2, (8,8))))
print(a.add_antenna((2, (0,0))))
print('Num antennas: ', len(a.antennas))
print('Antennas: ', a.antennas)
print('Covered squares: ', a.num_covered())
print('Total power: ', a.total_power())
print(a.forbidden)
a.print_state()

problem = city_antenna(a)
print("Value: ", problem.value(a))


problem = city_antenna(a)
print(problem.actions(a))
print("new state: ")
problem.result(a,problem.actions(a)[0]).print_state()

print("")
print("old sate")
a.print_state()
"""


"""
print(a.move_antenna(0,0,0))
print('Covered squares: ', a.num_covered())
print(a.covered)

print(a.remove_antenna(0))
print(a.remove_antenna(0))
print(a.covered)
"""


