from house import Home

class Street:
    def __init__(self, street, valid_pools, valid_parks):
        self.homes = street["homes"]
        self.parks = street["parks"]
        self.pools = street["pools"]
        self.roundabout = self.homes

        self.validate(street, valid_pools, valid_parks)

    @property
    def homes(self):
        return self._homes

    @property
    def parks(self):
        return self._parks

    @property
    def pools(self):
        return self._pools

    @property
    def roundabout(self):
        return self._roundabout

    @homes.setter
    def homes(self, homes: list):
        """
            Format a single street such that every element is
            Home([left_fence, val, used_in_plan, right_fence])
            -> list[Home]
        """
        _homes = []
        _homes.append(Home([True, homes[0], homes[1], homes[2][0]]))

        for i in range(2, len(homes) - 1):
            home = homes[i] + [homes[i + 1][0]]
            _homes.append(Home(home))

        _homes.append(Home(homes[-1] + [True]))

        self._homes = _homes
    
    @parks.setter
    def parks(self, parks: int):
        '''
            -> int
        '''
        assert type(parks) == int and 0 <= parks

        self._parks = parks

    @pools.setter
    def pools(self, pools: list):
        '''
            -> list[bool]
        '''
        assert len(pools) == 3 and type(pools) == list
        assert type(pools[0]) == bool
        assert type(pools[1]) == bool
        assert type(pools[2]) == bool

        self._pools = pools

    @roundabout.setter
    def roundabout(self, homes: Home):
        '''
            -> list[int]
        '''
        roundabouts = []
        for i, home in enumerate(homes):
            if home.val == "roundabout":
                roundabouts.append(i)
        self._roundabout = roundabouts

    def validate(self, street: dict, valid_pools: list, valid_parks: int):
        '''
            -> None
        '''
        assert len(street) == 3

        prev_home_number, non_bis_count = -1, 0
        
        # When we encounter a bis, the bis'd house is either some number of houses ahead
        #   of the bis, or directly behind the bis
        # Indicates whether the bis'd house is ahead or not of the matching bis house.
        ahead = False

        for i, home in enumerate(self.homes):
            if home.bis == True:
                if not ahead and i != 0 and self.homes[i - 1].val == home.val:
                    assert not home.left_fence
                else:
                    if ahead:
                        assert home.val == prev_home_number
                    else:
                        ahead = True
                        assert prev_home_number < home.val
                        prev_home_number = home.val
            else:
                if ahead == True:
                    assert home.val == prev_home_number and not home.left_fence
                    ahead = False
                    non_bis_count += 1
                else:
                    if type(home.val) == int:
                        assert prev_home_number < home.val
                        prev_home_number = home.val
                        non_bis_count += 1
                    else:
                        assert not home.used_in_plan
                        if home.val == "roundabout":
                            prev_home_number = -1
                            assert home.left_fence and home.right_fence
                
        assert not ahead
        assert self.parks <= non_bis_count and self.parks <= valid_parks

        if self.pools[0]:
            assert type(self.homes[valid_pools[0]].val) == int and not self.homes[valid_pools[0]].bis
        if self.pools[1]:
            assert type(self.homes[valid_pools[1]].val) == int and not self.homes[valid_pools[1]].bis
        if self.pools[2]:
            assert type(self.homes[valid_pools[2]].val) == int and not self.homes[valid_pools[2]].bis