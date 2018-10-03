

def ddc(N, base):
    if base == [8, 4, 2, 1]:

        ddc = int()
        for i in str(N):
            ddc *= 16
            ddc += int(i)

        return str(bin(ddc))[2:]

    else:

        ddc = str()

        for i in str(N):

            four = [0, 0, 0, 0]
            current_number = int(i)

            for j in range(len(base)):
                if current_number >= base[j]:
                    current_number -= base[j]
                    four[j] = 1

            for j in four:
                ddc += str(j)

        return ddc


print(ddc(851, [7, 4, 2, 1]))
