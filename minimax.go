package main

type node struct {
	maxNode         bool
	currentPosition int
	stack           int
	redProb         float32
	greenProb       float32
	dblGreenProb    float32
}

func expectminimax(node node, depth int) int {
	// Terminal node
	if node.currentPosition+node.stack >= 17 {
		return 100
	}
	if !node.maxNode {

	} else if node.maxNode {
		// if there are +2's left, return that. Other than that, red
		if node.dblGreenProb != 0 {
			return 2
		} else if node.greenProb != 0 {
			return 1
		} else {
			return 0
		}
	}
	return 0
}
