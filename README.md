Practical task
==============

# The fun part:
Now that everyone has contrubuted their code: we can play with the filters! I have implemented a small function that converts the modified data to a wav file again. In this repo you now find 3 different soundfiles created by applying different filters.
Feel free to add this repo as a remote and pull the changes and try it yourselfs!

```bash
git remote add upstream git@github.com:danielk333/live_freq_analysis.git
git fetch upstream master
git checkout master
git merge upstream/master
```

Also to keep working with this it is a good idea to have this as a reference:
[WaveFormat](http://soundfile.sapp.org/doc/WaveFormat/)

## The code: main.py
Open the file and look at the code, it loads some wav sound file, extracts the data, fourier transform it in a windowed fashion and plots a animation of the frequency content of the sound file as a function of time! Also open the sound file and listen to it (yes its me whistling :P).

And remember, if you find this task enjoyable, feel free to keep submitting merge requests for other features and we can build it into a great showcase example!

# The task:
1. Fork the repository
2. Clone it into your local computer
3. Create a branch with appropriate name
4. Choose one of the below tasks 1-4
5. If all tasks 1-4 are already taken, choose one of the bonus tasks
6. Write a issue in this repository that you will handle this task
7. Implement that task and submit a merge request

When tasks 1-3 are done and integrated:
Everyone pull the master branch from this repo (by adding a second remote in git) and implement task 5 locally

## There are 5 tasks to complete in this library:
Remember that you are not doing ALL tasks yourself, only task 5.

Note about the *filter* functions below: you can choose to implement so that they work on a single fourier transform (i.e. 1 set of frequency and amplitude) or a whole set of fourier transformes (like the sliding windowed fourier transforms done in the script), both are OK!

1. Implement a _frequency smoothing filter_, this can be done by using a running_mean with window N like

```python
def running_mean(x, N):
    cumsum = n.cumsum(n.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
```

For more info on this, look at [Moving average](https://en.wikipedia.org/wiki/Moving_average)

2. implement a _frequency band pass_, i.e. all frequencies outside f1 and f2 are set to 0
3. Implement a _frequency gaussian filter_, i.e. multiply all amplitudes with a gaussian evaluated at that frequency. The gaussian should have some arbitrary mean (f_mu) and standard deviation (f_std) in frequency space.
4. Change the windowed frequency extraction part of the script into a function and implement testing using pytest, suggested tests can be: checking that a simulated input sin-wave gets analysed to the correct frequency within some tolerance

```python
def test_freq_sin(x, N):
    T_s = 1e-6
    t = n.arange(0,1,T_s,dtype=n.float)
    f0 = 3000 #Hz

    wav_data = n.sin(n.pi*2.0*f0*t)

    freq_content = THE_FUNCTION_THAT_EXTRACTS_FREQUENCY_STUFF(wav_data, T_s=T_s, window=wav_data.size, overlap=0)

    assert n.abs(n.mean(freq_content)/(2,0*n.pi) - f0) < 100 
```
And to extend the test even further one could try inputting a linearly sliding frequency f0(t) and look that the function actually produces the correct linear curve.

5. Use the _frequency smoothing filter_, _frequency band pass_ and the scipy _load wav_ and _write wav_ functions to: load the *test.wav*, fourier transform, apply a or several filters, inverse transform the data, and save the data into a new wav file

## Bonus tasks

6. Add a peak amplitude plot feature (i.e. a line with the max amplitude for each frequency). This should either update in real time (i.e. to max SO FAR), but be pre-calculated or be just a constant
7. Extract the windowed calculation of the frequency spectrum into a function
8. Extract the plotting into a function
9. Out of the peak amplitude for every frequency, also plot the frequency that has the largest peak as a dot
10. Implement sphinx documentation
