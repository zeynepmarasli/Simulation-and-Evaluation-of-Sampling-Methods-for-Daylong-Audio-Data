import sys, operator, os, string, re, random, math
from random import randrange
import statistics
import matplotlib.pyplot as plt

class Utterance:
    def __init__(self, utt, isVanDam = False): #utt is TOKENIZED // split from TAB 
        """
        Utterance class
        - utt: TOKENIZED line; ex: FA1	good morning	good morning.	25480	27970	T	None   (if isVanDam is FALSE)
        - isVanDam: (bool)
        - xds: T
        - CHIsubtiers: None
        - speaker: FA1
        - cleaned_speech: good morning
        - raw_speech: good morning.
        - start_ts: 25480
        - end_ts: 27970
        """
        self.utt = utt #TOKENIZED line
        #print(self.utt)
        self.isVanDam = isVanDam
        self.speaker = self.set_speaker()
        self.CHIsubtiers = self.set_CHIsubtiers()
        self.xds = self.set_xds()
        self.cleaned_speech, self.raw_speech = self.set_speech()
        self.start_ts = self.set_start_ts()
        self.end_ts = self.set_end_ts()

    def set_speaker(self):
        """
        - returns speaker label
        """
        if self.isVanDam is False: return self.utt[0]
        else:
            sp = self.utt[0]
            speaker_codes = {'MOT': 'FA1', 'FAT': 'MA1', 'SIS': 'FC1', 'CHI': 'CHI'}
            return speaker_codes[sp]
    
    def set_speech(self): 
        """
        - sets both cleaned and raw speech as tokenized list 
        """
        cleaned_speech = []
        raw_speech = []
        if self.isVanDam: 
            cleaned_speech = self.utt[1:-2] # last two tokens are timstamp and xds; DEBUG 
            raw_speech = self.utt[1:-2] # the same thing from the input txt file
        else:
            if self.get_speaker() == "CHI":
                if self.utt[2] == "0.":                  
                    cleaned_speech = []
                    raw_speech = self.utt[2].split() 
            else:
                cleaned_speech = self.utt[1].split() 
                raw_speech = self.utt[2].split()
        return cleaned_speech, raw_speech
    
    def set_start_ts(self): 
        '''
        - returns start timestamp (ms) of utterance
        '''
        if self.isVanDam: return int(self.get_ts()[0])
        else: return int(self.utt[3])
        
    def set_end_ts(self):
        """
        - return end timestamp (ms) of utterance
        """
        if self.isVanDam: return int(self.get_ts()[-1])
        else: 
            return int(self.utt[4])

    def get_ts(self):   
        """
        - returns timestamps as list
        - TO DO: remove if not needed 
        """
        if self.isVanDam: 
            timestamps = self.utt[-1]
            timestamps = timestamps.replace("\n", "")
            return(timestamps.split("_"))
        else:
            return [self.get_start_ts(), self.get_end_ts()]
    
    def set_xds(self):
        """
        - returns xds label
        """
        if self.isVanDam: 
            return re.sub(r'\[|\]', "", self.utt[-2]) # TODO: DEBUG IF NEEDED 
        else:
            return self.utt[-2] # second to last element is xds label 
            
    def set_CHIsubtiers(self):
        """
        - returns CHI subtiers if they are present
        - present CHI subtiers are returned in this format: "['N', '0', '0']"
        """
        if self.isVanDam is False and self.get_speaker() == "CHI": 
            subtiers = self.utt[-1] 
        else: return None 
        
    def view_utt(self):
        """
        - prints entire transcript line 
        """
        print(self.utt)

    def describe_utt(self):
        '''
        - prints out all components of utterance object
        '''
        self.view_utt()
        print("speaker: ", self.get_speaker())
        print("raw speech: ", self.get_speech(cleaned=False))
        print("cleaned speech: ", self.get_speech(cleaned=True))
        print("start & stop timestamps (ms): ", self.get_ts())
        print("xds: ", self.get_xds())
        print("subtiers: ", self.get_CHIsubtiers())
        print()

    # getter methods
    def get_speaker(self):
        return self.speaker
    def get_speech(self, as_tokens = True, cleaned = True):
        if as_tokens: 
            if cleaned: return self.cleaned_speech
            else: return self.raw_speech
        else: 
            if cleaned: return " ".join(self.cleaned_speech)
            else: return " ".join(self.raw_speech)
    def get_start_ts(self):
        return self.start_ts
    def get_end_ts(self):
        return self.end_ts
    def get_xds(self):
        return self.xds
    def get_CHIsubtiers(self):
        return self.CHIsubtiers
    
