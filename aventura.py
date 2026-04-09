# Variaveis globais do jogo - CUIDADO: Nao use variaveis globais em projetos grandes!
import random
player_name = ""
player_health = 0
inventory = []
current_location = ""
monster_general_damage = 0 #dano geral dos monstros por ai

# Mapa do jogo
locations = {
    "Clareira Tranquila": {
        "description": "Você está em uma clareira ensolarada. Há um caminho para o Leste.",
        "east": "Caminho da Floresta",
        "west": "Pântano Misterioso",
        "items": ["poção pequena","poção misteriosa"] 
    },
    "Caminho da Floresta": {
        "description": "Uma trilha estreita serpenteia pela floresta. Você pode ir para o Oeste ou Norte.",
        "west": "Clareira Tranquila",
        "north": "Caverna Sombria",
    },
    "Caverna Sombria": {
        "description": "Uma caverna escura e úmida. Há um brilho fraco no fundo. Você pode voltar para o Sul.",
        "south": "Caminho da Floresta",
        "items": ["amuleto mágico"]
    },
    "Pântano Misterioso": {
        "description": "Um pântano denso e perigoso. Você sente um arrepio. Há um caminho para o Leste.",
        "east": "Clareira Tranquila",
        "south" : "Vila Ninja",
        "challenge": True  # Novo desafio
    },
    "Vila Ninja": {
        "description" : "Uma remota e escondida Vila de ninjas,Há um caminho para leste",
        "east": "Mina Abandonada",
        "north" : "Pântano Misterioso",
        "items" : ["poção_pequena"]
    },
    "Mina Abandonada" : {
        "description" : "Uma estranha mina abandonada a anos ,Há uma saida ao oeste",
        "east": "Caminho da Floresta",
        "west" : "Vila Ninja",
        "items" : ["poção_pequena","item misterioso"],
        "challenge": True
    }
}

print(type(locations))
def display_status():
    print("\n--- Status do Jogador ---")
    print(f"Nome: {player_name}")
    print(f"Vida: {player_health}")
    print(f"Inventário: {", ".join(inventory) if inventory else "Vazio"}")
    print("------------------------")


def main_game_loop():
    global player_name, player_health, current_location, inventory , monster_general_damage

    # Inicializacao do jogo
    player_name = input("Qual o seu nome, aventureiro? ")
    player_health = 100
    current_location = "Clareira Tranquila"
    inventory = []

    game_active = True
    while game_active:
        display_status()
        print(f"\nVocê está em: {current_location}")
        print(locations[current_location]["description"])

        # Opcoes de saida
        exits = []
        for direction in ["north", "south", "east", "west"]:
            if direction in locations[current_location]:
                exits.append(direction.capitalize())
        print(f"Saídas disponíveis: {", ".join(exits)}")

        # Itens no local
        if "items" in locations[current_location] and locations[current_location]["items"]:
            print(
                f"Itens neste local: {", ".join(locations[current_location]["items"])}")

        # Desafio no local
        if "challenge" in locations[current_location] and locations[current_location]["challenge"] == True: #atualizei o sistema de luta
            monster_general_damage = random.randint(20,50) # gera um dano aleatorio para o inimigo do local do jogo
            print("Um monstro impede seu caminho!")
            action_combat = input("o que deseja fazer?\n enfrentar o monstro - 1\n Tentar Fugir - 2 \n ação:")
            if action_combat == "1":
                player_health = player_health - monster_general_damage
                print(f"Você lutou bravamente, mas perdeu {monster_general_damage} pontos de vida. Vida atual: {player_health}")
            elif action_combat == "2":
                roleta_dinamica = random.randint(1,2) # calcula em 50% de chance se o jogador consegue fugir
                if roleta_dinamica == 1:
                    print(f"Você consegiu fugir ileso")
                else:
                    player_health = player_health - int(monster_general_damage * 1.2) 
                    print(f"o monstro de alcançou e você levou {int(monster_general_damage * 1.2)} pontos de dano\nVida atual:{player_health}")
            else:
                print(f"comando invalido")
                continue
            locations[current_location]["challenge"] = False

        action = input(
            "O que você quer fazer?\n1 - Andar\n2 - Pegar item\n3 - Usar item\n4 - Sair\nEscolha: ").strip()

        if action == "1":
            direction_input = input(
                "Digite a direção (norte, sul, leste, oeste): ").lower().strip()

            if direction_input == "norte" and "north" in locations[current_location]:
                current_location = locations[current_location]["north"]
            elif direction_input == "sul" and "south" in locations[current_location]:
                current_location = locations[current_location]["south"]
            elif direction_input == "leste" and "east" in locations[current_location]:
                current_location = locations[current_location]["east"]
            elif direction_input == "oeste" and "west" in locations[current_location]:
                current_location = locations[current_location]["west"]
            else:
                print("Você não pode ir nessa direção.")

        elif action == "2":
            if "items" in locations[current_location] and locations[current_location]["items"]:
                # pega o primeiro item
                item_to_pick = locations[current_location]["items"][0]
                inventory.append(item_to_pick)
                locations[current_location]["items"].remove(item_to_pick)

                print(f"Você pegou o {item_to_pick}.")
            else:
                print("Não há itens para pegar aqui.")

        elif action == "3":
            item_to_use = input("Qual item deseja usar? ").lower().strip()

            if item_to_use in inventory:
                if item_to_use == "poção pequena":
                    player_health += 20
                    inventory.remove(item_to_use)
                    print("Você usou a poção e recuperou 20 de vida.")
                elif item_to_use == "poção misteriosa": # poção com chance de ganhar ou perder vida
                    roleta_dinamica = random.randint(1,2)
                    if roleta_dinamica == 1: 
                        player_health += 50
                        print("Parabéns a poção era de cura e você ganhou 50 pontos de vida")
                    else:
                        player_health -= 20
                        print("a Poção era de veneno e você perdeu 20 pontos de vida")
                elif item_to_use == "amuleto mágico":
                    print("Você usou o Amuleto Mágico! PARABÉNS, você venceu o jogo!")
                    game_active = False
                else:
                    print("Você não sabe como usar este item agora.")
            else:
                print("Você não tem este item no seu inventário.")

        elif action == "4":
            game_active = False
            print("Você decidiu sair da Floresta Encantada. Até a próxima!")

        else:
            print("Comando inválido.")

        # Condicoes de fim de jogo
        if player_health <= 0:
            print("Sua vida chegou a zero. Fim de jogo!")
            game_active = False

        if current_location == "Caverna Sombria" and "amuleto mágico" in inventory and game_active:
            print("Você encontrou o Amuleto Mágico e venceu o jogo!")
            game_active = False


# Chamada principal para iniciar o jogo
main_game_loop()
