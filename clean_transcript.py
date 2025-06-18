# CLEAN_TRANSCRIPT.PY 
# cleans transcript in prep for daylong sampling (daylongtranscript.py and randomsampler.py)
    # removes comments
    # removes non-alphabetic characters; extra linguistic annotations 
    # removes vcm, lex, mwu tiers for CHI 
    # add xds annotation to end of corresponding speaker tier
    # for ex: *MOT:	let's change your diaper . [+ id] 59836_66554 will be cleaned as:  MOT let's change your diaper 59836_66554 [+ id]
    # or *FA1:	<good morning.> [!=sings] •%snd:"A787_001109"_27329_29409• will be: FA1 good morning 27329_29409 T

import sys, operator, os, string, re, random, math


skip_chars = ["@", "VCM", "LEX", "MWU"]
punct = r'\*|:|\?|\.|,|\"'
things_in_brackets = r'[\(\[\<\{].*?[\)\<\}\]]'

def clean_fausey(input_file, output_file):
    file_input = open(input_file, "r")
    file_output = open(output_file, "w")
    transcript = file_input.readlines()
    transcript_cleaned = []
    skip_chars = ["0", "@", "VCM", "LEX", "MWU", "VC0M"]
    punct = r'\*|:|\?|\.|,|\|!|<|>|{|}|\"|-'
    things_in_brackets = r'[\(\[].*?[\)\]]'
    for line in transcript:
        if line[0] in skip_chars: continue
        else: 
            if line[0] == "%": 
                line = re.sub(r'\n+', "", line)
                line = re.sub(r'\.', "", line)
                transcript_cleaned[-1] = transcript_cleaned[-1] + " " + line[-1] # add xds to end of speaker tier line (previous line)
            elif line[0] == "*":
                line = re.sub(punct, "", line)
                line = re.sub(things_in_brackets, "", line)
                line = re.sub(r'!', "", line)
                line = line.replace("•", "")
                line = line.replace("\x15", "")
                line = line.replace("%sndA787_001107_", "")
                line = line.replace("%sndA787_001109_", "")
                line = line.replace("%sndB895_010004_", "")
                line = re.sub("xxx", "", line)
                line = re.sub("&=[a-zA-z]+", "", line)
                line = re.sub("  +", " ", line)
                line = re.sub(r'\n+', "", line)
                transcript_cleaned.append(line)

    # write to output file 
    count = 0
    for index, line in enumerate(transcript_cleaned): 
        tokens = line.split()
        if tokens[0] != "CHI" and tokens[-1].isalpha() is False:
            xds_prev = transcript_cleaned[index-1].split()[-1] # get xds from previous line 
            line = line + " " + xds_prev
        if len(tokens) <= 3 or tokens[1] in skip_chars: pass
        else:
            #print(line) 
            file_output.write(line + "\n")
    return 



def clean_BN32(input_file, output_file):
    file_input = open(input_file, "r")
    file_output = open(output_file, "w")
    transcript = file_input.readlines()
    raw_lines = []
    transcript_cleaned = []
    skip_chars = ["@", "VCM", "LEX", "MWU"]
    punct = r'\*|:|\?|\.|,|\|!|<|>|{|}|\+|\"'
    things_in_brackets = r'[\(\[].*?[\)\]]'
    
    for line in transcript:
        if line[0] in skip_chars: continue 
        else: 
            line = re.sub(r'\n+', "", line) 
            if line[0] == "*": 
                raw_lines.append(line)
            elif line[0] != "*": 
                raw_lines[-1] = raw_lines[-1] + " " + line
            
    for line in raw_lines:
        bracketed = re.findall(things_in_brackets, line)
        for b in bracketed: 
            if "+" not in b: line = line.replace(b, "") # remove all bracketed items except direction
            else: 
                b_new = b.replace(" ", "")
                line = line.replace(b, b_new) #remove whitespace in direction marker (for easier tokenizing later on)
        line=re.sub("\&=[a-z]+", "", line)
        line = re.sub("xxx", "", line)
        line = re.sub(punct, "", line)
        line = re.sub(r'!', "", line)
        transcript_cleaned.append(line)

    # write to output file 
    for line in transcript_cleaned: 
        tokens = line.split()
        if len(tokens) <= 3 or tokens[1] == '0': pass
        else: file_output.write(line + "\n")
    return   


# for cleaning A787 files 
""" A787_1107 = "A787_1107.txt"
A787_1107_output = "A787_1107_clean.txt"
#clean_A787(A787_1107, A787_1107_output)

A787_1009 = "A787_1009.txt"
A787_1009_output = "A787_1009_clean2.txt"
clean_A787(A787_1009, A787_1009_output)
 """

""" BN32 = "BN32_010007.txt"
BN32_output = "BN32_clean.txt"
clean_BN32(BN32, BN32_output) """

B895_01002 = "B895_010004_KMK_edits.cha"
B895_01002_output = "B895_010004_KMK_clean.txt"
clean_fausey(B895_01002, B895_01002_output)