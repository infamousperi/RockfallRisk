def calculate_probability(df):
    count = (df['Kinetic Energy [kJ]'] >= ((-0.25*df['CumulativeMassInNet'])+1000)).sum()
    print(count, 'Steinschläge')
    probability = count / len(df)

    return probability


def calculate_overall_death_probability(yearly_probability):
    probability = (0.000367 + 0.004389) * 1.6 * yearly_probability

    return probability