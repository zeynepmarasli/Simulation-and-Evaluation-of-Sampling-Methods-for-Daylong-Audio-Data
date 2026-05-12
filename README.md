# Simulation and Evaluation of Sampling Methods for Daylong Audio Data
Code and analyses used for "Simulation and Evaluation of Sampling Methods for Daylong Audio Data"

1. clean_transcript.py
   - this python file takes in a raw CHAT file of a daylong transcript (transcripts used in this project can be found on HomeBank)
   - creates a tab-delimited txt file with the columns: [speaker]  [cleaned_utterance]  [raw_utterance]  [start_time]  [stop_time]  [xds]  [any other tiers]
   - this tab-delimited txt file is what is used for this project
  
2. daylongtranscript.py 
   - contain DaylongTranscript object ; requires tab-delimited txt file version of transcripts

3. randomsampler.py
   - contains RandomSampler object ; used to simulate sampling methods
   - uses DaylongTranscript object
   - outputs results to text file 

4. process_results_for_analysis_public.ipynb
   - uses generated raw sampling results to process estimate error results for analysis (outputs to csv
   - requires tab-delimited txt file version of transcripts
   - requires raw daylong estimate results (in SamplingResults_Raw.zip)
   

5. results_analysis_figures_public.ipynb
      - generates figures & tables included in main text 
      - requires CSV files of results (see CSV folder)
