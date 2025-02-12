import pygame
from deck import Deck
from market import Market
from player import Player
from token_pool import TokenPool
from card import Card
from constants import WIDTH, HEIGHT, WHITE, BLACK, BEIGE, GOLD, RED, GREEN, font, small_font, CARD_TYPES
from qLearningAgent import *

class Game:
    
    def __init__(self):
        self.deck = Deck()
        self.market = Market(self.deck)
        self.players = [Player(), Player()]
        self.current_player = 0
        self.token_pool = TokenPool()
        self.game_over = False
        self.selected_market_cards = []
        self.selected_hand_cards = []
        self.confirm_button = pygame.Rect(900, 600, 200, 50)
        self.message = ""
        self.agent = QLearningAgent(self)
        self.deal_initial_cards()

    def get_state(self):
        # Retourne l'état actuel du jeu sous forme de tableau ou de dictionnaire
        state = {
            'current_player': self.current_player,
            'market': [card.type for card in self.market.goods],
            'player_hand': [card.type for card in self.players[self.current_player].hand],
            'player_camels': self.players[self.current_player].camels,
            'player_score': self.players[self.current_player].score,
            'token_pool': self.token_pool.pool
        }
        return state
    
    # vérifie les actions possibles en fonction du jeu actuel
    def get_actions(self):
        actions = []
        player = self.players[self.current_player]

        # Ajouter l'action de vendre des biens
        for good_type in CARD_TYPES:
            if good_type != 'Camel' and len([c for c in player.hand if c.type == good_type]) >= 2:
                actions.append(('sell', good_type))

        # Ajouter l'action de prendre des cartes du marché
        if len(player.hand) < 7:
            for i, card in enumerate(self.market.goods):
                actions.append(('take_market_card', i))

        # Ajouter l'action de prendre des chameaux
        if any(card.type == 'Camel' for card in self.market.goods):
            actions.append(('take_camels',))

        # Ajouter l'action d'échanger des cartes
        for i, card in enumerate(player.hand):
            if card.type != 'Camel':
                actions.append(('exchange', i))

        # Ajouter l'action de prendre le dernier jeton
        for good_type in CARD_TYPES:
            if good_type != 'Camel' and len([c for c in player.hand if c.type == good_type]) == 2:
                actions.append(('take_last_token', good_type))

        return actions


    def step(self, action):
        player = self.players[self.current_player]
        reward = 0
        done = False

        if action[0] == 'sell':
            good_type = action[1]
            bonus = player.sell_goods(good_type, self.token_pool)
            if bonus is not False:
                reward = bonus
                self.next_turn()

        elif action[0] == 'take_market_card':
            index = action[1]
            if len(player.hand) < 7:
                card = self.market.goods.pop(index)
                player.hand.append(card)
                self.market.replenish()
                self.next_turn()

        elif action[0] == 'take_camels':
            camel_cards = [card for card in self.market.goods if card.type == 'Camel']
            player.camels += len(camel_cards)
            for camel_card in camel_cards:
                self.market.goods.remove(camel_card)
            self.market.replenish()
            self.next_turn()

        elif action[0] == 'exchange':
            index = action[1]
            if len(player.hand) < 7:
                card = player.hand.pop(index)
                self.market.goods.append(card)
                self.market.replenish()
                self.next_turn()

        elif action[0] == 'take_last_token':
            good_type = action[1]
            if good_type != 'Camel' and len(self.token_pool.pool[good_type]) > 0:
                token = self.token_pool.pool[good_type].pop()
                player.score += token
                player.tokens[good_type].append(token)
                for card in [c for c in player.hand if c.type == good_type]:
                    player.hand.remove(card)
                self.next_turn()

        # Vérifier si le jeu est terminé
        self.check_game_end()
        if self.game_over:
            done = True

        return self.get_state(), reward, done

    def reset(self):
        # Réinitialise le jeu
        self.__init__()
        return self.get_state()

    def deal_initial_cards(self):
        for player in self.players:
            for _ in range(5):
                card = self.deck.cards.pop(0)
                if card.type == 'Camel':
                    player.camels += 1
                else:
                    player.hand.append(card)

    def handle_click(self, pos):
        if self.game_over:
            return

        if self.current_player == 1:  # C'est le tour de l'adversaire (joueur humain)
            player = self.players[self.current_player]

            # Vendre des cartes
            if not self.selected_market_cards:
                if 50 <= pos[0] <= 550 and (400 + self.current_player * 200) <= pos[1] <= (550 + self.current_player * 200):
                    index = (pos[0] - 50) // 60  # Ajustement de la position
                    if index < len(player.hand):
                        good_type = player.hand[index].type
                        bonus = player.sell_goods(good_type, self.token_pool)
                        if bonus is not False:
                            self.message = f"Bonus de {bonus} !"
                            self.next_turn()

            # Sélectionner une carte du marché
            for i, card in enumerate(self.market.goods):
                if 50 + i * 60 <= pos[0] <= 50 + (i + 1) * 60 and 100 <= pos[1] <= 220:  # Ajustement de la position
                    if card in self.selected_market_cards:
                        self.selected_market_cards.remove(card)
                    else:
                        self.selected_market_cards.append(card)
                    break

            # Sélectionner une carte de la main du joueur
            for i, card in enumerate(player.hand):
                if 50 + i * 60 <= pos[0] <= 50 + (i + 1) * 60 and (400 + self.current_player * 200) <= pos[1] <= (550 + self.current_player * 200):  # Ajustement de la position
                    if card in self.selected_hand_cards:
                        self.selected_hand_cards.remove(card)
                    else:
                        self.selected_hand_cards.append(card)
                    break

            # Prendre des chameaux
            if any(card.type == 'Camel' for card in self.selected_market_cards):
                camel_cards = [card for card in self.market.goods if card.type == 'Camel']
                player.camels += len(camel_cards)
                for camel_card in camel_cards:
                    self.market.goods.remove(camel_card)
                self.market.replenish()
                self.selected_market_cards = []
                self.next_turn()

            # Confirmer la sélection
            if self.confirm_button.collidepoint(pos):
                if len(self.selected_market_cards) == 1:
                    if len(player.hand) == 7:
                        self.message = "Trop de carte !"
                    else:
                        for card in self.selected_market_cards:
                            self.market.goods.remove(card)
                            player.hand.append(card)
                        self.market.replenish()
                        self.selected_market_cards = []
                        self.selected_hand_cards = []
                        self.next_turn()
                elif len(player.hand) + len(self.selected_market_cards) - len(self.selected_hand_cards) <= 7:
                    if len(self.selected_hand_cards) == len(self.selected_market_cards):
                        for card in self.selected_market_cards:
                            self.market.goods.remove(card)
                            player.hand.append(card)
                        for card in self.selected_hand_cards:
                            player.hand.remove(card)
                            self.market.goods.append(card)
                        self.market.replenish()
                        self.selected_market_cards = []
                        self.selected_hand_cards = []
                        self.next_turn()
                    elif len(self.selected_hand_cards) > len(self.selected_market_cards):
                        self.message = "Trop de carte de votre main selectionné"
                    else:
                        num_camels_needed = len(self.selected_market_cards) - len(self.selected_hand_cards)
                        if player.camels >= num_camels_needed:
                            player.camels -= num_camels_needed
                            for card in self.selected_market_cards:
                                self.market.goods.remove(card)
                                player.hand.append(card)
                            for _ in range(num_camels_needed):
                                self.market.goods.append(Card('Camel'))
                            self.market.replenish()
                            self.selected_market_cards = []
                            self.selected_hand_cards = []
                            self.next_turn()
                        else:
                            self.message = "Pas assez de chameaux pour remplacer les cartes sélectionnées."
                else:
                    self.message = "Trop de carte !"

                # Prendre le dernier jeton en payant avec 2 biens
                if len(self.selected_hand_cards) == 2 and self.selected_hand_cards[0].type == self.selected_hand_cards[1].type:
                    good_type = self.selected_hand_cards[0].type
                    if good_type != 'Camel' and len(self.token_pool.pool[good_type]) > 0:
                        token = self.token_pool.pool[good_type].pop()
                        player.score += token
                        player.tokens[good_type].append(token)
                        for card in self.selected_hand_cards:
                            player.hand.remove(card)
                        self.message = f"Jeton {good_type} de {token} points obtenu !"
                        self.next_turn()
                    else:
                        self.message = "Pas assez de jetons disponibles ou type de bien invalide."

        else:  # C'est le tour de l'agent
            state = self.get_state()
            available_actions = self.get_actions()  # Obtenir les actions possibles
            action = self.agent.choose_action(state)  # Choisir une action parmi les actions disponibles
            next_state, reward, done = self.step(action)
            self.agent.update_q_table(state, action, reward, next_state)

    def next_turn(self):
        self.current_player = 1 - self.current_player
        self.message = ""  # Réinitialiser le message à la fin du tour
        self.check_game_end()

    def check_game_end(self):
        if len(self.deck.cards) == 0:
            self.message = "End of game"
            self.game_over = True

        # Vérifier si trois types de jetons sont épuisés
        empty_token_types = sum(1 for values in self.token_pool.pool.values() if not values)
        if empty_token_types >= 3:
            self.message = "End of game"
            self.game_over = True

    def draw(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(BEIGE)

        # Afficher le marché
        pygame.draw.rect(screen, GOLD, (40, 90, 433, 100), 2)  # Nouvelles dimensions
        for i, card in enumerate(self.market.goods):
            pygame.draw.rect(screen, card.color, (50 + i * 60, 100, 54, 80))  # Ajustement de la position et de la taille
            if card in self.selected_market_cards:
                pygame.draw.rect(screen, RED, (50 + i * 60, 100, 54, 80), 2)  # Contour rouge pour les cartes sélectionnées

        # Afficher les mains des joueurs
        for p in range(2):
            player = self.players[p]
            y = 400 if p == 0 else 600
            pygame.draw.rect(screen, GOLD, (40, y - 10, 433, 100), 2)  # Nouvelles dimensions
            for i, card in enumerate(player.hand):
                pygame.draw.rect(screen, card.color, (50 + i * 60, y, 54, 80))  # Ajustement de la position et de la taille
                if card in self.selected_hand_cards:
                    pygame.draw.rect(screen, RED, (50 + i * 60, y, 54, 80), 2)  # Contour rouge pour les cartes sélectionnées

            # Afficher les scores
            text = font.render(f"Joueur {p + 1} : {player.score}", True, BLACK)
            screen.blit(text, (500, 400 + p * 200))

            # Afficher le nombre de chameaux
            camel_text = font.render(f"Chameaux : {player.camels}", True, BLACK)
            screen.blit(camel_text, (500, 440 + p * 200))

        # Indiquer quel joueur est en train de jouer
        current_player_text = font.render(f"Tour du Joueur {self.current_player + 1}", True, GREEN)
        screen.blit(current_player_text, (400, 50))

        # Afficher les jetons restants
        self.token_pool.draw_tokens(screen)

        # Afficher le bouton de confirmation
        pygame.draw.rect(screen, GOLD, self.confirm_button)
        confirm_text = font.render("Confirmer", True, BLACK)
        screen.blit(confirm_text, (950, 610))

        # Afficher le message
        message_text = font.render(self.message, True, BLACK)
        screen.blit(message_text, (400, 700))

        pygame.display.flip()
