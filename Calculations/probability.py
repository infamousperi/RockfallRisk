def calculate_probability(df):
    count = (df['Velocity [m/s]'] > ((-0.25*df['CumulativeMassInNet'])+1000)).sum()
    print(count)
    probability = count / len(df)

    return probability


def calculate_yearly_probability(total_probability, period):
    probability = 1 - (1 - total_probability)**(1/period)

    return probability


def calculate_overall_death_probability(yearly_probability):
    probability = (0.367 + 4.389) * 1.6 * yearly_probability

    return probability