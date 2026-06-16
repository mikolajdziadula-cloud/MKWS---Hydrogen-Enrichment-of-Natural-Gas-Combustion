import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

T0 = 700.0
P0 = 20 * ct.one_atm

lambda_values = np.linspace(0.7, 1.5, 60)
phi_values = 1.0 / lambda_values

h2_shares = {
    "0% H2": 0.00,
    "5% H2": 0.05,
    "10% H2": 0.10,
    "20% H2": 0.20,
    "40% H2": 0.40
}

gas = ct.Solution("gri30.yaml")

def mole_fraction(gas, species):
    if species in gas.species_names:
        return gas.X[gas.species_index(species)]
    return 0.0

results = {}

for label, h2_share in h2_shares.items():

    hydrogen_share = h2_share
    methane_share = 1.0 - hydrogen_share
    fuel = {
        "CH4": methane_share,
        "H2": hydrogen_share
    }

    results[label] = {
        "T": [],
        "CO2": [],
        "CO": [],
        "H2O": [],
        "O2": [],
        "NO": [],
        "NO2": [],
        "H2": []
    }

    for phi in phi_values:
        gas.TP = T0, P0

        gas.set_equivalence_ratio(
            phi,
            fuel=fuel,
            oxidizer={"O2": 1.0, "N2": 3.76}
        )

        gas.equilibrate("HP")

        results[label]["T"].append(gas.T)
        results[label]["CO2"].append(mole_fraction(gas, "CO2"))
        results[label]["CO"].append(mole_fraction(gas, "CO"))
        results[label]["H2O"].append(mole_fraction(gas, "H2O"))
        results[label]["O2"].append(mole_fraction(gas, "O2"))
        results[label]["NO"].append(mole_fraction(gas, "NO"))
        results[label]["NO2"].append(mole_fraction(gas, "NO2"))
        results[label]["H2"].append(mole_fraction(gas, "H2"))

for label in results:
    for key in results[label]:
        results[label][key] = np.array(results[label][key])

def make_plot(quantity, ylabel, filename):
    plt.figure(figsize=(8, 5))

    for label in h2_shares.keys():
        plt.plot(lambda_values, results[label][quantity], label=label)

    plt.xlabel(r"Air excess ratio $\lambda$ [-]")
    plt.ylabel(ylabel)
    plt.title(ylabel + r" vs $\lambda$")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

make_plot("T", "Adiabatic flame temperature [K]", "temperature.png")
make_plot("CO2", r"Mole fraction of CO$_2$ [-]", "CO2.png")
make_plot("CO", r"Mole fraction of CO [-]", "CO.png")
make_plot("H2O", r"Mole fraction of H$_2$O [-]", "H2O.png")
make_plot("O2", r"Mole fraction of O$_2$ [-]", "O2.png")
make_plot("NO", r"Mole fraction of NO [-]", "NO.png")
make_plot("NO2", r"Mole fraction of NO$_2$ [-]", "NO2.png")
make_plot("H2", r"Mole fraction of H$_2$ [-]", "H2_unburned.png")