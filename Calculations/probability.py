def calculate_probability(df):
    count = (df['Velocity [m/s]'] > ((-0.25*df['CumulativeMassInNet'])+1000)).sum()
    print(count)
    probability = count / len(df)

    return probability