from .BTCSD import change_detection as cdm

NOTICE = """
ATTENTION: when using the model, it expects an input as a dictionary containing data following one of the structures described below:


Change-Detection Model Data Set-Up:
{
    'y': the count/continuous measurement variable to be predicted,
    'time': the time indicator for each measured variable,
    'n_cat': the number of expected times the signal changes
}


Null Model Data Set-Up:
{
    'y': the count/continuous measurement variable to be predicted
}

@Zachary Rosen, 08/16/2023
"""

print(NOTICE)
