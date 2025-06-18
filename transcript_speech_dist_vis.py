import os, sys
import numpy as np
import pandas as pd
from random import randrange
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

os.chdir(os.path.expanduser("/Users/zeynepmarasli/Downloads/Documents/Projects/Daylong_Analyses/Python_Code/"))
sys.path.append("/Users/zeynepmarasli/Downloads/Documents/Projects/Daylong_Analyses/Python_Code/")
from module_lib.daylongtranscript import*
#from daylongtranscript import*

# PROGRAM OBJECTIVE: obtain & visualize minute by minute word counts of a daylong audio file

def get_cumdistribution(wcount_distribution):
    #print(wcount_distribution)
    print(sum(wcount_distribution))
    cumdistribution = []
    cum_wcount = 0
    for interval_count in wcount_distribution:
        cum_wcount = cum_wcount + interval_count
        cumdistribution.append(cum_wcount)
    return cumdistribution

def main():
    # get distributions (x and y) for each transcript:
    #A1_distribution = get_distribution("Transcripts/Clean/All_Tiers/A787_001107_cleaned.txt")
    #x_A1 = list(range(1, len(A1_distribution)+1))
    #y_A1 = A1_distribution
    #print("Transcript A dist acquired\n")
    transcriptA1 = DaylongTranscript(fpath = "Transcripts/Clean/All_Tiers/A787_001107_cleaned.txt", fname = "A787_001107",isVanDam=False)
    A1_distribution = transcriptA1.speech_distribution
    x_A1 = list(range(1, len(A1_distribution)+1))
    y_A1 = A1_distribution
    
    transcriptA2 = DaylongTranscript(fpath = "Transcripts/Clean/All_Tiers/A787_001109_cleaned.txt", fname = "A787_001109",isVanDam=False)
    A2_distribution = transcriptA2.speech_distribution
    x_A2= list(range(1, len(A2_distribution)+1))
    y_A2 = A2_distribution

    transcriptA3 = DaylongTranscript(fpath = "Transcripts/Clean/All_Tiers/A787_001111_cleaned.txt", fname = "A787_001111",isVanDam=False)
    A3_distribution = transcriptA3.speech_distribution
    x_A3= list(range(1, len(A3_distribution)+1))
    y_A3 = A3_distribution

    transcriptB1 = DaylongTranscript(fpath = "Transcripts/Clean/All_Tiers/B895_010002_cleaned.txt", fname = "B895_010002")
    B1_distribution = transcriptB1.speech_distribution
    x_B1= list(range(1, len(B1_distribution)+1))
    y_B1 = B1_distribution

    transcriptB2 = DaylongTranscript(fpath = "Transcripts/Clean/All_Tiers/B895_010004_cleaned.txt", fname = "B895_010004")
    B2_distribution = transcriptB2.speech_distribution
    x_B2 = list(range(1, len(B2_distribution)+1))
    y_B2 = B2_distribution

    transcriptC = DaylongTranscript(fpath = "Transcripts/Clean/XDS_only/BN32_clean.txt", fname = "BN32", isVanDam=True)
    C_distribution = transcriptC.speech_distribution
    x_C = list(range(1, len(C_distribution)+1))
    y_C = C_distribution

    #PLOT
    #plt.scatter(x_A1, y_A1)
    #plt.scatter(x_A2, y_A2)
    #plt.scatter(x_B1,y_B1)
    #plt.scatter(x_B2,y_B2)
    #xticks = [0,100,200,300,400,500,600,700, 800]
    
    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6,1, sharex = True, figsize = (12,12))
    fig.suptitle("Word Count Distributions of Transcripts", y = 0.98, fontweight = "bold")
    
    ax1.bar(x_A1, y_A1)
    ax1.set_ylabel("A1", fontweight = "bold", size=15)
    
    ax2.bar(x_A2, y_A2)
    ax2.set_ylabel("A2", fontweight = "bold", size=15)
    
    ax3.bar(x_A3, y_A3)
    ax3.set_ylabel("A3", fontweight = "bold", size=15)

    ax4.bar(x_B1,y_B1)
    ax4.set_ylabel("B1", fontweight = "bold", size=15)

    ax5.bar(x_B2,y_B2) 
    ax5.set_ylabel("B2", fontweight = "bold", size=15)

    ax6.bar(x_C,y_C) 
    ax6.set_ylabel("C", fontweight = "bold", size=15)
    ax6.set_xlabel("time (minutes)", size=12)

    plt.tight_layout()
    plt.xticks(ticks = [0,100,200,300,400,500,600,700, 800], size=12)
    plt.savefig('wcdist_ALL.png')
    plt.show()
    

    """ plt.title('Transcript', fontsize = 20)
    plt.xticks(ticks = [0,100,200,300,400,500,600,700, 800], rotation = '45', fontsize = 14)
    
    plt.xlabel('time interval in daylong recording (min)', fontsize = 16)
    plt.ylabel('word count', fontsize = 16)
    
    plt.yticks(fontsize = 16)
    plt.figure(figsize = (20,10)) 
    plt.savefig('wcdist_ALL_CogSci.png') 
    """
    #plt.show()

def mini_main():
    transcriptC = DaylongTranscript(fpath = "Transcripts/Clean/XDS_only/BN32_clean.txt", fname = "BN32", isVanDam=True)
    transcriptC.describe(visualize_speech=True)

#mini_main()
main()
