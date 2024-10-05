# A.I Learnings
> [!IMPORTANT]
> This is only written for learning, so take everything with a grain of salt.

# A.I rps
This is a test between A.I models to find which one is more efficient at predicting the opponents move.

The following sequence of player moves were used to test the HMM(Hidden Markov Model), Lower order Markov chain and Higher order MMarkov chain.

> [!NOTE]
> I foolishly deleted the lower order Markov chain file so just trust me on this one. T-T

```
rock
paper
scissors
scissors
paper
rock
rock
scissors
paper
```

Definitely not the best test, but hey there's actually a test... :)

This was the result from the models: 
```
lower order Markov Chain: 25%

HMM(Hidden Markov Model): 12.50%

higher order Markov chain: 37.50%
```

So we learn that Markov chains are more efficient to predict player moves in RPS(Rock Paper Scissors), and HMM's are shit(at least when it comes RPS).
