"""
File: Distant Skies (main)
Description: Python implementation of a board game made by Holden Linnan and Kent Carrier.
Author: Kent Carrier
Email: kentbo0528@gmail.com
"""


from helpers import *
import generation as gen
from dataclasses import dataclass, field, is_dataclass, asdict
from typing import Union
import json


@dataclass(frozen=False)
class Colony:
    owner: Union["Player", None]
    name: str = 'no_save_referenced'
    docked: dict["Fleet"] = field(default_factory=dict)
    prod_per_turn: int = 25


@dataclass(frozen=True)
class Build:
    name: str
    parts: dict


@dataclass(frozen=False)
class Ship:
    name: str
    build: "Build"
    parent_fleet: str
    fuel: float = 100
    drive_charge: float = 100
    attack: float = 100


@dataclass(frozen=False)
class Fleet:
    name: str
    owner: Union["Player", None]
    location: Union["Planet", "Moon", "Colony", "Orbit"]
    members: list["Ship"] = field(default_factory=list)


@dataclass(frozen=True)
class Orbit:
    origin: Union["Planet", "Moon"]
    destination: Union["Planet", "Moon"]


@dataclass(frozen=False)
class Player:
    name: str
    net_worth: int = 0
    owned_colonies: dict["Colony"] = field(default_factory=dict)
    owned_fleets: dict["Fleet"] = field(default_factory=dict)


@dataclass(frozen=False)
class System:
    """
    planets is a list of Planet objects.
    """
    stars: frozenset
    planets: list
    name: str = 'Centauri'


@dataclass(frozen=True)
class Star:
    temp: int


@dataclass(frozen=False)
class Planet:
    """
    moons is a list of Moon objects.
    """
    name: str
    area: int
    moons: list
    colonies: dict[any] = field(default_factory=dict)


@dataclass(frozen=False)
class Moon:
    name: str
    area: int
    colonies: dict["Colony"] = field(default_factory=dict)


@dataclass(frozen=False)
class Game:
    system: "System"
    players: list["Player"]


def join_players():
    """
    Creates a list of players.
    :return: ordered list of players, which are each strings
    """
    while True:
        playercount = num_choice('Number of players: ', 2, 8)
        if playercount > 8 or playercount < 1:
            slow_print('Please input a number between 2 and 4.', 2)
            continue
        break

    players = []
    if bool_choice('Would you like for the players to have names? '):
        for player in range(1, playercount + 1):
            players.append(Player(input('Name for Player ' + str(player) + ': ')))
    else:
        player = 0
        while playercount > player:
            player += 1
            players.append(Player('Player ' + str(player)))

    return players


