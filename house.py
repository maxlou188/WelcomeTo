class Home:
    def __init__(self, home):
        self.left_fence = home[0]
        self.bis = home[1]
        self.val = home[1]
        self.used_in_plan = home[2]
        self.right_fence = home[3]

        self.validate(home)

    @property
    def right_fence(self):
        return self._right_fence

    @property
    def left_fence(self):
        return self._left_fence
    
    @property
    def used_in_plan(self):
        return self._used_in_plan
    
    @property
    def bis(self):
        return self._bis
    
    @property
    def val(self):
        return self._val

    @right_fence.setter
    def right_fence(self, has_right_fence: bool):
        '''
            -> bool
        '''
        assert type(has_right_fence) == bool

        self._right_fence = has_right_fence
    
    @left_fence.setter
    def left_fence(self, has_left_fence: bool):
        '''
            -> bool
        '''
        assert type(has_left_fence) == bool

        self._left_fence = has_left_fence

    @used_in_plan.setter
    def used_in_plan(self, is_used_in_plan: bool):
        '''
            -> bool
        '''
        assert type(is_used_in_plan) == bool

        self._used_in_plan = is_used_in_plan

    @bis.setter
    def bis(self, val: list):
        '''
            -> bool
        '''
        if type(val) == list:
            assert len(val) == 2
            assert 0 <= val[0] <= 17
            assert val[1] == "bis"

        self._bis = type(val) == list

    @val.setter
    def val(self, val):
        '''
            val: list or str or int -> int
        '''
        assert type(val) == list or type(val) == str or type(val) == int
        if type(val) == int:
            assert 0 <= val <= 17
        elif type(val) == str:
            assert val == "blank" or val == "roundabout"
        
        self._val = val[0] if self.bis else val

    def validate(self, home):
        '''
            home: Home -> bool
        '''
        assert len(home) == 4