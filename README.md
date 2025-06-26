# Simulation and Evaluation of Sampling Methods for Daylong Audio Data
Code and analyses used for "Simulation and Evaluation of Sampling Methods for Daylong Audio Data"

1. clean_transcript.py
   - this python file takes in a raw CHAT file of a daylong transcript (transcripts used in this project can be found on HomeBank)
   - creates a tab-delimited txt file with the columns: [speaker]  [cleaned_utterance]  [raw_utterance]  [start_time]  [stop_time]  [xds]  [any other tiers]
   - this tab-delimited txt file is what is used for this project
  
2. daylongtranscript.py randomsampler.py
   - contain DaylongTranscript object ; requires tab-delimited txt file version of transcripts

3. randomsampler.py
   - contains RandomSampler object ; used to simulate sampling methods
   - uses DaylongTranscript object
   - outputs results to text file 

4. analyze_visualize_results.ipynb
   - JupyterNotebook of all analyses included in paper
   - uses generated 
   - requires tab-delimited txt file version of transcripts
   - requires CSV files of results (see CSVs folder)
     
