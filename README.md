# Pre-Built Implementation of Bayesian Change-Detection in Time Series Model

#### @Zachary Rosen, 08/16/2023

The model written here is a simple change-detection model implemented in PyJAGs that allows for greater than two changes to a signal in time. This makes it useful for change-detection where one might expect a signal to be "bursty" or exhibit behavior where the inital signal change tapers off, or becomes stronger as time progresses.

Because the model is written in PyJAGS, it may not play nicely with some operating systems (like MacOS). In these instances, it may be preferable to download the package to a google colab notebook or amazon sagemaker instance. To do this, I recommend the following command-line code

```angular2html
!git clone https://github.com/zaqari/Bayesian-TimeSeries-Change-Detection.git
```

You will need to also install the pyjags package. If you do not install the package using setup.py, then you will need to run the following command in your script or in the command line

```angular2html
!pip3 install -U pyjags
```

Once the package has been installed, you can easily belt out models via the following syntax:

```
from BayesianChangeDetection import cdm

model = cdm(
    y = the_measured_values_for_your_problem
    time = time_for_each_measurement_or_else_none
    n_cat = optional_value_for_number_of_expected_time_changes
)
```

And you can pull the results for your model using

```
model.posterior
```
