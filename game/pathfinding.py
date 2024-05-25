import heapq


def a_star_pathfinding(start, goal, grid, cell_size):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start = (start[0] // cell_size, start[1] // cell_size)
    goal = (goal[0] // cell_size, goal[1] // cell_size)

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[0] < len(grid[0]) and 0 <= next_node[1] < len(grid):
                if grid[next_node[1]][next_node[0]] < 3:  # Assuming walls are 3 or greater
                    new_cost = cost_so_far[current] + 1
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(goal, next_node)
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current

    path = []
    if goal in came_from:
        current = goal
        while current:
            path.append((current[0] * cell_size, current[1] * cell_size))
            current = came_from[current]
        path.reverse()

    return path
