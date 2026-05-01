+++
title = "Understanding Context in Go"
date = 2026-05-01
[taxonomies]
tag = ['go-lang']
+++

The idea of using `context`, `cancel`, `<- ctx.Done()` was new to me when I learned Go.
I had a hard time wrapping my head around it and hence, writing this blog post for my future-self.

The idea is to send a signal to a process (goroutine), for example, to shutdown when an event occurs.

For understanding, we will take a toy program which does computation in two steps.
The main goroutine will create multiple goroutines and only one of the goroutines should proceed to step 2 computation.


One way to do it is by using channels - a non-context approach.
In this approach, we will send signal by closing the channel, like below:
```go
func computeBreakUsingSignal(id int, wg *sync.WaitGroup, responses chan<- int, signal <-chan struct{}) {
	defer wg.Done()

	// Long Compute part 1
	i := rand.Intn(5) + 5
	fmt.Println(id, " Sleeping for ", i, " seconds")
	time.Sleep(time.Duration(i) * time.Second)

	select {
	case responses <- i:
		fmt.Println(id, " finished first computation")
	case <-signal:
		fmt.Println(id, " returning")
		return
	}

	// Long Compute Part 2
	time.Sleep(10 * time.Second)
	fmt.Println(id, " completed second computation.")
}

func sendSignalByChannel() {
	var wg sync.WaitGroup

	responses := make(chan int)
	signal := make(chan struct{})

	for i := range 5 {
		wg.Add(1)
		go computeBreakUsingSignal(i, &wg, responses, signal)
	}

	resp := <-responses
	close(signal)
	fmt.Println("Received ", resp)
	wg.Wait()
}

func main() {
    sendSignalByChannel()
}
```

When a go routine returns, it sends a value in `responses` channel.
Upon receiving a value in `responses` channel, `sendSignalByChannel` closes `signal` channel, thereby preventing rest of the goroutines to proceed to step 2 of the computation.

Here is another way of doing the same, but with contexts which is the idiomatic Go approach.

```go
func sendSignalByContext() {
	var wg sync.WaitGroup

	responses := make(chan int)
	ctx, cancel := context.WithCancel(context.Background())

	for i := range 5 {
		wg.Add(1)
		go computeBreakUsingContext(i, &wg, responses, ctx)
	}

	resp := <-responses
	fmt.Println("Received ", resp)
	// cancel closes ctx.Done channel
	cancel()
	wg.Wait()
}

func computeBreakUsingContext(id int, wg *sync.WaitGroup, responses chan<- int, ctx context.Context) {
	defer wg.Done()
	i := rand.Intn(10) + 1

	fmt.Println(id, " Sleeping for ", i, " seconds")
	time.Sleep(time.Duration(i) * time.Second)

	select {
	case responses <- i:
		fmt.Println(id, " finished")
	case <-ctx.Done():
		fmt.Println(id, " returning")
		return
	}

	time.Sleep(10 * time.Second)
	fmt.Println(id, " completed second computation.")
}

func main() {
	sendSignalByContext()
}
```

When the first Go routine returns, we call the `cancel` method returned by `context.WithCancel` function.
The `cancel` method provides a way to close the `Done` channel of the context by calling it, thereby allowing us to send a signal to other Go routines.
In this example as well, only one of the goroutines will proceed to second computation.

A limitation here is when we send a signal or call `cancel`, the cancellation happens only after stage 1 of the long computation is completed - this is an inherent limitation and the long running function should check periodically for signals.
