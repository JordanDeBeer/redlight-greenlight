package main

import (
	"fmt"

	"github.com/JordanDeBeer/redlight-greenlight/probabilities"
)

func main() {
	if probabilities.PredictDraw(0, 0, 0, 0, 0) {
		fmt.Println("draw")
	} else {
		fmt.Println("walk")
	}
}

//func main() {
//g := game.NewGame()
////fmt.Printf("%+v\n", g)
//localServer.NewLocalGame(*g)
//}
