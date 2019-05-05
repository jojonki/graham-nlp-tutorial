# Tutorial 9: Topic Model

[See graham's document.](http://www.phontron.com/slides/nlp-programming-ja-09-topic.pdf)

## Approximation by sampling
```
$ python sample.py
Result:
A: 0.500 (5005/10000)
B: 0.302 (3016/10000)
C: 0.198 (1979/10000)
```


## Gibbs sampling
```
$ python gibbs_sampling.py
Result:
P(mom,dag) = 0.550 (5503/10000)
P(mom,son) = 0.278 (2776/10000)
P(fat,dag) = 0.111 (1107/10000)
P(fat,son) = 0.061 (614/10000)
```
