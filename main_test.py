from main import Action, Battle, Fighter


run_cases = [
    {
        "name": "one_turn_status",
        "kind": "status",
        "turns": [
            ("Iris", ("Guard Strike", 2, 3, 2)),
        ],
        "expected": {
            "finished": False,
            "winner": None,
            "current_turn": "Moro",
            "turns": 1,
            "left": {"name": "Iris", "health": 12, "energy": 1, "shield": 2},
            "right": {"name": "Moro", "health": 7, "energy": 3, "shield": 0},
        },
    },
    {
        "name": "two_turn_status",
        "kind": "status",
        "turns": [
            ("Iris", ("Guard Strike", 2, 3, 2)),
            ("Moro", ("Jab", 1, 2, 0)),
        ],
        "expected": {
            "finished": False,
            "winner": None,
            "current_turn": "Iris",
            "turns": 2,
            "left": {"name": "Iris", "health": 12, "energy": 2, "shield": 0},
            "right": {"name": "Moro", "health": 7, "energy": 3, "shield": 0},
        },
    },
    {
        "name": "short_battle_winner",
        "kind": "status",
        "fighters": (("Nia", 5, 2), ("Rex", 3, 0)),
        "turns": [
            ("Nia", ("Slash", 2, 3, 0)),
        ],
        "expected": {
            "finished": True,
            "winner": "Nia",
            "current_turn": None,
            "turns": 1,
            "left": {"name": "Nia", "health": 5, "energy": 1, "shield": 0},
            "right": {"name": "Rex", "health": 0, "energy": 1, "shield": 0},
        },
    },
]

submit_cases = run_cases + [
    {
        "name": "invalid_action_validation",
        "kind": "error",
        "action": ("", 1, 0, 0),
        "expected": "action name must not be empty",
    },
    {
        "name": "not_enough_energy",
        "kind": "error",
        "fighters": (("Ava", 5, 0), ("Bolt", 5, 0)),
        "turns": [
            ("Ava", ("Burst", 1, 2, 0)),
        ],
        "expected": "Ava does not have enough energy for Burst",
    },
    {
        "name": "full_report",
        "kind": "report",
        "turns": [
            ("Iris", ("Guard Strike", 2, 3, 2)),
            ("Moro", ("Jab", 1, 2, 0)),
            ("Iris", ("Guard Strike", 2, 3, 2)),
            ("Moro", ("Heavy Blow", 3, 6, 0)),
            ("Iris", ("Guard Strike", 2, 3, 2)),
            ("Moro", ("Heavy Blow", 3, 6, 0)),
            ("Iris", ("Jab", 1, 2, 0)),
        ],
        "expected": "Winner: Iris\nTurns: 7\nNext turn: none\nIris - HP: 4, Energy: 2, Shield: 0\nMoro - HP: 0, Energy: 2, Shield: 0\nHistory:\n1. Iris used Guard Strike on Moro: +2 shield, 3 damage, 3 dealt\n2. Moro used Jab on Iris: +0 shield, 2 damage, 0 dealt\n3. Iris used Guard Strike on Moro: +2 shield, 3 damage, 3 dealt\n4. Moro used Heavy Blow on Iris: +0 shield, 6 damage, 4 dealt\n5. Iris used Guard Strike on Moro: +2 shield, 3 damage, 3 dealt\n6. Moro used Heavy Blow on Iris: +0 shield, 6 damage, 4 dealt\n7. Iris used Jab on Moro: +0 shield, 2 damage, 2 dealt",
    },
]


def build_battle(case):
    fighter_data = case.get("fighters")
    if fighter_data is None:
        fighter_data = (("Iris", 12, 2), ("Moro", 10, 2))

    left_data, right_data = fighter_data
    left = Fighter(*left_data)
    right = Fighter(*right_data)
    return Battle(left, right)


def play_turns(battle, turns):
    for actor_name, action_data in turns:
        action = Action(*action_data)
        battle.take_turn(actor_name, action)


def print_case_input(case):
    fighter_data = case.get("fighters")
    if fighter_data is None:
        fighter_data = (("Iris", 12, 2), ("Moro", 10, 2))

    print("Fighters:")
    print(
        f"  Left:  {fighter_data[0][0]} (HP: {fighter_data[0][1]}, Energy: {fighter_data[0][2]})"
    )
    print(
        f"  Right: {fighter_data[1][0]} (HP: {fighter_data[1][1]}, Energy: {fighter_data[1][2]})"
    )

    if "turns" in case:
        print("Turns:")
        count = 1
        for actor_name, action_data in case["turns"]:
            print(
                f"  {count}. {actor_name} -> {action_data[0]} (Cost: {action_data[1]}, Damage: {action_data[2]}, Shield: {action_data[3]})"
            )
            count += 1

    if "action" in case:
        action_data = case["action"]
        print("Action:")
        print(
            f"  {action_data[0]!r} (Cost: {action_data[1]}, Damage: {action_data[2]}, Shield: {action_data[3]})"
        )


def test(case):
    print("---------------------------------")
    print(f"Case: {case['name']}")
    print_case_input(case)
    print("")

    try:
        if case["kind"] == "error":
            if "action" in case:
                try:
                    Action(*case["action"])
                    actual = None
                except Exception as e:
                    actual = str(e)
            else:
                battle = build_battle(case)
                try:
                    play_turns(battle, case["turns"])
                    actual = None
                except Exception as e:
                    actual = str(e)
            print(f"Expected error: {case['expected']}")
            print(f"Actual error:   {actual}")
            return actual == case["expected"]

        battle = build_battle(case)
        play_turns(battle, case["turns"])

        if case["kind"] == "status":
            actual = battle.get_status()
        else:
            actual = battle.get_report()

        print("Expected:")
        print(case["expected"])
        print("")
        print("Actual:")
        print(actual)
        return actual == case["expected"]
    except Exception as e:
        print(f"Error: {e}")
        return False



def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)

    for test_case in test_cases:
        correct = test(test_case)
        if correct:
            passed += 1
            print("Pass")
        else:
            failed += 1
            print("Fail")

    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")



test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()

