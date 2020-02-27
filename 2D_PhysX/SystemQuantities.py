import copy
import itertools
import functools
import operator

from vpython import arrow
from vpython import vec
from vpython import mag

from matplotlib import pyplot as plt

class Reductor(object):
    """Performs reduction on call"""
    def __init__(self, identity_element, reduce_operation,):
        self.identity_element = identity_element
        self.reduce_operation = reduce_operation

    def __del__(self):
        del self.identity_element
        del self.reduce_operation

    def __call__(self, elements):
        return functools.reduce(self.reduce_operation, elements, self.identity_element)

class Quantity(object):
    """Physical quantity (momenta, energies etc.) with appropriate id, unit and computing scheme"""
    def __init__(self, quantity_id, unit, reductor, compute_one_element_function):
        self.quantity_id = quantity_id
        self.unit = unit
        self.reductor = reductor
        self.compute_one_element_function = compute_one_element_function

    def __del__(self):
        del self.quantity_id
        del self.unit
        del self.reductor
        del self.compute_one_element_function

    def compute_and_reduce(self, vObjects):	
        return self.reductor(map(self.compute_one_element_function, vObjects))

class SystemQuantities(object):
    """Class able to compute and store quantites of many systems and subsystems of objects and display a plot of chosen ones"""

    def __init__(self, arrow_pos=None):
        self.quantities = {}
        self.magnitudes = {}
        self.arrow_pos = arrow_pos

        if arrow_pos is not None:
            self.arrow = arrow(pos = arrow_pos, axis = vec(0, 0, 0), scale=2, shaftwidth=0.2)

        scalar_addition = Reductor(0, operator.add)
        vector_addition = Reductor(vec(0, 0, 0), operator.add)

        self.addQuantity("momentum",                        "Ns",   vector_addition,   lambda vObj : vObj.mass * vObj.vel)
        self.addQuantity("kinetic energy",                  "J",    scalar_addition,   lambda vObj : 0.5 * vObj.mass * mag(vObj.vel) ** 2)
        self.addQuantity("rotational kinetic energy",       "J",    scalar_addition,   lambda vObj : 0.5 * vObj.moment_of_inertia * vObj.ang_vel ** 2)
        self.addQuantity("elastic potential energy",        "J",    scalar_addition,   lambda vObj : 0.5 * vObj.stiffness * mag(vObj.obj.axis) ** 2)

        self.__plot_titles__ = { (False, False) : lambda quantity, system_id : system_id.capitalize() + " " + quantity.quantity_id,
                                 (False, True)  : lambda quantity, system_id : quantity.quantity_id.capitalize() + " of systems",
                                 (True, False)  : lambda quantity, system_id : system_id.capitalize(),
                                 (True, True)   : lambda quantity, system_is : "Quantities of systems" }
                                                         
        self.__plot_labels__ = { (False, False) : lambda quantity, system_id : system_id.capitalize() + " " + quantity.quantity_id,
                                 (False, True)  : lambda quantity, system_id : system_id.capitalize(),
                                 (True, False)  : lambda quantity, system_id : quantity.quantity_id.capitalize(),
                                 (True, True)   : lambda quantity, system_id : system_id.capitalize() + " " + quantity.quantity_id}

    def __delete__(self):
        del self.quantities
        del self.magnitudes

        if self.arrow_pos is not None:
            del self.arrow

    def addQuantity(self, quantity):
        self.quantities[quantity_id] = copy.copy(quantity)

    def addQuantity(self, quantity_id, unit, reductor, compute_one_element_function):
        self.quantities[quantity_id] = Quantity(quantity_id, unit, reductor, compute_one_element_function)

    def compute(self, vObjects, quantity_id, system_id=None, save_all_values=False):
        if quantity_id not in self.quantities:
            raise ValueError("quantity_id must be a key previously used to add quantity")

        systemMagnitude = self.quantities[quantity_id].compute_and_reduce(vObjects)

        if system_id is not None:
            if quantity_id not in self.magnitudes:   #create dictionary for the quantity if needed
                self.magnitudes[quantity_id] = {}

            if system_id not in self.magnitudes[quantity_id]:   #create list for the system if needed
                self.magnitudes[quantity_id][system_id] = []

                if not save_all_values:                         #prepare place for one magnitude
                    self.magnitudes[quantity_id][system_id].append(None)
                #for save_all_values magnitudes will be appended so there is no
                #need to reserve space

            systemMagnitudes = self.magnitudes[quantity_id][system_id]

            if save_all_values:
                systemMagnitudes.append(copy.copy(systemMagnitude))
            else:                
                systemMagnitudes[0] = copy.copy(systemMagnitude)

            if self.arrow_pos is not None and system_id is "global":   #resultant magnitude of whole system is passed to self.arrow
                self.arrow.axis = systemMagnitude
        
        return systemMagnitude

    def __prepare_for_plotting__(self, list):
        if len(list) == 0: return list

        if isinstance(list[0], vec):
            return [mag(i) for i in list]
        else:
            return list

    def __call_plt_plot__(self, values, quantity, system_id, is_many_elements_2D):
        plot_label = self.__plot_labels__[is_many_elements_2D](quantity, system_id)

        plt.plot(range(1, len(values) + 1), self.__prepare_for_plotting__(values), label = plot_label)
    
    def __prepare_plot_title__(self, quantity, system_id, is_many_elements_2D):
        return self.__plot_titles__[is_many_elements_2D](quantity, system_id)

    def plot(self, quantity_ids, system_ids):
        if len(quantity_ids) == 0 or len(system_ids) == 0:
            return  #if no data was received, do nothing

        (is_many_quantities, is_many_systems) = is_many_elements_2D = (len(quantity_ids) > 1, len(system_ids) > 1)

        #if a list is one element long (the element is assumed to be constant
        #for every value in other list)
        if all(is_many_elements_2D) and len(quantity_ids) != len(system_ids):
            raise ValueError("Quantities and systems length must match or at least one has to be 1.")

        for quantity_id in quantity_ids:
            if quantity_id not in self.quantities:
                raise ValueError("quantity_id must be a key previously used to add quantity")

        ids_iterator = list(zip(quantity_ids, system_ids)) if all(is_many_elements_2D) else list(itertools.product(quantity_ids, system_ids))

        for quantity_id, system_id in ids_iterator:
            if quantity_id not in self.magnitudes or system_id not in self.magnitudes[quantity_id]:
                raise ValueError("Magnitudes for given systen system and quantity not found")

        quantity = self.quantities[quantity_ids[0]]

        fig = plt.figure() 
        plt.title(self.__prepare_plot_title__(quantity, system_ids[0], is_many_elements_2D))
        plt.xlabel("Time [ticks]")        

        if is_many_quantities == False:
            plt.ylabel(quantity.quantity_id.capitalize() + " [" + quantity.unit + "]")
        
        for quantity_id, system_id in ids_iterator:
            values = self.magnitudes[quantity_id][system_id]
            quantity = self.quantities[quantity_id]
            self.__call_plt_plot__(values, quantity, system_id, is_many_elements_2D)

        if any(is_many_elements_2D):
            plt.legend(loc="upper left")
        
        plt.show()