import random
import copy


TUBES_COUNT = 3
BALLS_COUNT = 6


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

    def generate_goal_state(self, max_height=BALLS_COUNT, tubes_inst=None):
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
                    selected_tube = random.randint(0, TUBES_COUNT-1)
                    if len(self.goal_state[selected_tube]) < max_height:
                        self.goal_state[selected_tube].append(ball)
                        break
                    if i == 99:
                        self.goal_state[0].append(ball)

    def heuristic_calc(self, user_state, goal_state=None):
        if goal_state is None:
            goal_state = copy.deepcopy(self.goal_state)
        state = copy.deepcopy(user_state)
        goal_state_tube_counts = {}
        score = 0
        index = 0
        for tube in goal_state:
            goal_state_tube_counts[len(tube)] = index
            index += 1
        # print("=== testing state:")
        # self.display_tubes(state)
        for key in reversed(sorted(goal_state_tube_counts.keys())):
            goal_tube = goal_state[goal_state_tube_counts[key]]
            # print("testing goal_tube:" + str(goal_state_tube_counts[key]))
            # print(goal_tube)
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
        # print("score= " + str(score))
        return BALLS_COUNT - score

    @staticmethod
    def move_ball(state, source, destination, count=1):
        tubes = copy.deepcopy(state)  # clone
        moved_balls = 0
        for i in range(0, max(1, count)):
            if len(tubes[source]) > 0:
                ball = tubes[source].pop()
                tubes[destination].append(ball)
                moved_balls += 1
            else:
                break
        return tubes, moved_balls

    def find_moves(self, tubes, current_cost=0):
        moves_list = []
        for tube_index in range(len(tubes)):
            for i in range(1, TUBES_COUNT):
                new_state, moved_balls = Board.move_ball(tubes, tube_index, (tube_index + i) % TUBES_COUNT)
                if moved_balls > 0:
                    predicted_cost = current_cost + self.heuristic_calc(new_state)
                    moves_list.append({
                        'cost': predicted_cost,
                        'state': new_state
                    })
        return moves_list


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
# moved_board, moved_balls = board.move_ball([
#     ['R', 'P'],
#     ['P', 'R', 'G'],
#     ['G']
# ], 0, 1)
# print("test move results:")
# board.display_tubes(moved_board)
available_states = board.find_moves([
    ['R', 'P'],
    ['P', 'R', 'G'],
    ['G']
])
for predicted_state in available_states:
    print("=== available move cost:" + str(predicted_state['cost']))
    board.display_tubes(predicted_state['state'])
