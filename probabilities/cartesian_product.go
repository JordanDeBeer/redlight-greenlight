package probabilities

type score [2]int
type boardState struct {
	playerScore      score
	spentRed         int
	spentGreen       int
	spentDoubleGreen int
	opponentScore    score
}

func product(states ...boardState) (ch chan boardState) {
	for _, v := range states {

	}
}
