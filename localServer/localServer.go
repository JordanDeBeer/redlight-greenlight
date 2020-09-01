package localServer

import (
	"fmt"

	"github.com/JordanDeBeer/redlight-greenlight/game"
)

func NewLocalGame(game.Game) {
	thisGame := game.NewGame()
	turn := &game.Turn{Player: thisGame.PlayerTurn, Stack: thisGame.PlayerPositions[thisGame.PlayerTurn], Action: ""}
	for thisGame.Winner == -1 {
		fmt.Printf("\nPlayer %v's turn\n", thisGame.PlayerTurn)
		fmt.Printf("Stack: %v. Position: %v\n", turn.Stack, thisGame.PlayerPositions[thisGame.PlayerTurn])
		fmt.Println("Enter 'draw' or 'walk': ")
		var action game.Action
		fmt.Scanln(&action)
		turn.Action = action
		*turn = thisGame.StageTurn(turn)
	}
	fmt.Printf("%v has won!\n", thisGame.Winner)
}
