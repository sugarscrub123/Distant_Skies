import distant_skies as ds
from helpers import *
import random as rand
import math
import os


def generate_system():

    want_random = bool_choice('Would you like a random system? Yes or no: ')
    max_size = 99
    if bool_choice('Is there a maximum size you would like to impose on this system? '):
        max_size = num_choice('Maximum size: ')

    def generate_star(bull=False):
        """
        Generates num number of stars.
        :param bull: boolean, if True, generate a random star
        :return: A Star object
        """
        if bull:
            star = ds.Star(rand.randint(1, 7))
        else:
            star = ds.Star(num_choice('Star temperature (from 1 to 7): ', 1, 7))
        return star

    def generate_terrestrial(name, bull=True):

        if bull:
            # Generate a random area from 3 to 6 for the colonies it can sustain
            size = rand.randint(3, 6)
            # Generate random moons to orbit the planet
            moons = generate_moons(name, size, True)
            colonies = []
            for n in range(0, size):
                colonies.append(None)
            planet = ds.Planet(name, size, moons)
        else:
            size = num_choice('Planet area (from 3 to 10): ', 3, 10)

            colonies = []
            for n in range(0, size):
                colonies.append(None)

            planet = ds.Planet(name, size, generate_moons(name, size, False))

        return planet

    def generate_gas_giant(name, bull=True):

        if bull:
            # Generate random moons to orbit the planet
            moons = generate_moons(name, 8, True)

            planet = ds.Planet(name, 0, moons)
        else:
            size = num_choice('ds.Planet area (from 3 to 10): ', 3, 10)

            planet = ds.Planet(name, size, generate_moons(name, size, False))

        return planet

    def generate_moons(planet_name, planet_size, bull=True):
        """
        Generates a moon with at least 1 colony site, and at most, 1 less site than the parent planet has.
        """

        moons = []
        # random generation
        if bull:
            moons_num = math.floor(math.exp(3 * rand.random() - 1))
            if planet_size < 8 and moons_num > 4:
                moons_num -= 2
            if planet_size > 5:
                moons_num += 1
                planet_size = planet_size // 2
            moon = 0
            while moon <= moons_num:
                name = str(planet_name) + chr(97 + moon)
                size = rand.randint(1, planet_size - 1)
                final_moon = ds.Moon(name, size)
                moons.append(final_moon)
                moon += 1
        # non-random generation
        else:
            command_message = 'How many moons for this planet? The planet\'s size is ' + str(planet_size) + '. '
            moons_num = num_choice(command_message)
            moon = 0
            while moon < moons_num:

                if moon == 0:
                    command_message = 'Moon area for the first moon (must be smaller than the planet): '
                elif moon == 1:
                    command_message = 'Moon area for the second moon (must be smaller than the planet): '
                elif moon == 2:
                    command_message = 'Moon area for the third moon (must be smaller than the planet): '
                else:
                    command_message = 'Moon area for the ' + str(
                        moon + 1) + 'th moon (must be smaller than the planet): '

                name = str(planet_name) + chr(97 + moon)
                size = num_choice(command_message, 1, planet_size - 1)
                moons.append(ds.Moon(name, size))
                moon += 1

        return moons

    def rename_system(system, new_name):

        for planet in system.planets:
            planet.name = new_name + ' ' + planet.name.split()[-1]
            for moon in planet.moons:
                moon.name = new_name + ' ' + moon.name.split()[-1]
        system.name = new_name

    if want_random:
        # Generate the stars that make up the system center
        star_num = rand.choices([1, 2, 3, 4, 5], [59.62, 31.52, 6.25, 1.88, .44])[0]
        suns = set()
        while star_num > 0:
            suns.add(generate_star(True))
            star_num -= 1

        # Frost line distance calculation
        frost_line = 0
        for sun in suns:
            frost_line += sun.temp**.5

        # Generate the planets
        planet_num = 0
        # At least one round of planets per star
        for i in range(1, len(suns)+1):
            planet_num += math.floor((rand.randint(4, 10))/(2*i))
        planets = []
        if planet_num > max_size:
            planet_num = max_size
        for current_planet in range(1, planet_num + 1):
            if current_planet <= frost_line:
                current_planet = generate_terrestrial(str(current_planet))
            else:
                current_planet = generate_gas_giant(str(current_planet))
            planets.append(current_planet)

    else:
        star_num = num_choice('Number of stars in the system: ')
        suns = set()
        while star_num > 0:
            suns.add(generate_star(False))
            star_num -= 1

        # Frost line distance calculation
        frost_line = 0
        for sun in suns:
            frost_line += sun.temp**.5

        # Generate the planets
        planet_num = num_choice('Number of planets: ', 1, None)
        planets = []
        for current_planet in range(1, planet_num):
            if current_planet <= frost_line:
                current_planet = generate_terrestrial(str(current_planet), False)
            else:
                current_planet = generate_gas_giant(str(current_planet), False)
            planets.append(current_planet)

    suns = frozenset(suns)

    return ds.System(suns, planets, 'Default')


def celestial_dict(system):
    """
    Generates a dictionary of the available bodies in the system.
    :param system: System object
    :return: dictionary with body names as the key and the Planet or Moon object as the value
    """

    bodies = dict()

    for planet in system.planets:
        for moon in planet.moons:
            bodies.update({moon.name.lower(): moon})
        bodies.update({planet.name.lower(): planet})

    return bodies


def random_line(afile):
    file = open(afile)
    line = next(file)
    for num, aline in enumerate(file, 2):
        if rand.randrange(num):
            continue
        line = aline
    return line


def random_name(system):
    """
    :return: str
    """

    try:
        # try to open the used_names file
        used_names = open('saves/save_game_' + system.name + '/used_names.txt', 'a+')
    except FileNotFoundError:
        # if it doesn't exist...
        try:
            # create the directory
            os.makedirs('saves/save_game_' + system.name)
        except FileExistsError:
            # if it already exists...
            pass
    finally:
        # directory shoud now exist. Now open .txt file
        used_names = open('saves/save_game_' + system.name + '/used_names.txt', 'w+')

    while True:
        name = random_line('colony_name_library.txt')[0:-1]
        if name not in used_names:
            used_names.seek(0, 2)
            used_names.write('\n' + name)
            used_names.close()
            return name


def load_game(save_name):
    with open('saves/save_game_' + save_name + '.txt', 'r') as save:
        suns = set()
        for line in save:
            data = save.read().strip()
            for i in range(0, len(data)):
                char = data[i]
                if char == 's':
                    suns.add(ds.Star(int(data[i+1])))




def save_game(new_game):

    with open('saves/save_game_' + new_game.system.name + '.txt', 'w+') as save:
        pass

