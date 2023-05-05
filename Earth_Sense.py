import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import json

st.set_page_config(page_title='Air Quality Analysis',  layout='wide', page_icon=':Calculator:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Pokemon Game")
t2.markdown("Version 1.0")


import requests
import random

def get_pokemon_details(pokemon):
    """Retrieves details about a Pokemon from the PokeAPI."""
    pokemon_data = requests.get(pokemon['pokemon_species']['url']).json()
    pokemon_name = pokemon_data['name']
    pokemon_url = pokemon_data['varieties'][0]['pokemon']['url']
    pokemon_details = requests.get(pokemon_url).json()
    pokemon_type = pokemon_details['types'][0]['type']['name']
    pokemon_ability = pokemon_details['abilities'][0]['ability']['name']
    return pokemon_name, pokemon_type, pokemon_ability

def get_pokemon_moves(pokemon_name):
    url = f"https://pokeapi.co/api/v2/"
    pokemon_url = f"{url}pokemon/{pokemon_name}"
    response = requests.get(pokemon_url)
    if response.ok:
        moves = [move["move"]["name"] for move in response.json()["moves"]]
        return moves
    else:
        return None

def get_pokemon_attributes(pokemon_name):
    base_url = "https://pokeapi.co/api/v2/"
    pokemon_url = f"{base_url}pokemon/{pokemon_name}"
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        pokemon_details = response.json()
        attributes = {}

        for stat in pokemon_details['stats']:
            stat_name = stat['stat']['name']
            stat_value = stat['base_stat']
            attributes[stat_name] = stat_value

        return attributes
    else:
        print(f"Error: Failed to retrieve data for {pokemon_name}")
        return None    

st.write("Welcome to the Pokemon game!")
game_mode = st.text_input("Enter '1' for single player or '2' for two player: ")
if game_mode:
    st.write("You selected game mode:", game_mode)

if game_mode == '1':
    # Single player version of the game

    # Make a GET request to the PokeAPI to retrieve information about the Kanto Pokedex
    response = requests.get('https://pokeapi.co/api/v2/pokedex/kanto')

    # Parse the JSON response into a Python dictionary
    pokedex = response.json()

    # Retrieve the list of Pokemon in the Kanto Pokedex
    kanto_pokemon = pokedex['pokemon_entries']

    # Randomly select 20 Pokemon from the Kanto Pokedex
    selected_pokemon = random.sample(kanto_pokemon, 20)

    # Print information about the selected Pokemon
    #st.write("Here are 20 random Pokemon from the Kanto Pokedex:")
    for pokemon in selected_pokemon:
        pokemon_name, pokemon_type, pokemon_ability = get_pokemon_details(pokemon)
        #st.write(f"{pokemon_name:<15} (Type: {pokemon_type:<10}, Ability: {pokemon_ability:<20})")

    # Prompt the user to select a Pokemon
    while True:
        st.write("\nChoose 1 and begin your journey!")
        st.write("Enter the name of the Pokemon you want to choose:")
        pokemon_choice = st.selectbox('Select Pokemon', selected_pokemon)
        
        if pokemon_choice:
           st.write("\nGame starting...")
#           # Find the selected Pokemon in the list of randomly selected Pokemon
#           selected_pokemon_names = [get_pokemon_details(pokemon)[0] for pokemon in selected_pokemon]
#           if pokemon_choice in selected_pokemon_names:
#               st.write(f"You have chosen: ")
#               st.write(pokemon_choice)
#               break
#           else:
#               st.write("Invalid choice. Please try again.")


elif game_mode == '2':
    # Two player version of the game

    # Get the names of the players
    player1_name = st.text_input("Enter the name of player 1: ")
    if player1_name:
        player2_name = st.text_input("Enter the name of player 2: ")
    if player1_name:    

    # Make a GET request to the PokeAPI to retrieve information about the Kanto Pokedex
        response = requests.get('https://pokeapi.co/api/v2/pokedex/kanto')

    # Parse the JSON response into a Python dictionary
        pokedex = response.json()

    # Retrieve the list of Pokemon in the Kanto Pokedex
        kanto_pokemon = pokedex['pokemon_entries']

    # Randomly select 20 Pokemon from the Kanto Pokedex
        selected_pokemon = random.sample(kanto_pokemon, 20)

    # Print information about the selected Pokemon
        #st.write("Here are 20 random Pokemon from the Kanto Pokedex:")
        for pokemon in selected_pokemon:
            pokemon_name, pokemon_type, pokemon_ability = get_pokemon_details(pokemon)
           # st.write(f"{pokemon_name:<15} (Type: {pokemon_type:<10}, Ability: {pokemon_ability:<20})")

    # Prompt player 1 to select a Pokemon
    while True:
    # Find the selected Pokemon in the list of randomly selected Pokemon
        selected_pokemon_names = [get_pokemon_details(pokemon)[0] for pokemon in selected_pokemon]
        st.write("Player 1, choose 1 and begin your journey!")
        player1_choice = st.selectbox('Select Pokemon', selected_pokemon)
        
        if player1_choice:        
    # Prompt player 2 to select a Pokemon

            st.write("Player 2, choose 1 and begin your journey!")
            player2_choice = st.selectbox('Select Pokemon', selected_pokemon)

            if player2_choice:
    # Game starting
                st.write("Game starting...")
                st.write("Player 1has chosen :")
                st.write(player1_choice)
                st.write("Player 2 has chosen :")
                st.write(player2_choice)
                st.write("Let the battle begin!")
    # Code for the battle between player 1's and player 2's Pokemon
    # ...
                break
# Find the selected Pokemon in the list of randomly selected Pokemon
        selected_pokemon_names = [get_pokemon_details(pokemon)[0] for pokemon in selected_pokemon]



if player1_choice in selected_pokemon_names:
    attributes = get_pokemon_attributes(player1_choice)
    if attributes:
        moves = get_pokemon_moves(player1_choice)
        print("\n" + "-"*40)
        print(f"{player1_choice.upper()} BASE STATS:")
        for stat_name, stat_value in attributes.items():
            print(f"{stat_name.capitalize()}: {stat_value}")
        print("-"*40)
    else:
        print(f"Error: Failed to retrieve attributes for {player1_choice}. Please try again.")

if player2_choice in selected_pokemon_names:
    attributes = get_pokemon_attributes(player2_choice)
    if attributes:
        moves = get_pokemon_moves(player2_choice)
        print("\n" + "-"*40)
        print(f"{player2_choice.upper()} BASE STATS:")
        for stat_name, stat_value in attributes.items():
            print(f"{stat_name.capitalize()}: {stat_value}")
        print("-"*40)
    else:
        print(f"Error: Failed to retrieve attributes for {player2_choice}. Please try again.")


# Find the selected Pokemon in the list of randomly selected Pokemon
selected_pokemon_names = [get_pokemon_details(pokemon)[0] for pokemon in selected_pokemon]

if player1_choice in selected_pokemon_names and player2_choice in selected_pokemon_names:
    player1_stats = get_pokemon_attributes(player1_choice)
    player2_stats = get_pokemon_attributes(player2_choice)

    # Compare the total base stats of each player's selected Pokemon
    player1_total_stats = sum(player1_stats.values())
    player2_total_stats = sum(player2_stats.values())

    print(f"Player 1: {player1_choice.upper()}")
    for stat_name, stat_value in player1_stats.items():
        print(f"{stat_name.capitalize()}: {stat_value}")
    print(f"Total base stats: {player1_total_stats}\n")

    print(f"Player 2: {player2_choice.upper()}")
    for stat_name, stat_value in player2_stats.items():
        print(f"{stat_name.capitalize()}: {stat_value}")
    print(f"Total base stats: {player2_total_stats}\n")

    print("Let the battle begin!\n")
    time.sleep(1)

    # Determine which player attacks first
    players = [(player1_choice, player1_total_stats), (player2_choice, player2_total_stats)]
    random.shuffle(players)
    first_player = players[0][0]
    second_player = players[1][0]

    print(f"{first_player.upper()} attacks first!\n")
    time.sleep(1)

    while player1_total_stats > 0 and player2_total_stats > 0:
        # Determine the attack strength of each player
        player1_attack = random.randint(1, player1_total_stats)
        player2_attack = random.randint(1, player2_total_stats)

        # Reduce the total base stats of the player that attacks
        if first_player == player1_choice:
            player2_total_stats -= player1_attack
            print(f"{first_player.upper()} attacks with {player1_attack} strength!")
            time.sleep(1)
            if player2_total_stats <= 0:
                break
            player1_total_stats -= player2_attack
            print(f"{second_player.upper()} counterattacks with {player2_attack} strength!")
            time.sleep(1)
            if player1_total_stats <= 0:
                break
        else:
            player1_total_stats -= player2_attack
            print(f"{first_player.upper()} attacks with {player2_attack} strength!")
            time.sleep(1)
            if player1_total_stats <= 0:
                break
            player2_total_stats -= player1_attack
            print(f"{second_player.upper()} counterattacks with {player1_attack} strength!")
            time.sleep(1)
            if player2_total_stats <= 0:
                break

    print("\nThe battle is over!\n")
    time.sleep(1)

    if player1_total_stats > player2_total_stats:
        print(f"{first_player.upper()} wins!")
    elif player2_total_stats > player1_total_stats:
        print(f"{second_player.upper()} wins!")
    else:
        print("It's a tie!")
else:
    print("Invalid Pokemon choice for one or both players. Please try again.")
     

    
    

 

