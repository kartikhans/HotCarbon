from constant import EMISSIONS


class SaveInEmission:
    def __init__(
        self,
        embodied_em_new,
        energy_avg_old,
        energy_avg_new,
        expected_age,
        emission_per_unit,
    ):
        self.emNew = embodied_em_new
        self.avgEnergyOld = energy_avg_old / 1000
        self.avgEnergyNew = energy_avg_new / 1000
        self.emissionPerUnit = emission_per_unit / (1000 * 3600 * 1000)
        self.expectedAge = expected_age * 365 * 24 * 60 * 60

    def saved_emission(self, old_time, new_time):
        saved_by_embodied = (self.emNew / self.expectedAge) * new_time

        print(saved_by_embodied)
        saved_by_energy = (
            self.avgEnergyNew * new_time - self.avgEnergyOld * old_time
        ) * self.emissionPerUnit

        print(saved_by_embodied / (saved_by_energy + saved_by_embodied))
        return saved_by_energy + saved_by_embodied

    def old_emission_range(self, new_time):
        saved_by_embodied = self.emNew / (self.expectedAge * self.emissionPerUnit)

        saved_by_energy = self.avgEnergyNew

        return f"Total Energy of the device should be strictly less than {new_time * (saved_by_energy +
                                                                                      saved_by_embodied)}"


if __name__ == "__main__":
    new_avg_energy = 9399.75
    old_avg_energy = 6861
    emission_per_unit = 204
    k = SaveInEmission(
        embodied_em_new=EMISSIONS.get("M2"),
        energy_avg_old=old_avg_energy,
        energy_avg_new=new_avg_energy,
        expected_age=5,
        emission_per_unit=emission_per_unit,
    )

    exec_time_new = 22.82
    exec_time_old = 22
    emissions_saved = k.saved_emission(new_time=exec_time_new, old_time=exec_time_old)
    print(f"Emissions saved: {emissions_saved} Kg")