class DaylongTranscript:
    def __init__(self, fpath = "", fname = "", silence_length = 30, isVanDam = False):
        """
        DaylongTranscript class 
        - fname: (str) name of transcript file
        - isVanDam: (bool) if transcript is VanDam BN32
        - audio_length: (int) length of audio in ms
        - daylong_word_count: (int) total transcribed word count
        - silence_intervals: (list) list of pairs of timestamps corresponding to silence intervals (>30 min)
        - total_silence: (int) summed silences in ms 
        - speech_distribution: (list) word count distribution/minute of transcript
        """
        self.fname = fname 
        self.fpath = fpath # filepath to original text transcript
        self.isVanDam = isVanDam
        self.utterances = self.make_utterances() #each tokenized line is an Utterance object 
        self.audio_length = self.set_audio_length() #in ms
        self.daylong_word_count = self.set_total_word_count()
        self.silence_intervals, self.total_silence = self.set_silence_intervals(silence_length) # list of pairs of timestamps 
        self.speech_distribution = self.set_speech_distribution()    
      
    def make_utterances(self):
        """
        - takes in CLEANED transcript line by line and tokenizes accroding to format: [speaker, utterance, timestamp, xds, subtier(if CHI), subtier(ifCHI)]
        - instantiates Utterance objects for each utt line 
        """
        inFile = self.fpath
        f = open(inFile, "r")
        all_tokens = []
        for line in f:
            line = line.replace("\x15", "")
            line = line.replace("•%sndA787_001107_", "")
            line = line.replace("•%sndA787_001109_", "")
            line = line.replace("•", "")
            line = line.replace("  ", " ")
            line = line.replace(" \n", "")
            if self.isVanDam is False: tokens = line.split(sep = "\t")
            else: tokens = line.split(" ")
            if tokens[0] == 'SIL': 
                continue #skip annotation that indicates Silences
            else: 
                all_tokens.append(Utterance(tokens, self.isVanDam))

        return all_tokens

    def set_audio_length(self):
        """
        - returns the end timestamp of final utterance, indicating length of recording (in ms)
        """
        last_timestamp = self.utterances[-1].get_end_ts()
        return last_timestamp 
    
    def set_total_word_count(self, count_unique_only = False):
        """
        - returns word count of transcript; uses cleaned utterances to count speech 
        """
        wc = 0 
        unique_words = []
        #words = words + line[1:-1]
        for line in self.utterances:
            words = line.get_speech()
            if count_unique_only is True:
                for word in words:
                    if word not in unique_words:
                        wc = wc + 1
                        unique_words.append(word)

            else: wc = wc + len(words)
        return wc

    def set_silence_intervals(self, silence_length = 30):  
        """
        - identifies intervals of silence in transcript where no speech has been transcribd for 30 minutes or more 
        - returns: list of pairs of timestamps and total summed silence intervals (ms)
        """
        silences = []
        threshold = self.convert_to_ms(silence_length)  # 30 minutes in ms
        for index in range(len(self.utterances) -1):
            utt1 = self.utterances[index]
            utt2 = self.utterances[index+1]
            diff = utt2.get_start_ts() - utt1.get_end_ts() 
            if diff >= threshold: 
                #print("SILENCE")
                #print("\t", utt1.utt)
                #print("\t", utt2.utt)
                #print("\t", diff)
                silences.append([utt1.get_end_ts(), utt2.get_start_ts()])
        
        total_silence = 0
        for pair in silences:
            total_silence = total_silence + (pair[1] - pair[0])

        return silences, total_silence  
         
    def view_transcript(self):
        """
        - prints out transcript
        """
        for line in self.utterances: line.view_utt() 
        return 

    def convert_to_min(self, value): 
        """
        - converts a time in ms to minutes 
        """
        value = value / (60 *1000)
        return round(value, 3) 
    
    def convert_to_ms(self, value):
        """
        - converts minute value to milliseconds
        """
        return value * 60 * 1000 

    def describe_silences(self):
        """
        - prints out each silence interval timestamps and total silent and speaking intervals of transcript 
        """
        total_silence = 0
        for pair in self.silence_intervals:
            total_silence = total_silence + (pair[1] - pair[0])
        print("\tIntervals of silence:", self.silence_intervals)
        print("\t\t\t", total_silence, "ms //", self.convert_to_min(total_silence), "min total silent intervals")
        print("\t\t\t", self.convert_to_min(self.audio_length - total_silence), "min total speaking interval")

    def describe(self, visualize_speech = False):
        """
        - descriptives of transcript
        - visualize_speech: (bool) produces figure of speech distribution 
        """
        print("Transcript: ", self.fname, "---")
        print("\tAudio Length: ", self.audio_length, "ms // ", self.convert_to_min(self.audio_length), " min")
        print("\tTotal Word Count: ", self.daylong_word_count)
        self.describe_silences()
        if visualize_speech is True: self.visualize_speech_distribution()
   
    def find_lines(self, min):
        """
        - helper function called in get_wc_distribution()
        - input: tokenized transcript; audio time (in minutes) to find all lines in
        - returns: returns lines within specified minute
        - STARTS with utterances that begin fully within specified minute interval and INCLUDES utterances that begins WITHIN interval but ENDS outside
        - REALLY, I'm just checking if utterance STARTS within a specified minute interval, I don't care if it ends outside (shifts word/min a bit, but all words should be accounted for in one interval or the other)
            for obtaining speech distribution 
        """
        onemin_ms = self.convert_to_ms(1)
        minute_interval = self.convert_to_ms(min)
        lines = []
        for utt in self.utterances:
            utt_start = utt.get_start_ts()
            if (minute_interval - onemin_ms) < utt_start <= minute_interval:
                lines.append(utt)
        return lines
  
    def get_wcount(self, lines, return_words = False):
        """
        - helper function called in set_wc_distribution()
        - input: start & stop index of transcript lines (exclusive!!!); ex. if start_index = 1 and stop_index = 4 then will iterate through indeces 1,2,3 & NOT 4
        - returns: summed word count from lines (if return_words is False) OR actual words/speech from lines (if return_words is True)
        - for obtaining speech distribution 
        """
        wcount = 0
        words = ""
        if return_words is True: #if TRUE
            for line in lines:
                words = words + " "  + line.get_speech(as_tokens = False)
            return words
        else:
            for line in lines:
                wcount = wcount + (len(line.get_speech()))
            return wcount

    def set_speech_distribution(self, return_words = False):
        '''
        - function call for obtaining word count/minute distribution of transcript 
        - if return_words is False: return list of word COUNTS per minute 
        - if return_words is True: returns list of words per minute interval 
        '''
        audio_length_min = self.convert_to_min(self.audio_length)
        wc_dist = [] # will either hold word counts OR actual words per minute interval 
        for minute in range(1,math.ceil(audio_length_min) + 1):
            lines = self.find_lines(minute)
            wc_dist.append(self.get_wcount(lines, return_words=return_words))
        return wc_dist

    def get_feature_distribution(self, feature_dict = {}):
        """
        - function call for obtaining distribution/minute of a specific feature 
        -  valid feature types include: speaker, xds, utterance_annotation, select_word
        - debug??
        """
        feature_type = list(feature_dict.keys())[0]
        feature = list(feature_dict.values())[0]
        occurrences_per_minute = []
        audio_length_min = self.convert_to_min(self.audio_length)
        for minute in range(1,math.ceil(audio_length_min) + 1):
            lines = self.find_lines(minute)
            occurrences_in_min = 0
            for line in lines:
                if feature_type == "speaker" or feature_type == "xds": # COUNT WORDS 
                    if line.get_speaker() == feature or line.get_xds() == feature: 
                        occurrences_in_min = occurrences_in_min + len(line.get_speech(as_tokens = True))
                    #line.view_utt()
                elif feature_type == "utterance_annotation": # COUNT UTTERANCES WITH OCCURRENCES 
                    raw_speech = line.get_speech(cleaned = False, as_tokens = False)  
                    if feature in raw_speech: occurrences_in_min = occurrences_in_min + 1
                else: # feature is select word 
                    line_occurences = line.get_speech(as_tokens = True).count(feature)
                    """ if line_occurences != 0: 
                        print("FOUND IT")
                        line.view_utt() 
                        print("in line: ", line_occurences, " cum count: ", sum(occurrences_per_minute) + line_occurences)
                        #continue  """
                    occurrences_in_min = occurrences_in_min + line_occurences
                    """ if feature in line.get_speech():
                        #line.view_utt()
                        occurrences = occurrences + 1  """
            occurrences_per_minute.append(occurrences_in_min)
        return occurrences_per_minute
    
    def feature_count(self, feature_dict = {}):
        '''
        - valid feature types include: speaker, xds, utterance_annotation, select_word
        - function call for getting daylong count of a specific feature 
        '''
        fcount = 0 
        feature_type = list(feature_dict.keys())[0]
        feature = list(feature_dict.values())[0]
        if feature_type == "speaker" or feature_type == "xds":
            if feature_type == "speaker" and feature == "CHI": # FOR CHI, COUNT NUMBER OF UTTERANCES (VOCALIZATIONS)
                for utt in self.utterances: 
                    if utt.get_speaker() == feature: fcount = fcount + 1 
            else: 
                for utt in self.utterances: # COUNT NUMBER OF WORDS
                    if utt.get_speaker() == feature or utt.get_xds() == feature: fcount = fcount + len(utt.get_speech())
        elif feature_type == "utterance_annotation": # COUNT NUMBER OF UTTERANCES WITH FEATURE
            for utt in self.utterances:
                raw_utt = utt.get_speech(as_tokens = False, cleaned = False)
                if feature in raw_utt: fcount = fcount + 1
        elif feature_type == "select_word": # SELECT_WORD - COUNT NUMBER OF OCCURRENCES 
            cleaned_transcript = self.get_speech(return_tokens = True, return_cleaned = True)
            fcount = cleaned_transcript.count(feature)
        else: raise ValueError(f"Cannnot count for {feature_type} ({feature}) feature")

        return fcount

    def visualize_speech_distribution(self):
        """
        - plots speech distribution 
        """
        x = list(range(1, len(self.speech_distribution)+1))
        y = self.speech_distribution
        plt.bar(x, y)
        plt.xticks(rotation = 45, fontsize = 14)
        plt.xlabel('time interval in daylong recording (min)', fontsize = 16)
        plt.ylabel('word count', fontsize = 16)
        plt.title("Transcript", fontsize=20)
        plt.yticks(fontsize = 16)
        plt.show()

    def get_speech(self, return_tokens = False, return_cleaned = True):
        '''
        - returns as a string (if return_tokens is False, otherwise returns as string of tokens), ALL the transcribed speech from ALL utterances
        - if return_cleaned is False, uses raw utterance
        '''
        speech = ""
        for line in self.utterances:
            speech = speech + " " + line.get_speech(as_tokens = False, cleaned = return_cleaned)
        
        if return_tokens: return speech.split()
        else: return speech

    def get_utterances(self):
        return self.utterances
    def get_audio_length(self):
        return self.audio_length
    def get_total_word_count(self, count_unique_only = False):
        if count_unique_only: return self.set_total_word_count(count_unique_only=count_unique_only)
        else: return self.daylong_word_count
    def get_silence_intervals(self):
        return self.silence_intervals, self.total_silence
    def get_speech_distribution(self, return_words = False):
        if return_words: return self.set_speech_distribution(return_words = return_words)
        else: return self.speech_distribution
    
def main():
    print("loaded")

main()
    


