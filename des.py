from random import randint
from time import time_ns as now

STATS_PRE = 3
PRECISION = 7
MAX_POWER = 10

def timed_rv(f):
    def wrapper(*args, **kwargs):
        start = now()
        return_value = f(*args, **kwargs)
        elapsed = (now() - start) / 1000000
        if (elapsed > 1000) :
            print(f"résultat obtenu en {round(elapsed / 1000, STATS_PRE)} secondes.")
        else:
            print(f"résultat obtenu en {round(elapsed, STATS_PRE)} millisecondes.")
        return return_value
    return wrapper

###########################                                                                                                            

@timed_rv
def iterate(precision: int, x: int, precedent: float) -> float:
    resultats: list[int] = [0] * 6
    for _ in range(10 ** x):
        resultats[randint(0,5)] += 1
    r: list[int] = [0] * 6
    for i in range(len(r)):
        r[i] = round(float(resultats[i]) / sum(resultats) * 100, precision)
    ecartmax: float = round(max(r) - min(r), precision)
    pente: int = round(precedent / ecartmax, STATS_PRE)
    print(f"% de chance d'obtenir chaque dé pour {10 ** x} (10^{x}) lancers :")
    print(f"\t{r}")
    print(f"soit près de 1/6 ± {round(ecartmax / 200, precision)}", end = "" if precedent != 0 else "\n")
    if (precedent != 0):
          print(f"\t({pente} fois moins qu'au tour précédent)")
    return ecartmax

def main(prec: int, maxpow: int) -> None:
    rv: float = 0
    for x in range(0, maxpow):
        rv = iterate(prec, x, rv)
        print(end = "" if x == maxpow - 1 else "\n")

###########################                                                                                                            

from os import name as osName
from signal import signal as bindSignal, SIGINT, SIGTERM

def getContext(frame: str) -> str:
    return   frame.f_code.co_filename.split("\\")[-1] + ":" + str(frame.f_lineno) if osName == 'nt' \
        else frame.f_code.co_filename.split("/")[-1]  + ":" + str(frame.f_lineno)

def CtrlDHandler(signal_received: int, frame: str) -> None:
    print(f"\n! SIGTERM ({signal_received}) interruption à {getContext(frame)} !", flush = True)
    exit(0)