def play():

    dreadnaught = Build(
        'dreadnaught',
        {
            'hyperdrive': 200,
            'life support': 100,
            'targeting': 100
        }
    )
    colony_ship = Build(
        'colony ship',
        {
            'shield generator': 500
        }
    )
    capital_ship = Build(
        'capital ship',
        {
            'hyperdrive': 300,
            'life support': 200,
            'shield generator': 100
        }
    )
    fighter = Build(
        'fighter',
        {
            'life support': 50
        }
    )
    builds = {
        'dreadnaught': dreadnaught,
        'colony ship': colony_ship,
        'capital ship': capital_ship,
        'fighter': fighter
    }

    def read_system():

        slow_print('The system consists of the following:')
        types = {
            1: 'M',
            2: 'K',
            3: 'G',
            4: 'F',
            5: 'A',
            6: 'B',
            7: 'O'
        }
        for star in system.stars:
            slow_print('> One ' + str(types[star.temp]) + ' type star')

        for planet in system.planets:
            planet.name = system.name + ' ' + planet.name
            if planet.area == 0:
                slow_print('> A gas giant planet, ' + planet.name + ', with ', new_line=False)
            else:
                slow_print('> A terrestrial planet, ' + planet.name + ', with ' +
                           str(planet.area) + ' sites suitable for colonies, and ', new_line=False)
            if planet.moons != 0:
                if len(planet.moons) == 1:
                    slow_print('1 moon.')
                else:
                    slow_print(str(len(planet.moons)) + ' moons.')
                moon_count = 0
                for moon in planet.moons:
                    moon.name = system.name + ' ' + moon.name
                    moon_count += 1
                    if moon.area != 1:
                        slow_print('\t' + moon.name + ' has ' + str(moon.area) + ' sites suitable for colonies.')
                    else:
                        slow_print('\t' + moon.name + ' has ' + str(moon.area) + ' site suitable for a colony.')
            else:
                slow_print('no moons.')

    def rename_system(new_name):

        system.name = new_name
        for planet in system.planets:
            planet.name = new_name + ' ' + planet.name[-1]
            for moon in planet.moons:
                moon.name = new_name + ' ' + moon.name[-2:]

    def list_colonies(location):
        """
        :param location: Moon or Planet object with an attribute "colonies".
        """
        num = len(location.colonies)
        if num == 1:
            slow_print('This body has 1 colony:')
        elif num == 0:
            slow_print('This body has no colonies.')
        else:
            slow_print('This body has' + str(num) + 'colonies:')
        for colony in location.colonies.values():
            slow_print(colony.name + ' is owned by ' + colony.owner.name + '.')

    def establish_colony(celest_body):
        """
        Establishes a colony on a given body if and only if the player owns a ship that currently orbits the body, the
        ship is carrying enough resources to establish said colony, and if there is an open space for a colony on the
        body. If the ship in question is a colony ship, the colony resource requirement will be waived.
        :param celest_body: name of the body the player wants to establish a colony on
        :return:
        """

        for planet in system.planets:
            if celest_body.lower() == planet.name.lower():
                if len(planet.colonies) < planet.area:
                    if bool_choice('Would you like to give this colony a custom name? '):
                        name = any_choice('Custom name: ').lower()
                    else:
                        name = gen.random_name(system).lower()
                    colony = Colony(player, name.lower())
                    planet.colonies.update({name: colony})
                    player.owned_colonies.update({name: colony})
                    colonies.add(colony.name)
                    slow_print('New colony ' + colony.name.capitalize() + ' successfully established on ' + planet.name +
                               ', outputting 25 resources per turn.')
                    return True
                elif planet.area == 0:
                    slow_print('You cannot establish a colony on a gas giant planet.')
                    return False
                else:
                    slow_print('This planet already has the maximum number of colonies.', 2)
                    return False
            else:
                for moon in planet.moons:
                    if celest_body.lower() == moon.name.lower():
                        if len(moon.colonies) < moon.area:
                            if bool_choice('Would you like to give this colony a custom name? '):
                                name = any_choice('Custom name: ')
                            else:
                                name = gen.random_name(system)
                            colony = Colony(player, name)
                            moon.colonies.update({name.lower(): colony})
                            player.owned_colonies.update({name.lower(): colony})
                            colonies.add(colony.name)
                            slow_print('New colony ' + colony.name + ' successfully established on ' + moon.name +
                                       ', outputting 25 resources per turn.')
                            return True
                        else:
                            slow_print('This moon already has the maximum number of colonies.', 2)
                            return False

        slow_print((body + ' was not found anywhere in the system.'), 2)
        return False

    def purchase_ship():
        """
        Create a Ship object from a player request.
        :return: Build object in the form of the requested build.
        """
        selection = ''
        try:
            selection = builds[list_choice('Please choose a model.\n> ', builds).lower()]
        except KeyError:
            print('You somehow managed to input a word that simultaneously is and isn\'t the name of a ship in the '
                  'catalog. Please contact Kent and tell him how you figured that out. And don\'t do it again.')
            return
        finally:
            num = 1
            for fleet in player.owned_fleets.values():
                for ship in fleet.members:
                    if ship.build.name == selection.name:
                        num += 1

            build_site = player.owned_colonies[
                list_choice('Where will you construct this ship? ', player.owned_colonies)
            ]

            if bool_choice('Do you want to name your ship? '):
                while True:
                    name = any_choice('Custom ship name: ')
                    for fleet in player.owned_fleets.values():
                        for ship in fleet.members:
                            if name == ship.name:
                                slow_print('This name is already being used for one of your ships. '
                                           'Please choose another name.')
                    break
            else:
                name = selection.name + str(num)
            ship = Ship(name, selection, '')
            print(len(build_site.docked))
            if (len(build_site.docked) != 0) and bool_choice('There are fleets available at ' + build_site.name +
                                                             ' for your new ship to join. Merge ' + ship.name +
                                                             ' with one of them? '):
                joining = list_choice('Which fleet would you like to add your ship to? ', build_site.docked)
                build_site.docked[joining].append(ship)
                ship.parent_fleet = joining.name
            else:
                fleet = Fleet(ship.name + ' Fleet', player, build_site, [ship])
                build_site.docked.update({fleet.name: fleet})
                player.owned_fleets.update({fleet.name: fleet})
                ship.parent_fleet = fleet.name
            slow_print('Purchase successful! ' + ship.name + ' has been added to your fleet at ' + build_site.name + '.')

    def view_ships(target_player):
        """
        :param target_player: A Player object instance, NOT a string
        """
        slow_print('The following ships are in ' + target_player.name + '\'s possession:')
        for fleet in target_player.owned_fleets.values():
            for ship in fleet.members:
                if isinstance(fleet.location, Orbit):
                    slow_print(
                               ship.name.capitalize()
                               + ', a ' + ship.build.name
                               + ', currently en route from '
                               + fleet.location.origin.name + ' to ' + fleet.location.destination.name
                               )
                else:
                    slow_print(
                               ship.name.capitalize()
                               + ', a ' + ship.build.name
                               + ', currently at ' + fleet.location.name
                               )

    def move_fleet(fleet, destination):
        """
        :param fleet: is a Fleet object
        :param destination: is a Colony, Planet, or Moon object
        """
        origin = fleet.location
        if not isinstance(origin, Orbit):
            fleet.location = Orbit(fleet.location, destination)
        else:
            pass



    def normal(request):

        words = request.split()
        verb = words[0].lower()

        if verb == 'save':
            gen.save_game(Game(system, players))
        elif verb == 'establish':
            target_body = list_choice('Target body: ', bodies)
            establish_colony(target_body)
        elif verb == 'get' or verb == 'view':
            if words[1] == 'colonies':
                try:
                    body_name = ''
                    for word in words[3:]:
                        body_name += ' ' + word
                    body_name = body_name.strip().lower()
                    target_body = bodies[body_name]
                    print(target_body)
                    list_colonies(target_body)
                except IndexError:
                    slow_print('Incorrect syntax for this command. The syntax for this action is:'
                               '\n> ' + verb + ' colonies for [name of body]')
                except KeyError:
                    slow_print('Cannot find ' + words[3] + ' in the Proxima system.')
            elif words[1] == 'ships':
                try:
                    for named in players:
                        if named.name == words[3]:
                            view_ships(named)
                except IndexError:
                    view_ships(player)
            else:
                slow_print('"' + words[1] + '" is not a recognized object for the verb "get."')
        elif verb == 'purchase':
            purchase_ship()
        elif verb == 'move':
            if words[1] == 'fleet':
                fleets = player.owned_fleets.keys()
                fleet = words[2]
                if fleet in fleets:
                    destination = list_choice('Please enter a destination.', colonies)
                    move_fleet(player.owned_fleets[fleet], destination)

