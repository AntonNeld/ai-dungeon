class PickUpSystem:

    def pick_up_items(self, pickupper_components, actions, position_components,
                      pickup_components, score_components):
        picked_up_items = {}
        removed_entities = set()
        for pickupper_id, pickupper in pickupper_components.items():
            if pickupper_id not in position_components:
                continue
            if (pickupper.mode == "action"
                    and (pickupper_id not in actions
                         or actions[pickupper_id].action_type != "pick_up")):
                continue

            x = position_components[pickupper_id].x
            y = position_components[pickupper_id].y
            pickups = [e for e in position_components.get_entities_at(x, y)
                       if e in pickup_components]
            for pickup_id in pickups:
                kind = pickup_components[pickup_id].kind
                if (
                    kind == "item" and not
                    pickupper.full_inventory()
                ):
                    picked_up_items[pickup_id] = pickupper_id
                elif kind == "vanish":
                    removed_entities.add(pickup_id)
                elif kind == "addScore":
                    removed_entities.add(pickup_id)
                    added_score = pickup_components[pickup_id].score
                    if pickupper_id in score_components:
                        score_components[pickupper_id] += added_score
        return picked_up_items, removed_entities