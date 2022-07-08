def number_or_refusal(streets, possible_numbers):
    for i, street in enumerate(streets):
        prev = -1
        for j, home in enumerate(street):
            if home == "blank":
                next, k = home, j + 1
                while type(next) is str and k < len(street):
                    next = street[k] # [1, 2, b, b, b]
                    k += 1
                for number in possible_numbers:
                    if (prev < number and next == "blank") or (prev < number and number < next):
                        return [number, i, j]
            else:
                if type(home) is int:
                    prev = home
    return -1

def increase_refusal(player_state):
    player_state["refusals"] += 1
    return player_state

def put_house(player_state, house_location):
    streets = player_state["streets"]
    house_number, street_number, house_index = house_location[0], house_location[1], house_location[2]

    if house_index:
        streets[street_number]["homes"][house_index + 1][1] = house_number
    else:
        streets[street_number]["homes"][house_index] = house_number

    player_state["streets"] = streets
    return player_state