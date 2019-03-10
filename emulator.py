import os

import count_area
import prediction


class Hydroponics:
    def __init__(self, plant_number):
        '''

        :param plant_number: starts with 1
        '''
        self.plant_number = plant_number
        # self. all_squares = count_area.read_areas_from_file(plant_number, type='array')
        self.all_squares = count_area.read_areas_from_file(plant_number - 1)
        self.emu_data = []
        self.cell = plant_number if plant_number < 5 else plant_number + 2
        self.predictions = []
        self.mistakes = []
        self.max_predictions = 12

    def add_measurements(self, count):
        assert (len(self.emu_data) + count) <= len(self.all_squares)
        self.emu_data = self.all_squares[:len(self.emu_data) + count]

    def get_last_image(self):
        assert len(self.emu_data) > 0
        path = os.path.join('camera_emulator', str(self.cell) + '_cell', '')
        return path

    def predict(self):
        self.predictions = prediction.make_prediction(self.emu_data.values, self.max_predictions)
        self.mistakes = prediction.calculate_mistake(self.predictions,
                                                     self.all_squares.values[len(self.emu_data):len(self.emu_data) + self.max_predictions])




emulator = Hydroponics(3)


# print(emulator.emu_data)

emulator.add_measurements(50)
# print(emulator.emu_data)

# print(emulator.all_squares.values[len(emulator.emu_data):len(emulator.emu_data) + emulator.max_predictions])

emulator.predict()
print(emulator.predictions)
print(emulator.mistakes)

