class CityPlan:
    def __init__(self, city_plan):
        self.position = city_plan["position"]
        self.criteria = city_plan["criteria"]
        self.score1 = city_plan["score1"]
        self.score2 = city_plan["score2"]

    @property
    def criteria(self):
        return self._criteria

    @property
    def position(self):
        return self._position
    
    @property
    def score1(self):
        return self._score1

    @property
    def score2(self):
        return self._score2

    @criteria.setter
    def criteria(self, criteria: list):
        '''
        -> list[int]
        '''
        assert type(criteria) == list or type(criteria) == str
        if type(criteria) == list and all(type(i) == int for i in criteria):
            assert criteria == sorted(criteria)
        else:
            criteria_one = [["all houses", 0], ["all houses", 2], "end houses", "7 temps", "5 bis"]
            criteria_two = ["two streets all parks", "two streets all pools", ["all pools all parks", 1], ["all pools all parks", 2], "all pools all parks one roundabout"]

            if self.position == 1:
                assert criteria in criteria_one
            elif self.position == 2:
                assert criteria in criteria_two
            else:
                raise Exception("Invalid Position")
        
        self._criteria = criteria

    @position.setter
    def position(self, position: int):
        '''
        -> int
        '''
        assert 1 <= position <= 3 and type(position) == int

        self._position = position

    @score1.setter
    def score1(self, score1: int):
        '''
        -> int
        '''
        assert 0 <= score1 and type(score1) == int

        self._score1 = score1

    @score2.setter
    def score2(self, score2: int):
        '''
        -> int
        '''
        assert 0 <= score2 and type(score2) == int

        self._score2 = score2