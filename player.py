import random

class Board:
    tubes = [
        ['G', 'G'],
        ['R', 'R'],
        ['P', 'P']
    ]
    goal_state = []
    def __init__(self, tubes=None, goal_state=None):
        if tubes is not None:
            self.tubes = tubes
        if goal_state is not None:
            self.goal_state = goal_state
        else:
            self.generate_goal_state()

    @staticmethod
    def display_tubes(tubes_inst=None):
        """ print tubes in linear format """
        if tubes_inst is None:
            tubes_inst = Board.tubes
        for balls in tubes_inst:
            print '| ' + ' '.join(balls)
        print '--------'

    def generate_goal_state(self, max_height=6, tubes_inst=None):
        """ generates a goal state """
        if len(self.goal_state) < 1:
            self.goal_state = [
                [], [], []
            ]
        if tubes_inst is None:
            tubes_inst = self.tubes
        for balls in tubes_inst:
            for ball in balls:
                for i in range(0, 100):
                    selected_tube = random.randint(0, 2)
                    if len(self.goal_state[selected_tube]) < max_height:
                        self.goal_state[selected_tube].append(ball)
                        break
                    if i == 99:
                        self.goal_state[0].append(ball)

test_board = Board(
    goal_state=[
        ['G'],
        ['R', 'P'],
        ['P', 'R', 'G']
    ]
)

print
print '=== tubes ==='
test_board.display_tubes()
print
print '=== goal state ==='
test_board.display_tubes(test_board.goal_state)
