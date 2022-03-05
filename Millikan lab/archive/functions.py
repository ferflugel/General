import pandas as pd

def get_terminal_velocity(y_positions):
    y_positions = [x for x in y_positions if x != '#NV']
    delta_y = [float(y_positions[i]) - float(y_positions[i - 1])
               for i in range(1, len(y_positions))]
    delta_y = moving_average(delta_y, 10)
    return max(delta_y)

# Note: moving average function from kite.com
def moving_average(y_velocity, window_size):
    numbers_series = pd.Series(y_velocity)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]
    return without_nans
