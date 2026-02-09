+++
title = "Channel Closing In Go"
date = 2026-01-07
[taxonomies]
tag = ['go-lang']
+++

I had a go snippet like below:

```go
var cancel = make(chan struct{})
var wg sync.WaitGroup

func isCancelled() bool {
	select {
	case <-cancel:
		return true
	default:
		return false
	}
}

func send() {
	cancel <- struct{}{}
	close(cancel)
	wg.Done()
}

func main() {

	result1 := isCancelled()
	fmt.Printf("result1=%t\n", result1)

	go func() {
		result2 := isCancelled()
		fmt.Printf("result2=%t\n", result2)
	}()

	wg.Add(1)
	go send()
	wg.Wait()

	result3 := isCancelled()
	fmt.Printf("result3=%t\n", result3)
}
```

The above printed:

```
result1=false
result2=true
result3=true
```

I expected that `result3=false`  because the channel is closed `close(cancel)` after sending to the channel.
But it is the other case. Why?

When a channel is closed, it indicates that no more values will be sent on it. 
When `result3 := isCancelled()` is called, receiving from a closed channel yields zero value of the
channel (in this case `struct{}{}`) and thus `result3=true` was printed.

Suppose I modify the `send` method to not close the channel, what will be the output?
```go
func send() {
	cancel <- struct{}{}
	wg.Done()
}
```

When the modified `send` is run, it printed:
```
result1=false
result2=true
result3=false
```

In this case, since the channel is not closed, the select could not receive any value from the channel and thus, `result3` is false.

This is a nice idea because the closing of channel and a `select` statement can be used to broadcast a signal to other go routines that an event has occurred. 

Other references on the same:
- [https://gobyexample.com/closing-channels](https://gobyexample.com/closing-channels)
- [https://go.dev/blog/pipelines](https://go.dev/blog/pipelines)
