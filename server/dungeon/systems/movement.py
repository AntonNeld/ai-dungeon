from dungeon.consts import Position


class MovementSystem:

    def move_entities(self, actions, position_components,
                      blocks_movement_components, tags_components):
        for mover_id, action in actions.items():
            if action.action_type != "move":
                continue

            dx = dy = 0
            if action.direction == "up":
                dy = 1
            elif action.direction == "down":
                dy = -1
            elif action.direction == "left":
                dx = -1
            elif action.direction == "right":
                dx = 1
            else:
                raise RuntimeError(f"Unknown direction {action.direction}")

            new_x = position_components[mover_id].x + dx
            new_y = position_components[mover_id].y + dy
            colliding_entities = position_components.get_entities_at(
                new_x, new_y)
            if not any(
                map(
                    lambda e: e in blocks_movement_components and not
                    set(blocks_movement_components[e].passable_for_tags)
                    & set(tags_components[mover_id] if mover_id
                          in tags_components else []),
                    colliding_entities)):
                position_components[mover_id] = Position(x=new_x, y=new_y)