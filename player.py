import random
import copy


BALLS_COUNT = 6
TUBE_LABELS = ['A', 'B', 'C']
TUBES_COUNT = len(TUBE_LABELS)
MAX_TREE_HEIGHT = 20


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
    def display_tubes(tubes_inst=None, with_labels=False):
        """ print tubes in linear format """
        if tubes_inst is None:
            tubes_inst = Board.tubes
        index = 0
        for balls in tubes_inst:
            if with_labels:
                label = TUBE_LABELS[index]
            else:
                label = ''
            print(label + '| ' + ' '.join(balls))
            index += 1
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
            goal_state_tube_counts[len(tube) + (index / len(goal_state))] = index
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

    @staticmethod
    def sort_moves(moves_list, real_cost_preferred=True):
        sorted_moves_list = []
        cost_per_list_index = {}
        for i in range(len(moves_list)):
            if real_cost_preferred and moves_list[i]['real_cost'] is not None:
                move_cost = moves_list[i]['real_cost']
            else:
                move_cost = moves_list[i]['cost']
            adapted_cost = move_cost + (i / len(moves_list))
            cost_per_list_index[adapted_cost] = i
        for key in sorted(cost_per_list_index.keys()):
            move = moves_list[cost_per_list_index[key]]
            sorted_moves_list.append(move)
        return sorted_moves_list

    def find_moves(self, tubes, current_cost=0):
        moves_list = []
        for tube_index in range(len(tubes)):
            for i in range(1, TUBES_COUNT):
                tube_dest = (tube_index + i) % TUBES_COUNT

                if len(tubes[tube_index]) + len(tubes[tube_dest]) > 1:
                    new_state, moved_balls = Board.move_ball(tubes, tube_index, tube_dest)
                    if moved_balls > 0:
                        heuristic_val = self.heuristic_calc(new_state)
                        predicted_cost = current_cost + heuristic_val
                        moves_list.append({
                            'cost': predicted_cost,
                            'state': new_state,
                            'move': {
                                'source': tube_index,
                                'destination': tube_dest,
                                'str': TUBE_LABELS[tube_index] + ' ~> ' + TUBE_LABELS[tube_dest]
                            },
                            'real_cost': None,
                            'h': heuristic_val
                        })
        return moves_list

    def find_path(self, current_state=None, current_cost=1):
        if current_cost > MAX_TREE_HEIGHT:
            return [], current_cost + 1
        if current_state is None:
            current_state = copy.deepcopy(self.tubes)
        available_moves_raw = self.find_moves(current_state, current_cost)
        available_moves = self.sort_moves(available_moves_raw)
        best_path = []
        best_cost_found = None

        for i in range(len(available_moves)):
            next_move = available_moves[0]

            if next_move['h'] == 0:
                return [next_move['move']], current_cost + 1

            if next_move['real_cost'] is None:
                path, real_cost = self.find_path(next_move['state'], current_cost + 1)
                if best_cost_found is None or real_cost < best_cost_found:
                    best_cost_found = real_cost
                    best_path = path
                next_move['real_cost'] = real_cost
                available_moves = self.sort_moves(available_moves)
            else:
                # shortest path is already entered ~> it is best path
                best_path.insert(0, next_move['move'])
                return best_path, next_move['real_cost']

        return [], current_cost + 1


board = Board(
    # goal_state=[
    #     ['G'],
    #     ['R', 'G'],
    #     ['P', 'P', 'R']
    # ]
    goal_state=[
        [],
        ['R', 'G'],
        ['P', 'G', 'P', 'R']
    ]
)

print()
print('=== tubes ===')
board.display_tubes(board.tubes, True)
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
# available_states = board.find_moves([
#     ['R', 'P'],
#     ['P', 'R', 'G'],
#     ['G']
# ])
# for predicted_state in available_states:
#     print("=== available move:'" + predicted_state['move']['str'] + "'  cost:" + str(predicted_state['cost']))
#     board.display_tubes(predicted_state['state'])
# moves, cost = board.find_path()
# print("path found with cost=" + str(cost))
# for move in moves:
#     print(move['str'])

print("-- end --")
