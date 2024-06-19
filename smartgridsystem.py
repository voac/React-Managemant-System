import random
import numpy as np
from sklearn.linear_model import LinearRegression
import time

class PowerPlant:
    def __init__(self, name, max_production):
        self.name = name
        self.max_production = max_production
        self.current_production = 0

    def produce_power(self):
        return self.current_production

    def adjust_production(self, required_production):
        # Add a buffer of 10MW to the required production
        self.current_production = min(self.max_production, required_production + 26)
        return self.current_production

class Consumer:
    def __init__(self, name, max_consumption_day, max_consumption_night):
        self.name = name
        self.max_consumption_day = max_consumption_day
        self.max_consumption_night = max_consumption_night
        self.current_consumption = 0

    def consume_power(self, time_of_day):
        if time_of_day == '낮':
            self.current_consumption = random.uniform(0, self.max_consumption_day)
        else:
            self.current_consumption = random.uniform(0, self.max_consumption_night)
        return self.current_consumption

class GridController:
    def __init__(self, plants, consumers):
        self.plants = plants
        self.consumers = consumers
        self.day_consumption_data = []
        self.night_consumption_data = []
        self.time_steps_day = []
        self.time_steps_night = []
        self.power_shortage_events = []
        self.power_surplus_count = 0
        self.excessive_consumption_events = []

    def balance_grid(self, time_of_day, day):
        total_consumption = sum(consumer.consume_power(time_of_day) for consumer in self.consumers)
        total_production = sum(plant.produce_power() for plant in self.plants)

        if time_of_day == '낮':
            self.day_consumption_data.append(total_consumption)
            self.time_steps_day.append(day)
        else:
            self.night_consumption_data.append(total_consumption)
            self.time_steps_night.append(day)

        if total_consumption - total_production >= 10:
            self.excessive_consumption_events.append((day, time_of_day, total_consumption, total_production, total_consumption - total_production))
            print(f"\033[95m[Day {day} - {time_of_day.capitalize()}] 과도한 전력 소비 발생: {total_consumption:.2f} MW 사용, {total_production:.2f} MW 생산, 차이: {total_production - total_consumption:.2f} MW\033[0m")
        elif total_production >= total_consumption:
            self.power_surplus_count += 1
            print(f"\033[92m[Day {day} - {time_of_day.capitalize()}] 전원 공급 원활: {total_consumption:.2f} MW 사용, {total_production:.2f} MW 생산, 차이: {total_production - total_consumption:.2f} MW\033[0m")
        else:
            self.power_shortage_events.append((day, time_of_day, total_consumption, total_production, total_consumption - total_production))
            print(f"\033[91m[Day {day} - {time_of_day.capitalize()}] 전원 부족!: {total_consumption:.2f} MW 사용, {total_production:.2f} MW 생산, 차이: {total_production - total_consumption:.2f} MW\033[0m")

    def predict_production(self, time_of_day):
        # Perform linear regression to predict future consumption
        if time_of_day == '낮':
            X = np.array(self.time_steps_day).reshape(-1, 1)
            y = np.array(self.day_consumption_data)
        else:
            X = np.array(self.time_steps_night).reshape(-1, 1)
            y = np.array(self.night_consumption_data)
        
        if len(y) < 2:
            return sum(plant.max_production for plant in self.plants)  # Return max possible production if not enough data
        
        model = LinearRegression()
        model.fit(X, y)

        next_day = max(self.time_steps_day + self.time_steps_night) + 1
        predicted_consumption = model.predict(np.array([[next_day]]))[0]
        print(f"{next_day}일 {time_of_day} 예측 사용량 : {predicted_consumption:.2f} MW")

        return predicted_consumption

# Example usage
plants = [PowerPlant("Plant1", 100), PowerPlant("Plant2", 100)]
consumers = [
    Consumer("House1", 50, 20), 
    Consumer("House2", 30, 15), 
    Consumer("Factory1", 80, 30)
]

controller = GridController(plants, consumers)

# Initial 30 days with fixed production
for day in range(1, 31):
    for time_of_day in ['낮', '밤']:
        for plant in plants:
            plant.current_production = 100  # Fixed production of 100 MW per plant
        controller.balance_grid(time_of_day, day)

# Predict and balance grid for subsequent days
next_day = 31
days_to_simulate = 365 - 30

while days_to_simulate > 0:
    for time_of_day in ['낮', '밤']:
        predicted_consumption = controller.predict_production(time_of_day)
        for plant in plants:
            plant.adjust_production(predicted_consumption / len(plants))
        controller.balance_grid(time_of_day, next_day)

    time.sleep(0.01)  # Wait for 0.05 seconds before moving to the next day

    next_day += 1
    days_to_simulate -= 1

print("\033[94m시뮬레이션 종료.\033[0m")
print(f"\033[92m전원 공급 원활: {controller.power_surplus_count}\033[0m")
print(f"\033[91m전원 공급 부족 발생 횟수: {len(controller.power_shortage_events)}\033[0m")
for event in controller.power_shortage_events:
    day, time_of_day, consumption, production, difference  = event
    print(f"\033[91m    - Day {day}, {time_of_day.capitalize()} - 사용량: {consumption:.2f} MW, 생산량: {production:.2f} MW, 차이: {production - consumption:.2f} MW\033[0m")

print(f"\033[95m과도한 전력 소비 발생 횟수: {len(controller.excessive_consumption_events)}\033[0m")
for event in controller.excessive_consumption_events:
    day, time_of_day, consumption, production, difference = event
    print(f"\033[95m    - Day {day}, {time_of_day.capitalize()} - 사용량: {consumption:.2f} MW, 생산량: {production:.2f} MW, 차이: {production - consumption:.2f} MW\033[0m")
