import sys
import json
from move import number_or_refusal, increase_refusal, put_house

def possible_move(totalContent):
    totalContent = json.loads(totalContent)
    if "game-over" in totalContent:
        return "ack"
    
    game_state = totalContent["game-state"]
    player_state = totalContent["player-state"]

    construction_cards = game_state["construction-cards"]
    possible_numbers = [ i[0] for i in construction_cards]
    
    streets = player_state["streets"]

    street_home_info = [street["homes"] for street in streets]
    street_house_numbers = list()

    for street in street_home_info:
        house_numbers = list()
        house_numbers.append(get_house_number(street[0])) # getting first house number

        for i in range(2, len(street)):
            house_numbers.append(get_house_number(street[i][1]))
        
        street_house_numbers.append(house_numbers)

    new_house = number_or_refusal(street_house_numbers, possible_numbers)
    
    if new_house == -1:
        return increase_refusal(player_state)
    else:
        return put_house(player_state, new_house)
    
    


def get_house_number(house):
    return house if not isinstance(house, list) else house[0]

def main():
    totalContent = sys.stdin.read()
    totalContent = json.loads(totalContent)
    total_content_dict = {"game-state": totalContent[0], "player-state": totalContent[1]}
    print(json.dumps(possible_move(json.dumps(total_content_dict))))

# if __name__ == "__main__":
#     totalContent = sys.stdin.read()
#     print(json.dumps(possible_move(totalContent)))