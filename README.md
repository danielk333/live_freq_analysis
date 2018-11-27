Practical task
==============

## The code: main.py
Open the file and look at the code, it loads some wav sound file, extracts the data, fourier transform it in a windowed fashion and plots a animation of the frequency content of the sound file as a function of time! Also open the sound file and listen to it (yes its me whistling :P).

# The task:
1. Fork the repository
2. Clone it into your local computer
3. Create a branch with apropriate name
4. Choose one of the below tasks 1-4
5. If all tasks 1-4 are already taken, choose one of the bonus tasks
6. Write a issue in this repository that you will handle this task
7. Implement that task and submit a merge request

When tasks 1-3 are done and integrated:
Everyone pull the master branch from this repo (by adding a second remote in git) and implement task 5 locally

## You have 5 tasks to complete in this library:
1. Implement a _frequency smoothing filter_, this can be done by using a running_mean with window N like

```python
def running_mean(x, N):
    cumsum = n.cumsum(n.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
```

For more info on this, look at [Moving average](https://en.wikipedia.org/wiki/Moving_average)

2. implement a _frequency band pass_, i.e. all frequencies outside f1 and f2 are set to 0
3. Implement a _frequency gaussian filter_, i.e. multiply all values with a gausian with some mean (f_mu) and standard deviation (f_std) in frequency space
4. Change the windowed frequency extraction part of the script into a function and implement testing using pytest, suggested tests can be:

```python
def test_freq_sin(x, N):
    t = n.linspace(0,1,num=10000,dtype=n.float)
    f0 = 3000 %Hz

    wav_data = n.sin(n.pi*2.0*f0*t)

    freq_content = THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(...)

    assert n.abs(freq_content/(2,0*n.pi) - f0) < 100 
```
And to extend the test even further one could try inputting a linearly sliding frequency f0(t) and look that it actually reporuces the correct curve

5. Use the _frequency smoothing filter_ and _frequency band pass_ and load functions to: load the *test.wav*, fourier transform, smooth the data, bandpass the data at some frequency range, inverse transform the data, and save the data into a new wav file

## Bonus tasks

6. Add a peak amplitude plot feature (i.e. a line with the max amplitude for each frequency). This should either update in real time (i.e. to max SO FAR), but be pre-calculated or be just a constant
7. Extract the windowed calculation of the frequency spectrum into a function
8. Extract the plotting into a function
9. Out of the peak amplitude for every frequency, also plot the frequency that has the largest peak as a dot
10. Implement sphinx documentation