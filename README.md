

MFA (Montreal Forced Aligner) 

## Installation Method

MFA was installed using Conda (Miniconda).

### Step 1: Download Miniconda

- Download from https://www.anaconda.com/docs/getting-started/miniconda/main  
- Install it normally

### Step 2: Create MFA Environment

This keeps MFA isolated and avoids conflicts.
- conda create -n mfa python=3.10 -y
- Here we are creating a new virtual environment called “mfa” and installing 
- Python version 3.10 inside the environment. 
- -y automatically answers “yes” to all the prompts. 
- Command: conda activate mfa 
- In the terminal we need to see (mfa) , which means the environment is active.
 ### Step 3: Install Montreal Forced Aligner
 - Command : conda install -c conda-forge montreal-forced-aligner -y
- Command : mfa version
 ### Step  4 : Download Required Models
 - Acoustic model : Command : mfa model download acoustic english_us_arpa  
 - Dictionary : Command: mfa model download dictionary english_us_arpa
 - G2P Model (Grapheme-to-Phoneme) : Command : mfa model download g2p english_us_arpa
