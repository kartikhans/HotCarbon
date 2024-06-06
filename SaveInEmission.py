from datetime import datetime, timedelta
import multiprocessing

class SaveInEmission:
    def __init__(self, embodied_em_old, energy_avg_old, energy_avg_new, expected_age, emission_per_unit):
        self.emNew = embodied_em_old
        self.avgEnergyOld = energy_avg_old
        self.avgEnergyNew = energy_avg_new
        self.emissionPerUnit = emission_per_unit
        self.expectedAge = expected_age * 365 * 24 * 60 * 60

    def saved_emission(self, old_time, new_time):
        saved_by_embodied = (self.emNew/self.expectedAge)*new_time

        saved_by_energy = (self.avgEnergyNew*new_time - self.avgEnergyOld*old_time)*self.emissionPerUnit

        return saved_by_energy + saved_by_embodied

    def old_emission_range(self, new_time):
        saved_by_embodied = (self.emNew/(self.expectedAge*self.emissionPerUnit))

        saved_by_energy = self.avgEnergyNew

        return f"Total Energy of the device should be strictly less than {new_time * (saved_by_energy + 
                                                                                      saved_by_embodied)}"



if __name__ == '__main__':
    print("")

    m = multiprocessing.Manager()