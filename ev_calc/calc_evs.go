package ev_calc

import (
	"fmt"
	"log"
	"math"

	"github.com/JordanDeBeer/redlight-greenlight/game"
)

var EvMap map[BoardState]float32

type BoardState struct {
	BoardPosition int
	Stack         int

	SpentRed         int
	SpentGreen       int
	SpentDoubleGreen int

	OpponentBoardPosition int
}

func init() {
	EvMap = make(map[BoardState]float32)

}

func isBsConstant(bs BoardState) bool {
	scoreNeeded := 17 - (bs.BoardPosition + bs.Stack)
	if scoreNeeded <= 0 {
		log.Print("found ev in constant winstate", bs)
		winState := BoardState{99, 99, 99, 99, 99, 99}
		EvMap[winState] = float32(0)
		return true
	}
	// If there are no red cards left and drawing would result in a win
	if bs.SpentRed == 12 && 1*(game.NumberGreenCards-bs.SpentGreen)+2*(game.NumberDoubleGreenCards-bs.SpentDoubleGreen) >= scoreNeeded {
		log.Print("found ev in constant inf green win", bs)
		EvMap[bs] = float32(math.Inf(1))
		return true
	}
	// If there are only red cards left at the start of your turn
	if bs.Stack == 0 && bs.SpentGreen == 25 && bs.SpentDoubleGreen == 14 {
		log.Print("found ev in constant only red", bs)
		EvMap[bs] = 0.0
		return true
	}
	// Constant for only red cards left and not at the start of your turn
	//if bs.Stack != 0 && bs.SpentGreen == 25 && bs.SpentDoubleGreen == 14 {
	//	if game.NumberRedCards-bs.SpentRed%2 == 0 {
	//		EvMap[bs] = -FindEv(BoardState{bs.BoardPosition})

	//	}

	//}
	return false

}

// FindEv finds the estimated value for a board state
func FindEv(bs BoardState) (ev float32) {
	cardsLeft := game.TotalCards - (bs.SpentRed + bs.SpentGreen + bs.SpentDoubleGreen)

	// If there are zero cards left, we "reshuffle" the deck.
	if cardsLeft == 0 {
		bs = BoardState{bs.BoardPosition, bs.Stack, 0, 0, 0, bs.OpponentBoardPosition}
	}
	if cachedEv, ok := EvMap[bs]; ok {
		return cachedEv
	}
	if isBsConstant(bs) {
		return EvMap[bs]
	}
	redProb := (float32(game.NumberRedCards) - float32(bs.SpentRed)) / float32(cardsLeft)
	greenProb := (float32(game.NumberGreenCards) - float32(bs.SpentGreen)) / float32(cardsLeft)
	doubleGreenProb := (float32(game.NumberDoubleGreenCards) - float32(bs.SpentDoubleGreen)) / float32(cardsLeft)

	var greenRecurseEv, doubleGreenRecurseEv float32
	//	if cardsLeft == 1 {
	//		greenRecurseEv = FindEv(BoardState{bs.BoardPosition, bs.Stack + 1, 0, 0, 0, bs.OpponentBoardPosition})
	//		doubleGreenRecurseEv = FindEv(BoardState{bs.BoardPosition, bs.Stack + 2, 0, 0, 0, bs.OpponentBoardPosition})
	//	} else {
	if game.NumberGreenCards-bs.SpentGreen == 0 {
		greenRecurseEv = greenProb * FindEv(BoardState{bs.BoardPosition, bs.Stack + 1, bs.SpentRed, bs.SpentGreen, bs.SpentDoubleGreen, bs.OpponentBoardPosition})
	} else {
		greenRecurseEv = greenProb * FindEv(BoardState{bs.BoardPosition, bs.Stack + 1, bs.SpentRed, bs.SpentGreen + 1, bs.SpentDoubleGreen, bs.OpponentBoardPosition})
	}
	if game.NumberDoubleGreenCards-bs.SpentDoubleGreen == 0 {
		doubleGreenRecurseEv = doubleGreenProb * FindEv(BoardState{bs.BoardPosition, bs.Stack + 2, bs.SpentRed, bs.SpentGreen, bs.SpentDoubleGreen, bs.OpponentBoardPosition})
	} else {
		doubleGreenRecurseEv = doubleGreenProb * FindEv(BoardState{bs.BoardPosition, bs.Stack + 2, bs.SpentRed, bs.SpentGreen, bs.SpentDoubleGreen + 1, bs.OpponentBoardPosition})
	}
	//	}
	fmt.Printf("-%v*%v + %v*%v + %v*%v\n", bs.Stack, redProb, greenRecurseEv, greenProb, doubleGreenRecurseEv, doubleGreenProb)
	ev = float32(-bs.Stack)*redProb + (greenRecurseEv+1)*greenProb + (doubleGreenRecurseEv+2)*doubleGreenProb

	EvMap[bs] = ev
	fmt.Printf("%v:%v\n", bs, EvMap[bs])
	return ev
}
