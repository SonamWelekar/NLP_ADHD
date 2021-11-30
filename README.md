# NLP_ADHD

# Background

The National Institute for Children’s Health Quality has recognized that quality measures for child mental and behavioral health disorders, including attention-deficit/hyperactivity disorder (ADHD), are lacking and are critically needed (2). The current national quality measures used for assessment of ADHD care (Healthcare Effectiveness Data and Information Set (HEDIS)) capture the timing of follow up care for children prescribed with ADHD medications (3). These claims-based measures only address a narrow aspect of care in a subset of patients. Furthermore, they are not based on published clinical practice guidelines and received a “poor” or “not-rated” strength of evidence grade (4). Manual chart review of a sample of ADHD patients per clinician – used by many health care organizations to supplement these crude measures – is labor-intensive and expensive (5,6).

# Project Summary:

This project aims to leverage natural language processing (NLP) and machine learning (ML) models to improve the measurement of quality-of-care offered to children with developmental and behavioral disorders, including ADHD. We created a pipeline and binary classification algorithm based on a BERT transformer that achieved acceptable performance in classifying clinician notes that contained recommendations for evidence-based treatments for young children with ADHD. We also deployed the model on the unannotated deployment set (n=1,020 notes), which gave us a recall of 0.92. 

# Dataset:

The dataset used consists of clinical notes (free text data) from electronic health records (EHR) documented by Primary care providers (PCPs) at a communinty-based primary care network in California. Notes included are from primary care visits of children aged 4-6 years who have at least 1 visit with an ICD-10 diagnosis of ADHD after the age of 4 years.

# Repository Structure:

The repo consists of the src folder, which has two folders listed below:
1. data_processing:This folder contains python files required for processing text data from the notes before applying the transformer model.

2. notebooks:This folder contains notebooks used to obtain results for the research.
  
    a. The Training_ClinicalBERT notebook trains the network using dataset mentioned, and the trained weights are saved for further use.
  
    b. The Deployment_Val_Test_Set notebook uses the saved weights to obtain the results for validation and test set (annotated notes).
  
    c. The Final_Deployment_notebook uses the saved weights and predicts the labels and "BT_y/n" for unannotated notes, and the predictions are saved for further analysis.           (BT: Behavioral Therapy)
  
 
# Technologies used:

The Jupyter notebooks and python files needed are generated and executed using JupyterLab on the Google Cloud console and using GPU.

# Machine Learning algorithm used:

The network was trained using different transformer models, and the results are in the below table. The ClinicalBERT performed best and was used for further analysis.

![image](https://user-images.githubusercontent.com/36389195/143954469-6254aab7-349c-41b1-acf2-c5fee8871294.png)

# Citations:

 1. https://simpletransformers.ai/docs/binary-classification/
 2. Zima BT, Mangione-Smith R. Gaps in quality measures for child mental health care: an opportunity for a collaborative agenda. Journal of the American Academy of Child and Adolescent Psychiatry. 2011;50(8):735-737.
 3. National Committee for Quality Assurance. Follow-up care for children prescribed ADHD medication. Available at: http://www.ncqa.org. . Accessed October 24, 2019.
 4. Zima BT, Murphy JM, Scholle SH, et al. National quality measures for child mental health care: background, progress, and next steps. Pediatrics. 2013;131 Suppl 1:S38-49.
 5. Casalino LP, Gans D, Weber R, et al. US Physician Practices Spend More Than $15.4 Billion Annually To Report Quality Measures. Health Aff (Millwood). 2016;35(3):401-406.
 6. Schuster MA, Onorato SE, Meltzer DO. Measuring the Cost of Quality Measurement: A Missing Link in Quality Strategy. Jama. 2017;318(13):1219-1220.



