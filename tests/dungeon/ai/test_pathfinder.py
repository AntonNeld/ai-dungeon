from test_utils import room_from_text


def test_find_coins_auto_pickup():
    room = room_from_text("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "ai": {"kind": "pathfinder"},
      "pickupper": {},
      "perception": {},
      "actions": {
        "move_right": {},
        "move_left": {},
        "move_up": {},
        "move_down": {}
      }
    },
    "#": {"looksLike": "wall", "blocksMovement": true},
    "c": {"looksLike": "coin", "pickup": {"kind": "item"}}
  }
}

#########
#p#c#  c#
# # # ###
#   # #
###   #
  #####
    """)

    room.step(16)
    assert len(room.get_entities(looks_like="player")
               [0].pickupper.inventory) == 2
    assert room.get_entities(looks_like="coin") == []


def test_find_coins_action_pickup():
    room = room_from_text("""
{
  "definitions": {
    "p": {
      "looksLike": "player",
      "ai": {"kind": "pathfinder", "manualPickup": true},
      "pickupper": {"mode": "action"},
      "perception": {},
      "actions": {
        "move_right": {},
        "move_left": {},
        "move_up": {},
        "move_down": {},
        "pick_up": {}
      }
    },
    "#": {"looksLike": "wall", "blocksMovement": true},
    "c": {"looksLike": "coin", "pickup": {"kind": "item"}}
  }
}

#########
#p#c#  c#
# # # ###
#   # #
###   #
  #####
    """)

    room.step(18)
    assert len(room.get_entities(looks_like="player")
               [0].pickupper.inventory) == 2
    assert room.get_entities(looks_like="coin") == []
