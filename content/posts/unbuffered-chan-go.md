+++
title = "Unbuffered Channels in Go"
date = 2026-05-28
[taxonomies]
tag = ['go-lang']
+++

I had a Go snippet like this:

```go
var (
	deposits = make(chan int) // send amount to deposit
	balances = make(chan int) // receive balance
)

func Deposit(amount int) { deposits <- amount }
func Balance() int       { return <-balances }

func teller() {
	var balance int // balance is confined to teller goroutine
	for {
		select {
		case amount := <-deposits:
			balance += amount
		case balances <- balance:
			fmt.Println("Sending in channel balances")
		}
	}
}

func main() {
	go teller() 
	Deposit(100)
	fmt.Println("Balance=", Balance())
	a, b := Balance(), Balance()
	fmt.Printf("Balance = %d, Balance = %d", a, b)
}
```

The issue:
`Balance` receives balance from `balances` channel.
When `Balance()` is called, how is it ensured that there is value in the channel for it to receive and that the call is non-blocking?

Here, `balances` is an unbuffered channel - it can never be full nor empty. An unbuffered channel expects a rendezvous i.e a simultaneous send and receive for communication to happen via that channel.

A receive on Balance() will happen when there is a send in the `balance` channel at the same time.
When a receiver is ready, the `select` statement proceeds to send a value in the `balances` channel. Otherwise, the `select` statement blocks until either one of the two actions happen - when a value is ready to be received in `balances` channel, so that it can send into it or when it receives a value from `deposits` channel.
