package game

import (
	"math/rand"
)

const (
	// RedCard is a representation of a red card.
	RedCard Card = 0
	// GreenCard is a representation of a green card.
	GreenCard Card = 1
	// DblGreenCard is a representation of a double green card.
	DblGreenCard Card = 2
)

// Card is an int that represents a card (RedCard, GreenCard, or DblGreenCard)
type Card int

// Deck is a random (shuffled) deck of cards.
type Deck []Card

// NewDeck creates a new deck of random (shuffled) cards.
func NewDeck() Deck {
	var deck Deck
	for i := 0; i != NumberRedCards; i++ {
		deck = append(deck, RedCard)
	}
	for i := 0; i != NumberGreenCards; i++ {
		deck = append(deck, GreenCard)
	}
	for i := 0; i != NumberDblGreenCards; i++ {
		deck = append(deck, DblGreenCard)
	}
	rand.Shuffle(TotalCards, func(i, j int) { deck[i], deck[j] = deck[j], deck[i] })
	return deck
}

func (d *Deck) DrawCard() Card {
	card, newDeck := (*d)[len((*d))-1], (*d)[:len((*d))-1]
	*d = newDeck
	return card
}
