package main

import (
	"github.com/JordanDeBeer/redlight-greenlight/probabilities"
)

type node struct {
	maxNode            bool
	currentPosition    int
	stack              int
	redProb            float32
	greenProb          float32
	dblGreenProb       float32
	oppCurrentPosition int
	oppStack           int
}

func expectimax(node node, depth int) int {
	// Terminal node
	if node.currentPosition+node.stack >= 17 {
		return 100
	}
	if !node.maxNode {
		ev := probabilities.FindEv()
	}
	return 0
}
