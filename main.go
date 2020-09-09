package main

import "github.com/JordanDeBeer/redlight-greenlight/ev_calc"

//func main() {
//	var possibleScores [][2]int
//	var x int = 0
//	var y int = 0
//	for x+y < 16 {
//		y++
//		possibleScores = append(possibleScores, [2]int{x, y})
//		if x+y == 16 {
//			y = 0
//			x++
//		}
//
//	}
//	fmt.Println(possibleScores)
//}

func main() {
	ev_calc.FindEv(ev_calc.BoardState{0, 0, 0, 0, 0, 0})
}
