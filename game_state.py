from city_plan import CityPlan
import json

class GameState:
    def __init__(self, game_state):
        self.city_plans = game_state["city-plans"]
        self.city_plans_won = game_state["city-plans-won"]
        self.construction_cards = game_state["construction-cards"]
        self.effects = game_state["effects"]

        self.validate(game_state)
    
    def __str__(self):
        return json.dumps(self.to_dict())

    @property
    def city_plans(self):
        return self._city_plans
    
    @property
    def city_plans_won(self):
        return self._city_plans_won

    @property
    def construction_cards(self):
        return self._construction_cards

    @property
    def effects(self):
        return self._effects

    @city_plans.setter
    def city_plans(self, city_plans: list):
        """
            -> list[CityPlan]
        """
        self._city_plans = [CityPlan(city_plans[0]), CityPlan(city_plans[1]), CityPlan(city_plans[2])]
        assert len(city_plans) == 3 and type(city_plans) == list
        assert {1, 2, 3} == {self._city_plans[0].position, self._city_plans[1].position, self._city_plans[2].position}

    @city_plans_won.setter
    def city_plans_won(self, city_plans_won: list):
        '''
            ->list[bool]
        '''
        assert len(city_plans_won) == 3 and type(city_plans_won) == list
        assert type(city_plans_won[0]) == bool
        assert type(city_plans_won[1]) == bool
        assert type(city_plans_won[2]) == bool

        self._city_plans_won = city_plans_won

    @construction_cards.setter
    def construction_cards(self, construction_cards: list):
        '''
            ->list[list[int, effect]]
        '''
        all_effects = {"surveyor", "agent", "landscaper", "pool", "temp", "bis"}
        assert len(construction_cards) == 3 and type(construction_cards) == list
        assert 1 <= construction_cards[0][0] <= 15 and type(construction_cards[0][0]) == int
        assert 1 <= construction_cards[1][0] <= 15 and type(construction_cards[1][0]) == int
        assert 1 <= construction_cards[2][0] <= 15 and type(construction_cards[2][0]) == int

        assert construction_cards[0][1] in all_effects
        assert construction_cards[1][1] in all_effects
        assert construction_cards[2][1] in all_effects

        self._construction_cards = construction_cards

    @effects.setter
    def effects(self, effects: list):
        '''
            ->list[effect]
        '''
        all_effects = {"surveyor", "agent", "landscaper", "pool", "temp", "bis"}
        assert len(effects) == 3 and type(effects) == list
        assert effects[0] in all_effects
        assert effects[1] in all_effects
        assert effects[2] in all_effects

        self._effects = effects

    def validate(self, game_state):
        '''
            game_state: GameState -> None
        '''
        assert len(game_state) == 4

    def to_dict(self):
        game_state = {}
        game_state["city-plans"] = []
        game_state["city-plans-won"] = self.city_plans_won
        game_state["construction-cards"] = self.construction_cards
        game_state["effects"] = self.effects

        for city_plan in self.city_plans:
            city_plan_dict = {}
            city_plan_dict["criteria"] = city_plan.criteria
            city_plan_dict["position"] = city_plan.position
            city_plan_dict["score1"] = city_plan.score1
            city_plan_dict["score2"] = city_plan.score2
            
            game_state["city-plans"].append(city_plan_dict)

        return game_state

    def city_plan_completed(self):
        return all(self.city_plans_won)
