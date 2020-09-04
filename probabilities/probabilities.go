package probabilities

import (
	"fmt"

	"github.com/JordanDeBeer/redlight-greenlight/game"
)

// EVMap is a map[string]float32 where the key is a string representation of a turn state to the estimated value of a turn
// Format is ${stack}-${spendRed}-${spentGreen}-${spendDblGreen}
var EVMap map[string]float32

func countSpentCards(spentDeck []game.Card, cardColor game.Card) (count int) {
	for _, card := range spentDeck {
		if card == cardColor {
			count++
		}
	}
	return count
}

func FindEv(count, stack int, spentDeck []game.Card) (ev float32) {
	// Seed some initial values to get started.
	// Single red card left.
	EVMap[fmt.Sprintf("%v-%v-%v-%v", 0, game.NumberRedCards, game.GreenCard, game.DblGreenCard)] = 0

	cardsLeft := len(spentDeck)
	spentRed := countSpentCards(spentDeck, game.RedCard)
	spentGreen := countSpentCards(spentDeck, game.GreenCard)
	spentDblGreen := countSpentCards(spentDeck, game.DblGreenCard)

	redProb := float32(game.NumberRedCards-spentRed-count) / float32(cardsLeft)
	greenProb := float32(game.NumberGreenCards-spentGreen-count) / float32(cardsLeft)
	dblGreenProb := float32(game.NumberDblGreenCards-spentDblGreen-count) / float32(cardsLeft)

	// Immediate EV of the next draw
	ev = float32(-stack)*redProb + 1*greenProb + 2*dblGreenProb
	// Recurse to find the value of drawing more cards from the deck if green
	FindEv(count+1, stack+1, spentDeck)
	// Recurse to find the value of drawing more cards from the deck if double green

	return
}

func PredictDraw(position, stack int, spentRed, spentGreen, spentDblGreen int) bool {
	if position+stack >= 17 {
		return false
	}
	cardsLeft := game.TotalCards - spentRed - spentGreen - spentDblGreen

	redProb := float32(game.NumberRedCards-spentRed) / float32(cardsLeft)
	greenProb := float32(game.NumberGreenCards-spentGreen) / float32(cardsLeft)
	dblGreenProb := float32(game.NumberDblGreenCards-spentDblGreen) / float32(cardsLeft)

	expectedValue := float32(-stack)*redProb + 1*greenProb + 2*dblGreenProb
	fmt.Println(expectedValue)

	oppRedProb := float32(game.NumberRedCards-spentRed-1) / float32(cardsLeft-1)
	oppGreenProb := float32(game.NumberGreenCards-spentGreen-1) / float32(cardsLeft-1)
	oppDblGreenProb := float32(game.NumberDblGreenCards-spentDblGreen-1) / float32(cardsLeft-1)

	oppRedEv := float32(0)*oppRedProb + 1*oppGreenProb + 2*oppDblGreenProb
	oppGreenEv := float32(0)*oppRedProb + 1*oppGreenProb + 2*oppDblGreenProb
	oppDblGreenEv := float32(0)*oppRedProb + 1*oppGreenProb + 2*oppDblGreenProb

	fmt.Println(expectedValue)
	expectedValue = expectedValue + (oppRedEv + oppGreenEv + oppDblGreenEv/3)
	fmt.Println(expectedValue)
	if expectedValue > 0 {
		return true
	}
	return false
}
