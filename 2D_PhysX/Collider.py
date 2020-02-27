import itertools

class Collider(object):
    """Uses registered collision rules to test for collisions as well as compute and apply their effects."""

    def __init__(self):
        self.collision_rules = dict()
        self.counter = 0

    def __delete__(self):
        del self.collision_rules
        del self.counter

    def add_collision_rule(self, vClasses, is_collision_func, apply_collision_func):
        self.collision_rules[self.generate_key(vClasses)] = [is_collision_func, apply_collision_func]

    def apply_to_product(self, vObject1, vObject2):
        """Compares two objects"""

        key = self.generate_key([vObject1, vObject2])

        if key not in self.collision_rules:
            raise ValueError("Rule applying to objects couldn't be found")
        
        rule = self.collision_rules[key]

        if rule[0] is None:
            return

        collision = rule[0](vObject1, vObject2)
        if collision:
            rule[1](vObject1, vObject2, collision)
            self.counter += 1

    def apply_to_product(self, vObjects1, vObjects2):
        """Compares cartesian product of two lists"""

        key = self.generate_key([vObjects1[0], vObjects2[0]])

        if key not in self.collision_rules:
            raise ValueError("Rule applying to objects couldn't be found")
        
        rule = self.collision_rules[key]

        if rule[0] is None:
            return

        for vObj1, vObj2 in itertools.product(vObjects1, vObjects2):
            collision = rule[0](vObj1, vObj2)
            if collision:
                rule[1](vObj1, vObj2, collision)
                self.counter += 1

    def apply_to_combinations(self, vObjects, length_of_subsequence):
        """Compares combinations of specified length"""

        key = self.generate_key([vObjects[0], vObjects[0]])

        if key not in self.collision_rules:
            raise ValueError("Rule applying to objects couldn't be found")
        
        rule = self.collision_rules[key]

        if rule[0] is None:
            return

        for vObj1, vObj2 in itertools.combinations(vObjects, length_of_subsequence):
            collision = rule[0](vObj1, vObj2)
            if collision:
                rule[1](vObj1, vObj2, collision)
                self.counter += 1

    def generate_key(self, vClasses):
        key = ""
        for vClass in vClasses:
            key += vClass.class_id()

        return key