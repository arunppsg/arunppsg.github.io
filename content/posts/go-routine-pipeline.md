+++
title = "Go Routine Pipelines"
date = 2026-06-11
[taxonomies]
tag = ['go-lang']
+++

The idea is to build a pipeline that connects an arbitrary number of Go routines with channels.

### Approach 1
The below was my first approach.

```go
func try1() {
	n := int(N)
	allChans := make(map[int](chan int))
	for i := range n {
		allChans[i] = make(chan int)
		go func(i int) {
			<-allChans[i]
		}(i)
		allChans[i] <- i
	}
}
```

Why I thought it will work? On Go routine `i`, we send into channel `i` and receive from channel `i`.
But the issues with this approach are:
1. There is no channel pipeline here, each Go routine is independent of the other.
2. After a Go routine finishes, the channel created for it ( `allChan[i]`) still exists in the map.
The map retains references of a channel even after a Go routine has been finished, resulting in a memory leak.

### Approach 2

```go
func try2() {
	n := int(N)
	inChan := make(chan int)
	for i := range n {
		go func(i int) {
			val := <-inChan
			if i < n-1 {
				inChan <- val
			}
		}(i)
	}
	inChan <- 5
}
```

Issue with this approach:
- this is a fan-out because one Go routine sends into `inChan` while the remaining Go routines are waiting on the same `inChan` channel.

### Approach 3

```go
var N = 1e4
func main() {
	n := int(N)
	in := make(chan int)
	for i := range n {
		out := make(chan int)
		go func(inChan <-chan int) {
			a := <-inChan
			out <- a
		}(in)
		if i == 0 {
			in <- 1
		}
		if i == n-1 {
			j := <-out
			fmt.Printf("Received final out value: %d\n", j)
		}
		in = out
	}
}
```

For a channel `out`, it is held as reference only by two Go routines: 1) the immediate Go routine created after it's creation where it is used as a channel to send to 2) the next consecutive Go routine, where it is used as the `in` channel.
Since each Go routine hold on to only two-endpoints - one endpoint to receive, another to send, once a Go routine completes, it no longer holds reference to the channel `out`, which allows it to be garbage collected, thereby preventing memory leaks.

Consider same as above, except that `in` channel is not passed as parameter.
The Go routine will act as a closure in this case and the loop will look like this:

```go
in := make(chan int)
for i := range(n) {
    out := make(chan int)
    go func() {
        a := <- in
        out <- a
    }()
    if i == 0 {
        in <- 1
    }
    if i == n-1 {
        j := <-out
    }
    in = out
}
```

In the above case, the Go routine will attempt to read `in` from the outer scope.
But when `in` gets reassigned to `out` in iteration `k`, the new Go routine from iteration `k+1` will attempt a receive from the new `out`. 
Here, the Go routine in iteration `k+1` is reading from the wrong channel, a channel it was never supposed to read from.
But when we create a parameter, a copy of the `in` channel will be made at the time when the next Go routine is launched.

Now, what will happen if N is very large?
In such a scenario, the creation of Go routine will outpace completion, creating more Go routine stacks.
A stack size will be ~2 KB and it might result in out of memory error.

This can be prevented by limiting the number of Go routines using a semaphore, which can limit the number of concurrent Go routines. Here is an example of it:
```go
func main() {
	n := int(N)
	in := make(chan int)
	counts := make(chan struct{}, 100)
	for i := range n {
		counts <- struct{}{}
		out := make(chan int)
		go func(inChan <-chan int) {
			a := <-inChan
			out <- a
			<-counts
		}(in)
		if i == 0 {
			in <- 1
		}
		if i == n-1 {
			j := <-out
			fmt.Printf("Received final out value: %d\n", j)
		}
		in = out
	}
}
```
