

def policz(plik):
    N=0
    L=-1
    with open(plik, 'r') as F:
        for line in F:
            L+=1
            ostatnie = line.strip().split(",")[-1]

            if ostatnie=="Unknown":
                N+=1
    print(f"{100-N} na {L} gatunkow zostalo odgadniete")
    print(f"To {100-round(N/L*100)}%")

if __name__=="__main__":
    policz("billboard_got100_2025-08-07.csv")
