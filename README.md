# Unsupervised-Protein-Genes-Diseases-Extraction
Extract Proteins, Genes, and Diseases from text 

## Requirements:
1. Anaconda
2. Gensim
3. Spacy


If you are quite familiar with Anaconda, there is no need to read this post. The procedures are the same as they are on local machines.

Contents:

Download Anaconda
Install Anaconda
Create New Environment
Install Necessary Libraries
Download Anaconda
Go to the Anaconda official website and choose a version that fits your machine instance. I picked Anaconda 3 for Python 3.7 on Linux because I am using an Ubuntu instance. Copy the link of the Anaconda installation package.

type in terminal:

cd ~
Use wget to download Anaconda installation package to your directory:

wget link-of-Anaconda-package  [wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh]

## Installing Anaconda
NOTE:

Make sure the downloaded Anaconda installation package is in the root directory and
you are in the root directory while trying to install Anaconda with bash. Otherwise, things would get pretty weird.
After downloading the file to our machine, use bash the the command to run the file and install it(replace Anaconda3-5.1.0-Linux-x86_64.sh with the name of the file you download):

cd ~
bash Anaconda3-5.3.1-Linux-x86_64.sh
This can take a while.

Create New Environment
Things can’t just work out without bugs. So usually this error arises:

-bash: conda: command not found
Luckily it is not a tough problem. By one single command, we can solve it out.

For Anaconda 2:

export PATH=~/anaconda2/bin:$PATH
For Anaconda 3:

export PATH=~/anaconda3/bin:$PATH
Now we can create a new environment:

conda create -n deep-learning python=3
Explanation:

the command after create -n is the name of your newly-created environment. So the environment I am creating here is named “deep-learning”.
python=3 specifies the Python version in my deep-learning environment. If not specified in detail, this command installs Python 3.6 on my machine. So if your demand is more specific, you can provide more information in the command, such as python=3.5, in which case, my environment would have Python 3.5.
After the environment is created, you can check by

conda info --envs
You will see results similar to like this

ubuntu ~ $ conda info --envs
## conda environments:
#
DAND                     /Users/ubuntu/anaconda/envs/DAND dlnd /Users/ubuntu/anaconda/envs/dlnd deep-learning /Users/ubuntu/anaconda/envs/deep-learning 
Install Necessary Libraries
If you want to install libraries into an environment, or you want to use that environment, you have to activate the environment first by

source activate deep-learning
Only after the above command, we can install desired packages into the target environment.

The installation command is pretty straightforward:

conda install numpy pandas
But sometimes it can be

conda install -c conda-forge some-package
Here the command -c conda-forge are specifying the channel from which we are getting the package. The default channel is -c anaconda, which we don’t have to specify if we are using the default channel.

## Install Gensim and Spacy
conda install -c conda-forge gensim
conda install -c conda-forge spacy

Download Spacy models
anaconda3/envs/deep-learning/bin/python -m spacy download en_core_web_sm
anaconda3/envs/deep-learning/bin/python -m spacy download en

Download NLTK stopwords
import nltk
nltk.download('stopwords')

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

![CC BY 4.0 Icon](https://licensebuttons.net/l/by/4.0/88x31.png)

