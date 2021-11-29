# NLP_ADHD

# Project Summary:

This project aims to leverage NLP and ML models to improve the quality of care offered to children with developmental and behavioral disorders, including attention-deficit/hyperactivity disorder (ADHD) and autism spectrum disorder (ASD). We successfully created a pipeline and binary classification algorithm based on a BERT transformer that achieved acceptable performance in classifying clinician notes that contained recommendations for evidence-based treatments for young children with ADHD. We have also deployed the model on the unannotated deployment set, which gave us a recall of 0.92. 

# Dataset:

The dataset used consists of electronic health records (EHR) provided by Primary care providers (PCP) for 4-5 years of preschool-aged children.

# Repository Structure:

The repo consists of the src folder, which has two folders listed below:
1. data_processing:This folder contains python files required for processing text data from the notes before applying the transformer model.

2. notebooks:This folder contains notebooks used to obtain results for the research.
  
    a. The Training_ClinicalBERT notebook trains the network using dataset mentioned, and the trained weights are saved for further use.
  
    b. The Deployment_Val_Test_Set notebook uses the saved weights to obtain the results for validation and test set(annotated notes).
  
    c. The Final_Deployment_notebook uses the saved weights and predicts the labels and "BT_y/n" for unannotated notes, and the predictions are saved for further analysis.           (BT: Behavioral Therapy)
  
 
# Technologies used:

The Jupyter notebooks and python files needed are generated and executed using JupyterLab on the Google Cloud console and using GPU.

# Machine Learning algorithm used:

The network was trained using different transformer models, and the results are in the below table. The ClinicalBERT performed best and was used for further analysis.

![image](https://user-images.githubusercontent.com/36389195/143954469-6254aab7-349c-41b1-acf2-c5fee8871294.png)

# Citations:

 1. https://simpletransformers.ai/docs/binary-classification/

