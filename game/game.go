package game

const (
	// NumberRedCards is the number of Red cards in a deck.
	NumberRedCards = 11
	// NumberGreenCards is the number of Green cards in a deck.
	NumberGreenCards = 24
	// NumberDblGreenCards is the number of Double Green cards in a deck.
	NumberDblGreenCards = 13
	// TotalCards is the total number of cards in a deck. Equal to 50 in a typical deck
	TotalCards = NumberRedCards + NumberGreenCards + NumberDblGreenCards

	DrawAction = "draw"
	WalkAction = "walk"
)

type Player int
type Action string

type Turn struct {
	Player   Player
	Stack    int
	Action   Action
	LastDraw Card
}

type Game struct {
	PlayerTurn      Player
	PlayerPositions map[Player]int
	DrawPile        Deck
	RecyclePile     Deck
	Winner          Player
}

func NewGame() *Game {
	game := &Game{
		PlayerTurn:      0,
		PlayerPositions: map[Player]int{0: 0, 1: 0},
		DrawPile:        NewDeck(),
		RecyclePile:     []Card{},
		Winner:          -1,
	}
	return game
}

func (g *Game) StageTurn(t *Turn) Turn {
	// Walk Action.
	if t.Action == "walk" {
		return g.ExecuteTurn(*t)
	}
	// Draw Action
	card := g.DrawPile.DrawCard()
	t.LastDraw = card
	g.RecyclePile = append(g.RecyclePile, card)
	// If player draws a red card, end their turn.
	if card == 0 {
		t.Stack = 0
		return g.ExecuteTurn(*t)
	}
	t.Stack += int(card)
	return *t
}

func (g *Game) ExecuteTurn(t Turn) Turn {
	g.PlayerPositions[t.Player] += t.Stack
	if g.PlayerPositions[t.Player] >= 17 {
		g.Winner = t.Player
	}
	return g.nextturn()
}

func (g *Game) nextturn() Turn {
	turn := Turn{Stack: 0}
	if g.PlayerTurn == 0 {
		g.PlayerTurn = 1
		turn.Player = 1
	} else {
		g.PlayerTurn = 0
		turn.Player = 0
	}
	return turn
}
