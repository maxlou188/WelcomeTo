import json
from street import Street

class PlayerState:
    def __init__(self, player_state):
        self.agents = player_state["agents"]
        self.city_plan_score = player_state["city-plan-score"]
        self.refusals = player_state["refusals"]
        self.streets = player_state["streets"]
        self.temps = player_state["temps"]

        self.validate(player_state)

    def __str__(self):
        return json.dumps(self.to_dict())

    @property
    def agents(self):
        return self._agents

    @property
    def city_plan_score(self):
        return self._city_plan_score

    @property
    def refusals(self):
        return self._refusals

    @property
    def streets(self):
        return self._streets
    
    @property
    def temps(self):
        return self._temps

    @agents.setter
    def agents(self, agents: list):
        """
            -> list
        """
        assert len(agents) == 6 and type(agents) == list
        assert 0 <= agents[0] <= 1 and type(agents[0]) == int
        assert 0 <= agents[1] <= 2 and type(agents[1]) == int
        assert 0 <= agents[2] <= 3 and type(agents[2]) == int
        assert 0 <= agents[3] <= 4 and type(agents[3]) == int
        assert 0 <= agents[4] <= 4 and type(agents[4]) == int
        assert 0 <= agents[5] <= 4 and type(agents[5]) == int
        
        self._agents = agents

    @city_plan_score.setter
    def city_plan_score(self, city_plan_score: list):
        """
            -> lista
        """
        assert len(city_plan_score) == 3 and type(city_plan_score) == list
        assert city_plan_score[0] == "blank" or (0 <= city_plan_score[0] and type(city_plan_score[0]) == int)
        assert city_plan_score[1] == "blank" or (0 <= city_plan_score[1] and type(city_plan_score[1]) == int)
        assert city_plan_score[2] == "blank" or (0 <= city_plan_score[2] and type(city_plan_score[2]) == int)

        self._city_plan_score = city_plan_score

    @refusals.setter
    def refusals(self, refusals: int):
        """
            -> int
        """
        assert 0 <= refusals <= 3 and type(refusals) == int

        self._refusals = refusals

    @streets.setter
    def streets(self, streets: list):
        """
            Formats streets such that every element is
            of type class Street
            -> list[Street]
        """
        assert len(streets) == 3
        self._streets = [Street(streets[0], [2, 6, 7], 3), Street(streets[1], [0, 3, 7], 4), Street(streets[2], [1, 6, 10], 5)]
        assert len(self.streets[0].roundabout + self.streets[1].roundabout + self.streets[2].roundabout) <= 2

    @temps.setter
    def temps(self, temps: int):
        """
            -> int
        """
        assert 0 <= temps <= 11

        self._temps = temps

    def validate(self, player_state):
        """
            player_state: PlayerState -> bool
        """
        assert len(player_state) == 5

        assert len(self.streets[0].homes) == 10
        assert len(self.streets[1].homes) == 11
        assert len(self.streets[2].homes) == 12
        
    def to_dict(self):
        """
            -> dict
        """
        player_state = {}
        player_state["agents"] = self.agents
        player_state["city-plan-score"] = self.city_plan_score
        player_state["refusals"] = self.refusals
        player_state["streets"] = []
        player_state["temps"] = self.temps

        for street in self.streets:
            street_dict = {}
            street_dict["homes"] = []
            street_dict["parks"] = street.parks
            street_dict["pools"] = street.pools

            for i, home in enumerate(street.homes):
                val = [home.val, "bis"] if home.bis else home.val
                if i == 0:
                    street_dict["homes"].append(val)
                    street_dict["homes"].append(home.used_in_plan)
                else:
                    street_dict["homes"].append([home.left_fence, val, home.used_in_plan])

            player_state["streets"].append(street_dict)

        return player_state

    def _check_agents(self, new_player_state, effect_used):
        """

        Args:
            new_player_state (PlayerState)
            effect_used (bool or str)

        Returns:
            str or bool
        """
        if self.agents != new_player_state.agents:
            for i in range(len(self.agents)):
                if self.agents[i] != new_player_state.agents[i]:
                    assert not effect_used and new_player_state.agents[i] - self.agents[i] == 1
                    effect_used = "agent"
        return effect_used

    def _check_city_plans_scored(self, new_player_state, city_plans_scored):
        """

        Args:
            new_player_state (PlayerState)
            city_plans_scored (list[Tuple])

        Returns:
            list[Tuple]
        """
        if self.city_plan_score != new_player_state.city_plan_score:
            # city_plan_number[(score_position, score_number)]
            for i in range(len(self.city_plan_score)):
                if self.city_plan_score[i] != new_player_state.city_plan_score[i]:
                    assert type(new_player_state.city_plan_score[i]) == int and self.city_plan_score[i] == "blank"
                    city_plans_scored.append((i, new_player_state.city_plan_score[i])) # (position, score)
        return city_plans_scored

    def _check_houses(self, new_player_state, new_in_plan, house_played, effect_used):
        """

        Args:
            new_player_state (PlayerState)
            new_in_plan (bool)
            house_played (bool)
            effect_used (bool or str)

        Returns:
            (Tuple(int or bool, bool, str or bool))
        """
        new_house_location = (-1, -1)
        roundabout_location = None

        for i in range(len(self.streets)):
            for j in range(len(self.streets[i].homes)):
                old_home = self.streets[i].homes[j]
                new_home = new_player_state.streets[i].homes[j]
                
                if old_home.val != new_home.val:
                    assert old_home.val == "blank" and (type(new_home.val) == int or new_home.val == "roundabout")
                    if new_home.bis:
                        assert not effect_used
                        effect_used = "bis"
                    else:
                        if type(new_home.val) == int:
                            assert not house_played
                            house_played = new_home.val
                            new_house_location = (i, j)
                        else:
                            if new_home.val == "roundabout":
                                assert not roundabout_location
                                roundabout_location = (i, j)
                if old_home.used_in_plan != new_home.used_in_plan:
                    assert old_home.used_in_plan == False and new_home.used_in_plan == True
                    new_in_plan[i].append(j)

                # Fence changes due to surveyor and not roundabout placing, checking left fence so this works
                if old_home.left_fence != new_home.left_fence and not ((i, j - 1) == roundabout_location or (i, j) == roundabout_location):
                    assert old_home.left_fence == False and new_home.left_fence == True
                    assert not effect_used
                    assert not old_home.used_in_plan
                    effect_used = "surveyor"

            effect_used = self._check_parks(new_player_state, effect_used, new_house_location, i)

            effect_used = self._check_pools(new_player_state, effect_used, new_house_location, i)

        return (house_played, new_in_plan, effect_used)

    def _check_parks(self, new_player_state, effect_used, new_house_location, i):
        """

        Args:
            new_player_state (PlayerState)
            effect_used (bool or str)
            new_house_location (list)
            i (int)

        Returns:
            (bool or str)
        """
        if self.streets[i].parks != new_player_state.streets[i].parks:
                assert not effect_used and new_player_state.streets[i].parks - self.streets[i].parks == 1
                assert i == new_house_location[0]
                effect_used = "landscaper"
        return effect_used

    def _check_pools(self, new_player_state, effect_used, new_house_location, i):
        """

        Args:
            new_player_state (PlayerState)
            effect_used (bool or str)
            new_house_location (list)
            i (int)

        Returns:
            (bool or str)
        """
        if self.streets[i].pools != new_player_state.streets[i].pools:
                for j in range(len(self.streets[i].pools)):
                    if self.streets[i].pools[j] != new_player_state.streets[i].pools[j]:
                        assert not effect_used and self.streets[i].pools[j] == False and new_player_state.streets[i].pools[j] == True
                        possible_locations = {0: {2, 6, 7}, 1: {0, 3, 7}, 2: {1, 6, 10}}
                        assert i == new_house_location[0] and new_house_location[1] in possible_locations[i]
                        effect_used = "pool"
        return effect_used

    def _check_temps(self, new_player_state, effect_used):
        """

        Args:
            new_player_state (PlayerState)
            effect_used (bool or str)

        Returns:
            (bool or str)
        """
        if self.temps != new_player_state.temps:
            assert not effect_used and new_player_state.temps - self.temps == 1
            effect_used = "temp"
        
        return effect_used

    def valid_move(self, new_player_state, game_state):
        """

        Args:
            new_player_state (PlayerState)
            gaem_state (GameState)

        Returns:
            (bool)
        """
        # effect_used: False if no effect played, or the string effect
        effect_used = False

        effect_used = self._check_agents(new_player_state, effect_used)

        city_plans_scored = self._check_city_plans_scored(new_player_state, [])

        # new_in_plan: [[First row house's indices that are now in a plan], [Second row's ...], [Third row's ...]]
        house_played, new_in_plan, effect_used = self._check_houses(new_player_state, [[], [], []], False, effect_used)

        effect_used = self._check_temps(new_player_state, effect_used)

        if effect_used:
            assert effect_used in game_state.effects

        possible_numbers = []

        # Get indices of the same effects used
        indices = [i for i, effect in enumerate(game_state.effects) if effect == effect_used]

        # Didn't use effects, can be everything
        if len(indices) == 0:
            possible_numbers = [game_state.construction_cards[i][0] for i in [0, 1, 2]]

        # Temp, more range of possible
        elif effect_used == "temp":
            for i, effect in enumerate(game_state.effects):
                if effect == "temp":
                    temp_number = game_state.construction_cards[i][0]
                    possible_numbers.extend([temp_number - 2, temp_number - 1, temp_number, temp_number + 1, temp_number + 2])
        # Effects we played and their corresponding numbers on construction cards
        
        else:
            possible_numbers = [game_state.construction_cards[i][0] for i in indices]
        if self.refusals != new_player_state.refusals:
            assert not effect_used and new_player_state.refusals - self.refusals == 1
            assert type(house_played) == bool and house_played == False
            for street in self.streets:
                left_number = -1
                right_number = -1
                for i, home in enumerate(street.homes):
                    if home.val == "blank":
                        j = i
                        while j < len(street.homes):
                            if type(street.homes[j].val) == int:
                                right_number = street.homes[j].val
                                break
                            j += 1
                        
                        for number in possible_numbers:
                            assert not (number > left_number and (number < right_number or j == len(street.homes)))
                    elif type(home.val) == int:
                        left_number = home.val
            # If we get here it was a correct refusal
        else:
            assert type(house_played) == int and house_played in possible_numbers

        required_city_plans, regular_criteria = [], []
        for index, score in city_plans_scored:
            required_city_plans.append((game_state.city_plans[index], score))
        
        for city_plan, score in required_city_plans:
            required_criteria = city_plan.criteria
            correct_score = city_plan.score2 if game_state.city_plans_won[city_plan.position - 1] else city_plan.score1
            assert score == correct_score
            
            if all(type(elem) == int for elem in required_criteria):
                regular_criteria.extend(required_criteria)
            else:
                if required_criteria == [ "all houses", 0 ]:
                    assert len(new_in_plan[0]) == len(self.streets[0].homes)
                    new_in_plan[0].clear()

                elif required_criteria == [ "all houses", 2 ]:
                    assert len(new_in_plan[2]) == len(self.streets[2].homes)
                    new_in_plan[2].clear()

                elif required_criteria ==  "end houses":
                    assert new_in_plan[0][0] == 0 and new_in_plan[0][-1] == len(self.streets[0].homes) - 1
                    assert new_in_plan[1][0] == 0 and new_in_plan[1][-1] == len(self.streets[1].homes) - 1
                    assert new_in_plan[2][0] == 0 and new_in_plan[2][-1] == len(self.streets[2].homes) - 1
                    for i in range(len(new_in_plan)):
                        new_in_plan[i].pop(0)
                        new_in_plan[i].pop(-1)

                elif required_criteria == "7 temps":
                    assert new_player_state.temps >= 7
                    
                elif required_criteria == "5 bis":
                    max_bis_count = 0
                    for street in new_player_state.streets:
                        current_bis_count = 0
                        for house in street.homes:
                            if house.bis:
                                current_bis_count += 1
                                max_bis_count = max(max_bis_count, current_bis_count)

                    assert max_bis_count >= 5

                elif required_criteria == "two streets all parks":
                    assert (new_player_state.streets[0].parks == 3) + (new_player_state.streets[1].parks == 4) + (new_player_state.streets[2].parks == 5) >= 2

                elif required_criteria == "two streets all pools":
                    assert all(pool == True for pool in new_player_state.streets[0].pools) + all(pool == True for pool in new_player_state.streets[1].pools) + all(pool == True for pool in new_player_state.streets[2].pools) >= 2

                elif required_criteria == [ "all pools all parks", 1 ]:
                    assert new_player_state.streets[1].parks == 4 and all(pool == True for pool in new_player_state.streets[1].pools)

                elif required_criteria ==  [ "all pools all parks", 2 ]:
                    assert new_player_state.streets[2].parks == 5 and all(pool == True for pool in new_player_state.streets[2].pools)

                elif required_criteria == "all pools all parks one roundabout":
                    assert (new_player_state.streets[0].parks == 3 and all(pool == True for pool in new_player_state.streets[0].pools) and new_player_state.streets[0].roundabout) or \
                            (new_player_state.streets[1].parks == 4 and all(pool == True for pool in new_player_state.streets[1].pools) and new_player_state.streets[1].roundabout) or \
                            (new_player_state.streets[2].parks == 5 and all(pool == True for pool in new_player_state.streets[2].pools) and new_player_state.streets[2].roundabout)

        all_estate_sizes = []
        for i, row in enumerate(new_in_plan):
            size = 0
            for house_index in row:
                house = new_player_state.streets[i].homes[house_index]
                size += 1
                if house.left_fence:
                    size = 1
                if house.right_fence:
                    all_estate_sizes.append(size)
                if size == 1 and not house.left_fence:
                    raise Exception("invalid city-plan-score")
        
        assert sorted(all_estate_sizes) == sorted(regular_criteria)

        return new_player_state


    

    def score(self, temp_list: list):
        """
            -> int
        """
        score = 0
        
        score += self.city_plan_score_points()
        score -= self.refusal_points()
        score += self.street_points()
        score -= self.roundabout_points()

        score += self.temp_points(temp_list)

        return score

    def city_plan_score_points(self):
        """
            -> int
        """
        score = 0
        for points in self.city_plan_score:
            if type(points) == int:
                score += points
        return score

    def refusal_points(self):
        """
            -> int
        """
        if self.refusals == 2:
            return 3
        elif self.refusals > 2:
            return 5
        return 0

    def street_points(self):
        """
            -> int
        """
        score = 0
        estates = [0, 0, 0, 0, 0, 0, 0]
        pools = [0, 3, 6, 9, 13, 17, 21, 26, 31, 36]
        parks = [
            [0, 2, 4, 10],
            [0, 2, 4, 6, 14],
            [0, 2, 4, 6, 8, 18]
        ]
        bis = [0, 1, 3, 6, 9, 12, 16, 20, 24, 28]
        pools_count, pool_points = 0, 0
        park_points = 0
        bis_count = 0

        for i, street in enumerate(self.streets):
            current_estate = 0
            valid_estate = True
            for home in street.homes:
                if type(home.val) == int:
                    if home.left_fence:
                        valid_estate = True
                        current_estate = 1
                    if home.right_fence:
                        if current_estate >= 1 and current_estate <= 6 and valid_estate:
                            estates[current_estate] += 1
                        valid_estate = False
                    if valid_estate:
                        current_estate += 1
                    if home.bis:
                        bis_count += 1
                else:
                    valid_estate = False
            for pool in street.pools:
                if pool:
                    pools_count += 1

            park_points += parks[i][street.parks]

        pool_points += pools[pools_count]
        estates.pop(0)
        score += self.estate_points(estates) + park_points + pool_points - bis[bis_count]
        return score

    def roundabout_points(self):
        """
            -> int
        """
        roundabout_points = [0, 3, 8]
        roundabout_count = len(self.streets[0].roundabout + self.streets[1].roundabout + self.streets[2].roundabout)
        return roundabout_points[roundabout_count]

    def estate_points(self, estates):
        """
            -> int
        """
        score = 0
        estate_size_points = [
            [1, 3],
            [2, 3, 4],
            [3, 4, 5, 6],
            [4, 5, 6, 7, 8],
            [5, 6, 7, 8, 10],
            [6, 7, 8, 10 ,12]
        ]
        for i, points in enumerate(estate_size_points):
            score += points[self.agents[i]] * estates[i]
        return score

    def temp_points(self, playerTemps: list):
        """
            -> int
        """
        points = 0
        playerTemps.append(self.temps)
        playerTemps = sorted(set(playerTemps))
        playerSize = len(playerTemps)
        place = -1
        
        if playerSize == 0 or self.temps == 0:
            return 0
        elif self.temps > playerTemps[-1]:
            place = 1
        elif self.temps < playerTemps[0]:
            place = playerSize + 1
        else:
            place = playerSize - playerTemps.index(self.temps)
        
        if place == 1:
            points += 7
        elif place == 2:
            points += 4
        elif place == 3:
            points += 1

        return points

    def game_over(self):
        """
            -> bool
        """
        return self._all_street_full() or self._three_refusal() or self._city_plan_completed()
    
    def _all_street_full(self):
        """
            -> bool
        """
        for street in self.streets:
            for home in street.homes:
                if home.val == "blank":
                    return False

        return True

    def _three_refusal(self):
        """
            -> bool
        """
        return self.refusals >= 3

    def _city_plan_completed(self):
        """
            -> bool
        """
        return type(self.city_plan_score[0]) == int and type(self.city_plan_score[1]) == int and type(self.city_plan_score[2]) == int









    
