def calculate_probability(df):
    count = (df['Kinetic Energy [kJ]'] >= ((-0.25*df['CumulativeMassInNet'])+1000)).sum()
    print(count, 'Netzbrüche')
    probability = count / len(df)

    return probability


def calculate_overall_death_probability(yearly_probability):
    direct_hit = 316.8/86400
    indirect_hit = 3792/86400
    probability = (direct_hit + indirect_hit) * 1.6 * yearly_probability

    return probability