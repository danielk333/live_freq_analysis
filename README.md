Practical task
==============

## The code: main.py
Open the file and look at the code, it loads some wav sound file, extracts the data, fourier transform it in a windowed fashion and plots a animation of the frequency content of the sound file as a function of time! Also open the sound file and listen to it (yes its me whistling :P).

# The task:
1. Fork the repository
2. Clone it into your local computer
3. Create a branch with apropriate name
4. Choose one of the below tasks 1-3
5. If all tasks 1-3 are already taken, choose one of the bonus tasks
6. Write a issue in this repository that you will handle this task
7. Implement that task and submit a merge request
When tasks 1-3 are done and integrated:
Everyone pull the master branch from this repo (by adding a second remote in git) and implement task 4 locally

## You have 4 tasks to complete in this library:
1. Implement a _frequency smoothing filter_, this can be done by using a running_mean with window N like

{% highlight python %}
def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
{% endhighlight %}

For more info on this, look at [Moving average](https://en.wikipedia.org/wiki/Moving_average)

2. implement a _frequency band pass_, i.e. all frequencies outside f1 and f2 are set to 0
3. Implement data read and a data write functions (using scipy wav) and replace the hardcoded data read by this function
4. Use the _frequency smoothing filter_ and _frequency band pass_ and load functions to: load the *test.wav*, fourier transform, smooth the data, bandpass the data at some frequency range, inverse transform the data, and save the data into a new wav file

## Bonus tasks

5. Add a peak amplitude plot feature (i.e. a line with the max amplitude for each frequency). This should either update in real time (i.e. to max SO FAR), but be pre-calculated or be just a constant
6. Extract the windowed calculation of the frequency spectrum into a function
7. Extract the plotting into a function
8. Out of the peak amplitude for every frequency, also plot the frequency that has the largest peak as a dot
