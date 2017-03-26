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
            print('| ' + ' '.join(balls))
        print('--------')

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

    def heuristic_calc(self, user_state, goal_state=None):
        if goal_state is None:
            goal_state = list(self.goal_state)
        state = list(user_state)
        goal_state_tube_counts = {}
        score = 0
        index = 0
        for tube in goal_state:
            goal_state_tube_counts[len(tube)] = index
            index += 1
        print("=== testing state:")
        self.display_tubes(state)
        for key in reversed(sorted(goal_state_tube_counts.keys())):
            goal_tube = goal_state[goal_state_tube_counts[key]]
            print("testing goal_tube:" + str(goal_state_tube_counts[key]))
            print(goal_tube)
            best_match_state_tube_index = None
            best_match_state_tube_score = 0
            state_tube_index = 0
            for state_tube in state:
                state_tube_score = 0
                for i in range(0, min(len(state_tube), len(goal_tube))):
                    if state_tube[i] == goal_tube[i]:
                        state_tube_score += 1
                    else:
                        break
                if state_tube_score > best_match_state_tube_score:
                    best_match_state_tube_index = state_tube_index
                    best_match_state_tube_score = state_tube_score
                state_tube_index += 1
            if best_match_state_tube_index is not None:
                del state[best_match_state_tube_index]
                score += best_match_state_tube_score
        print("score= " + str(score))
        return 6 - score


board = Board(
    goal_state=[
        ['G'],
        ['R', 'G'],
        ['P', 'P', 'R']
    ]
)

print()
print('=== tubes ===')
board.display_tubes()
print()
print('=== goal state ===')
board.display_tubes(board.goal_state)
board.heuristic_calc([
    ['R', 'P'],
    ['P', 'R', 'G'],
    ['G']
])