# Start of actual game

    if bool_choice('[new] | [continue]\n> ', 'new', 'continue'):

        players = join_players()

        system = gen.generate_system()
        system_name = any_choice('What name will you give to this system?\n> ')
        proper_name = system_name.lower()
        system.name = proper_name.capitalize()
        read_system()
        if bool_choice('Would you like to rename this system?\n> '):
            rename_system(any_choice('What name will you give to this system?\n> ').lower().capitalize())

    else:
        game = gen.load_game(any_choice('save name?\n> '))
        system = game.system
        players = game.players

    bodies = gen.celestial_dict(system)
    print(bodies)

    print('\n========================'
          '\nThe game will now begin!'
          '\n========================\n')

    colonies = set()

    slow_print('All players have been given one ship to create a colony with.')
    for player in players:
        slow_print('Where would ' + player.name + ' like to place their first colony? \n> ', 1, False)
        body = input()
        while not establish_colony(body):
            slow_print('Where would ' + player.name + ' like to place their first colony? \n> ', 1, False)
            body = input()

    while True:
        for player in players:
            while True:
                console_msg = 'It is currently ' + player.name + '\'s turn.\n> '
                command = any_choice(console_msg)
                if command.strip()[0:3] == 'end':
                    break
                elif command != 'stop':
                    normal(command)
                else:
                    return


if __name__ == '__main__':
    play()
