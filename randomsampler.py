import sys, operator, os, string, re, random, math, bisect
import numpy as np
import pandas as pd 
from random import randrange
import statistics
import matplotlib.pyplot as plt
import plotly.express as px
os.chdir(os.path.expanduser("/Users/zeynepmarasli/Downloads/Documents/Projects/Daylong_Analyses/Python_Code/"))
sys.path.append("/Users/zeynepmarasli/Downloads/Documents/Projects/Daylong_Analyses/Python_Code/")
from module_lib.daylongtranscript import*

class Sampler():
    def __init__(self, transcript, sampling_interval = .5, total_sampled_time = None, prop_tts = None, simulations = 100, sampling_method = 4, feature_type = "word count", feature = None):
        if isinstance(transcript, DaylongTranscript): self.transcript = transcript
        else: raise TypeError("transcript must be of DaylongTranscript type")
        self.sampling_interval = self.convert_to_ms(sampling_interval) ### length of sampling interval in ms 
        self.prop_tss = prop_tts  
        self.total_sampled_time = self.set_total_sampled_time(total_sampled_time, prop_tts)
        self.simulations = simulations 
        self.num_intervals = int(self.total_sampled_time / self.sampling_interval)
        self.daylong_estimates = [] # will update with each simulation iteration (default 100 times)
        self.sampled_features = [] # keeps track of # of words/feature occurrences sampled; will update with each simulation iteration (default 100 times)
        self.sampling_method = self.check_sampling_method(sampling_method)
        self.valid_features = ["word count", "speaker", "select_word", "xds", "utterance_annotation"]
        self.feature_type, self.feature = self.set_feature(feature_type, feature)  #feature_type = index of valid feature list; feature = actual key to look for in transcript 
        self.daylong_feature_count = self.get_daylong_count() # obtains true daylong count of desired feature 
        
    def set_total_sampled_time(self, total_sampled_time, prop_tts):
        """ if proportion total sampled time indicated, then calculates raw total sampled time amount (ms) """
        if prop_tts is None:
            return self.convert_to_ms(total_sampled_time) 
        elif total_sampled_time is None:
            total_time = self.transcript.get_audio_length() 
            #total_valid_sampling_portions = total_time - self.transcript.total_silence # portions of transcript we DO sample from (disregarding silences > 30 min)
            tts = prop_tts * total_time
            #tts = prop_tts * total_valid_sampling_portions
            return tts 
        
    def check_sampling_method(self, sampling_method):
        # valid sampling method parameters: whole integer 1 through 4 
            # 1: "conservative" sampling 
            # 2: "sample overlapping utterance"
            # 3: "sample overlapping + following silence"
            # 4: "sampling ~half overlapping speech"
        if isinstance(sampling_method, int) is False: raise ValueError("Invalid sampling method; must be an integer 1 through 4")
        if sampling_method < 1 or sampling_method > 4: raise ValueError("Invalid sampling method; must be an integer 1 through 4")
        return sampling_method 

    def set_feature(self, feature_type, feature):
        # valid linguistic features to estimate for:
            # 0 "word count": daylong word count; does not require extra specifier in feature parameter 
            # 1 "speaker": speech from a specific speaker; MUST specify which speaker in feature parameter
            # 2 "select word": occurences of specific word; MUST specifcy which word in feature parameter
            # 3 "xds": speech directed; MUST specify xds tag in feature parameter
            # 4 "utterance annotation": will count (raw) UTTERANCEs which contains an utterance (ex. a question mark ); MUST specify whcih annoation in feature parameter
        if feature_type not in self.valid_features:  
            raise ValueError("Invalid feature; valid arguments are:", self.valid_features)
        else: 
            feature_type_ind = self.valid_features.index(feature_type) 

        if feature_type_ind == 0 and feature is not None:
            raise TypeError("Specified unncessary feature argument for word count feature type")
        elif 1 <= feature_type_ind <= 4 and feature is None:
            raise TypeError("Missing required positional argument: feature")      
        else:
            return feature_type, feature 

    def get_daylong_count(self):
        # ["word count", "speaker", "select_word", "xds", "utterance_annotation"]
        '''
            if self.feature_type == 0: return self.transcript.get_total_word_count() # if estimating daylong wc, just return total wc from object 
            dc = 0
            if self.feature_type == 1: # speaker; FA1, MOT , CHI, etc  
                for line in self.transcript.utterances:
                    if line.get_speaker() == self.feature: dc = dc + len(line.get_speech()) 
                return dc 
            elif self.feature_type == 2: # select word
                for line in self.transcript.utterances: dc = dc + line.get_speech().count(self.feature)
                return dc 
            elif self.feature_type == 3: # xds
                for line in self.transcript.utterances:
                    if line.get_xds() == self.feature:
                        l = line.get_speech()
                        print(l, " ", len(l)) 
                        dc = dc + len(line.get_speech())
                return dc
            '''
        if self.feature_type == "word count": return self.transcript.daylong_word_count
        else:
            f_dict = {self.feature_type: self.feature}
            return self.transcript.feature_count(feature_dict = f_dict)

    # def sample(): sampler method that's called by the user
    def sample(self, see_final_stats = False, see_sub_stats = False, export = True, sample_non_overlapping = False):
        self.daylong_estimates = []
        self.sampled_features = [] 
        if self.sampling_method == 1:
            pass
        elif self.sampling_method == 2:
            pass
        elif self.sampling_method == 3:
            pass
        elif self.sampling_method == 4:
            self.sampler_method_4(see_final_stats, see_sub_stats, export, sample_non_overlapping)
        else:
            raise ValueError("Invalid method value; must be an integer 1 through 4")
        return 

    # sampler_method_4(): samples ~half of the overlapping utterances 
    def sampler_method_4(self, see_final_stats = False, see_sub_stats = False, export = True, sample_non_overlapping = False):
        print_stats = "*{0:<3d} {1:11.0f} {2:12d} / {3:5.3f} {4:17d} / {5:5.3f} {6:14.1f} / {7:5.3f} {8:11d}"
        for simulation in range(self.simulations):
            #print("Simulation: ", simulation + 1)
            if see_sub_stats is True: print("{0:12s} {1:15s} {2:25s} {3:20s} {4:20s} {5:20s}".format("Des Start", "Des Stop", "SpTs per iteration", "Total SPTs", "Total ATS", "FC per iteration"))
            sampled_fc = 0 # sampled feature count 
            audio_time_sampled = 0 # AUDIO time sampled across all iterations of one simulation
            speech_time_sampled = 0 # SPEECH time sampled across all iterations of one simulation (sum of utterance timestamps)
            if sample_non_overlapping: 
                #print("sampling non-overlapping intervals")
                random_times = self.generate_random_times_nonoverlapping()
            else:
                #print("sampling with overlapping intervals")
                random_times = self.generate_random_times()

            for rt in random_times:
                start_index, stop_index, first_overlapping, last_overlapping = self.find_interval_method4(rt) 
                if start_index is None and stop_index is None: # no corresponding utterances within generated interval found 
                    sampled_fc = sampled_fc + 0 # because no words in corresponding utterance 
                    speech_time_sampled = speech_time_sampled + 0 #because no corresponding utterances 
                    audio_time_sampled = audio_time_sampled + self.sampling_interval 
                    if see_sub_stats is True: 
                        print(print_stats.format(rt, rt + self.sampling_interval, 0 , 0, speech_time_sampled, self.convert_to_min(speech_time_sampled),
                            audio_time_sampled, self.convert_to_min(audio_time_sampled), 0 ) )
                        print(" --> No corresponding timestamps within interval")
                else:
                    utterances = self.transcript.utterances[start_index:stop_index+1]
                    fc = self.getfcount(utterances, first_overlapping, last_overlapping)  
                    sampled_fc = sampled_fc + fc 
                    ts = self.transcript.utterances[stop_index].get_end_ts() - self.transcript.utterances[start_index].get_start_ts() # approx speech (in ms) sampled
                    speech_time_sampled = speech_time_sampled + ts 
                    audio_time_sampled = audio_time_sampled + self.sampling_interval
                    if see_sub_stats is True:
                        print(print_stats.format(rt, rt + self.sampling_interval, ts , self.convert_to_min(ts), speech_time_sampled, self.convert_to_min(speech_time_sampled),
                            audio_time_sampled, self.convert_to_min(audio_time_sampled), fc ) )
                        print("  -->", self.transcript.utterances[start_index].get_start_ts(), " " , self.transcript.utterances[stop_index].get_end_ts(), " " , first_overlapping, " ", last_overlapping)
            self.sampled_features.append(sampled_fc)
            de = self.get_daylong_estimate()
            self.daylong_estimates.append(de)
            if see_final_stats: self.view_sampling_stats(audio_time_sampled, speech_time_sampled) 

        if export: 
            self.export(result_type=1)
            self.export(result_type=2)
            print("\tResults exported")

        return

    def find_interval_method4(self, random_time):
        start_index = None
        stop_index = None # indeces of first and last utterances to be sampled from 
        first_overlapping = False 
        last_overlapping = False # whether first & last utterances are overlapping 
        interval_start = random_time
        interval_end = random_time + self.sampling_interval
        for index, curr_utt in enumerate(self.transcript.utterances):
            utt_start = curr_utt.get_start_ts() 
            utt_end = curr_utt.get_end_ts() 
            if (interval_start > utt_start and utt_start <= interval_end) and (interval_start <= utt_end <= interval_end): #if utt starts outside of boundary but ends within boundary --> OVERLAPPING UTTERANCE --> start of interval
                if start_index is None:
                    start_index = index #loop has found first utterance of interval (and first_overlapping is True)
                    first_overlapping = True 
                else: continue # in the case that there is another overlapping utterance after the start index 
            elif (interval_start <= utt_start <= interval_end) and (interval_start <= utt_end <= interval_end): #if utt is completely within desired sampling boundaries
                if start_index is None:
                    start_index = index # loop has found first utterance within interval 
                    first_overlapping = False 
                else: continue # loop is within the interval, should continue to next iteraction 
            elif (interval_start <= utt_start <= interval_end) and (utt_end >= interval_start and utt_end > interval_end): #utt begins within interval but ends outside --> OVERLAPPING UTTERANCE --> reached end of interval
                if start_index is None: #for utt < 30s (BN32), entire utt spans boundary; in this case, part of utterance spans boundary --> do not sample
                    stop_index = None
                    break
                elif index == len(self.transcript.utterances) - 1:  #if curr utt is last one, return
                    stop_index = index
                    break
                else:
                    stop_index = index # save index of overlapping utterance 
                    last_overlapping = True 
                    break
            elif utt_start > interval_end: #curr utt is fully out of bounds --> previous utt is last utt of interval & fully within bounds
                if start_index is None: 
                    stop_index = None
                    last_overlapping = False 
                else:
                    stop_index = index - 1
                    last_overlapping = False 
                    break
        return start_index, stop_index, first_overlapping, last_overlapping

    def getfcount(self, lines, first_overlapping = False, last_overlapping = False):
        '''
        - samples for desired feature within specified lines
        '''
        words = []
        feature_type_ind = self.valid_features.index(self.feature_type) 
        if feature_type_ind == 0 or feature_type_ind == 2: # if sampling for total words or specific word, sample all words in given interval 
            # get speech from lines depending on overlapping status 
            for index, line in enumerate(lines):
                if line == lines[0] and first_overlapping is True: 
                    words = words + self.get_latter_half(line)
                    # print(half_utt_length, line[1+half_utt_length:-1])
                elif line == lines[-1] and last_overlapping is True: # count half of utterance
                    words = words + self.get_former_half(line)
                else:
                    words = words + line.get_speech() # add all tokens in line that is not the speaker tag and timestamp
            if feature_type_ind == 0: return len(words) # if estimating total words, nothing more else to do
            elif feature_type_ind == 2: return words.count(self.feature) # return # of occurrences of specific word in sampled words 
            
        elif feature_type_ind == 1 or feature_type_ind == 3: # if sampling for speech from a specific speaker or to a specific speaker (xds), then only sample from correctly labeled utterances 
            is_feature = False 
            for index, line in enumerate(lines):
                if line.get_speaker() == self.feature or line.get_xds() == self.feature: is_feature = True 
                else: is_feature = False
                if is_feature:
                    if self.feature == "CHI": words = words + ["CHI"] # FOR CHI, count as VOCALIZATIONS
                    else: # all others, count WORDS 
                        if line == lines[0] and first_overlapping: # if at beginning of interval AND 
                            words = words + self.get_latter_half(line)
                        elif line == lines[-1] and last_overlapping: # if at end of interval AND 
                            words = words + self.get_former_half(line)
                        else:
                            words = words + line.get_speech() # line is in interval and NOT overlapping --> add all tokens 
                else: continue # speaker or xds tag is not desired one, do not sample from that line
            return len(words) 
        
        elif feature_type_ind == 4: # if sampling for utterances with an annotation, will count for UTTERANCES (not words) 
            sampled_fcount = 0
            for index, line in enumerate(lines):
                rawspeech = line.get_speech(as_tokens = False, cleaned = False)
                if self.feature in rawspeech: sampled_fcount = sampled_fcount + 1 # sample line regardless of whether it is overlapping or not  
                else:  continue  # line does not contain a question, do not sample from line and move onto next
            return sampled_fcount

    # def get_latter_half(): given a line, get the latter half of the speech 
    # called in getfcount for sampling method 4 when first_overlapping is True 
    def get_latter_half(self, line):
        speech = line.get_speech() 
        half_length = math.floor(len(speech)/2) # index of halfway pt of speech tokens 
        return speech[half_length:]
    
    # def get_latter_half(): given a line, get the first half of the speech 
    # called in getfcount for sampling method 4 when last_overlapping is True 
    def get_former_half(self, line):
        speech = line.get_speech() 
        half_length = math.floor(len(speech)/2) # index of halfway pt of speech tokens 
        return speech[0: half_length]
    
    def view_sampling_stats(self, audio_time_sampled, speech_time_sampled):
         print("\n---Sampling Stats")
         print("---Total sampled feature counts:", self.sampled_features[-1])
         print("---Total audio sampled time (min): ", self.convert_to_min(audio_time_sampled) )
         print("---Total spoken sampled time (min): ", self.convert_to_min(speech_time_sampled) )
         print("---Daylong estimate:", self.daylong_estimates[-1])

    def get_daylong_estimate(self):
        total_silence = 0
        for silence_pair in self.transcript.silence_intervals:
            total_silence = total_silence + (silence_pair[1] - silence_pair[0])
        numerator = self.transcript.get_audio_length() - total_silence 
        denominator = self.total_sampled_time
        de = (numerator/denominator) * self.sampled_features[-1]  #sampled feature count for most recent simulation 
        return round(de, 2) 

    def generate_random_times(self):
        times = []
        #print("Num intervals: ", self.num_intervals)
        for interval in range(self.num_intervals):
            random_time = random.randrange(self.transcript.audio_length - self.sampling_interval)
            while self.in_silence(random_time):
                random_time = random.randrange(self.transcript.audio_length - self.sampling_interval)
            times.append(random_time)
        
        """  output_file = open("randomtimes.txt", "a")
            times.sort()
            times = [self.convert_to_min(time) for time in times]
            end_rt = [round((time +0.5),2) for time in times]
            times = [str(i) for i in times]
            times = "\t".join(times)

            end_rt = [str(i) for i in end_rt]
            end_rt = "\t".join(end_rt)
            #results = [str(element) for element in results]
            #results = " ".join(results)
            #print("rts", times)
            output_file.write("interval start(min): " + str(times))
            output_file.write("\ninterval end(min): " + str(end_rt)) 
            output_file.write("\n\n")
            print("wrote rts to file") """
          
        #for start_time in sorted(times):
        #    print(f"Start: {self.convert_to_min(start_time)} min, End: {self.convert_to_min(start_time + self.sampling_interval)} min")
        return times
    
    def in_silence(self, rt):
        for pair in self.transcript.silence_intervals:
            if (pair[0] - self.sampling_interval) <= rt <= pair[1]: #i.e. if timestamp is between start of silence (shifted to account of time interval) && end of silence
                return True 
        return False 

    def generate_random_times_nonoverlapping(self):
        print(f"for {self.convert_to_min(self.total_sampled_time)} min of tts, generating {self.num_intervals} 30 second intervals")
        timestamps = [] 
        # Generate available time slots excluding silence intervals
        available_time = [t for t in range(0, self.transcript.get_audio_length() - int(self.sampling_interval) + 1)
                      if all(t + self.sampling_interval <= start or t > end for start, end in self.transcript.silence_intervals)]
        #print(f"ALL AVAILBLE TIMESTAMPS {available_time}")
        while len(timestamps) < self.num_intervals and available_time:
            start_time = random.choice(available_time)
            #print(f"selected: {start_time}")
            timestamps.append(start_time)
            # Remove all times that would overlap with this interval
            left_index = bisect.bisect_left(available_time, start_time - self.sampling_interval)
            # Find the right boundary (smallest value > selected_value + delta)
            right_index = bisect.bisect_right(available_time, start_time + self.sampling_interval)
            # Remove the range efficiently
            #print(f"REMOVING: {available_time[left_index:right_index]}")
            del available_time[left_index:right_index]
        
        #print("generated non-overlapping timestamps")
        #for start_time in sorted(timestamps):
            #print(f"Start: {self.convert_to_min(start_time)} min, End: {self.convert_to_min(start_time + self.sampling_interval)} min")
        if len(timestamps) != self.num_intervals: print(f"\t{len(timestamps)}")
        return timestamps
    
    def convert_to_min(self, value): #converts a time in ms to minutes 
        value = value / (60 *1000)
        return round(value, 3)
    
    def convert_to_ms(self, value):
        return value * 60 * 1000 # convert to ms

    def describe(self):
        print(f"Random Sampler ---\n\tSampling {self.transcript.fname}")
        print("\tSampling total ", self.convert_to_min(self.total_sampled_time), "minutes")
        print("\tAcross ", self.num_intervals, "samples of size: ", self.convert_to_min(self.sampling_interval), "minutes")
        print("\tSimulations: ", self.simulations)
        print("\tEstimating feature:", self.feature_type, "(", self.feature, ")\tGround Truth Daylong Count: ", self.daylong_feature_count)
        print()
        return 
    
    def export(self,result_type = 1, output_fname = ""):
        print("exporting")
        print(self.feature_type)
        print(self.prop_tss)
        #if self.feature is None: self.feature = "None"
        #if self.prop_tss is None: self.prop_tss = "None"
        if output_fname == "": output_fname = f"{self.transcript.fname}_{self.feature_type}_TEST"   
        output_details = f"Transcript: {self.transcript.fname} Sampling_interval: {str(self.sampling_interval)} Prop_TTS: {str(self.prop_tss)} TTS: {str(self.total_sampled_time)} Feature: {self.feature_type}({self.feature})"
        results = []
        if result_type == 1: # DAYLONG WORD COUNT ESTIMATES
            #print("\tExporting to daylong_estimate_outputs.txt")
            results = self.daylong_estimates
            output_fname = output_fname + "_daylong_estimates.txt"
            output_file = open(output_fname, "a")
        elif result_type == 2: # SAMPLED WORD COUNTS
            #print("\tExporting to sampled_word_daylongcounts.txt")
            results = self.sampled_features
            output_fname = output_fname + "_sampled_fcounts.txt"
            output_file = open(output_fname, "a")

        results = [str(element) for element in results]
        results = " ".join(results)

        output_file.write(output_details)
        output_file.write('\n%s ' %str(self.sampling_interval))
        output_file.write('%s' %str(self.num_intervals))
        output_file.write('\n%s\n' %results)

        return
    


def main():
    transcript_fpath = "/Users/zeynepmarasli/Downloads/Documents/Projects/Daylong_Analyses/Python_Code/Transcripts/Clean/All_Tiers/" #Clean/All_Tiers/" #For_OSF/"
    A787_files = ["A787_001107_cleaned.txt", "A787_001109_cleaned.txt", "A787_001111_cleaned.txt"]
    transcript = DaylongTranscript(fpath = transcript_fpath+A787_files[0], fname = A787_files[0], isVanDam=False)
    transcript.describe()
    print("\n")
    sampler = Sampler(transcript, sampling_interval=0.5, total_sampled_time=10, simulations = 1, feature_type = "word count")
    sampler.describe()
    sampler.sample(export = False, see_final_stats=True, sample_non_overlapping=True)
    print()
    #sampler = Sampler(transcript, sampling_interval=0.5, total_sampled_time=1, simulations = 1, feature_type = "word count")
    #sampler.describe()
    #sampler.sample(export = False, see_final_stats=True)


#main()
print("random sampler loaded")