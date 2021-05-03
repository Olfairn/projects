"""Simulation of customer behaviour in a supermarket

User story:
A program that shows the state of each customer at each timestep. The result is a csv file with all timesteps over one day.

Pseudocode:
Create supermarket instance
FOR (i in number of steps):
    Create some random number of customers
    Move all customers one step (some enter the market, some exit the market)
    Print some information about how many customers are where
    Gather all customer states in a dataframe
Save the dataframe with the customer states over time

"""

import time

import numpy as np

import transition_matrix
    

class Customer:
    """A customer in the supermarket
    """

    def __init__(self, id, state):
        self.id = id
        self.state = state

    def move(self):
        """ make customer move one step (change its state) """
        probabilities = PROB_MATRIX.loc[self.state]
        self.state = np.random.choice(probabilities.index, p = probabilities.values)

    def is_active(self):
        """ is the customer inside the supermarket? """
        if self.state == "checkout":
            return False
        else:
            return True

    def __repr__(self):
        return f"id: {self.id}, state: {self.state}"


class Supermarket:
    """Just a normal supermarket
    """

    def __init__(self):
        self.customers = []
        self.time = 7*60 # 7 o'clock
        self.customer_history = []
        self.id_counter = 0

    def next_step(self):
        """ Propagate to next timestep """
        self.time += 1
        for customer in self.customers:
            customer.move()
            self.customer_history.append(
                (self.time, customer.id, customer.state))

    def add_new_customers(self, number):
        """ Let new customers enter the market """
        for i in range(number):
            state = np.random.choice(
                ENTRANCE_PROB.index, p = ENTRANCE_PROB.values)
            self.customers.append(
                Customer(id = self.id_counter + i, state = state))
            self.customer_history.append(
                (self.time, self.id_counter + i, state))
        self.id_counter += number

    def get_time(self):
        """ Print the time of the day """
        print(f"Time: {time.strftime('%M:%S', time.gmtime(self.time))}")

    def print_customers(self):
        """ Print the state of all customers in the supermarket """
        return self.customers

    def nr_active_customers(self):
        """ Print the number of active customers """
        nr_active = 0
        for customer in self.customers:
            if customer.is_active() is True:
                nr_active += 1
        return nr_active

    def __repr__(self):
        return f"I am just a normal supermarket. I had {len(self.customers)} customers so far."


PROB_MATRIX = transition_matrix.get_transition_probabilities()
ENTRANCE_PROB = transition_matrix.get_entrance_probabilities()

lidl = Supermarket()
lidl.add_new_customers(10)

lidl.print_customers()

lidl.get_time()

lidl.next_step()
    
lidl.customer_history

lidl.nr_active_customers()