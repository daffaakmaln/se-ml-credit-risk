Description of the German credit dataset.



1\. Title: German Credit data



2\. Source Information



Professor Dr. Hans Hofmann  

Institut f"ur Statistik und "Okonometrie  

Universit"at Hamburg  

FB Wirtschaftswissenschaften  

Von-Melle-Park 5    

2000 Hamburg 13 



3\. Number of Instances:  1000



Two datasets are provided.  the original dataset, in the form provided

by Prof. Hofmann, contains categorical/symbolic attributes and

is in the file "german.data".   

&#x20;

For algorithms that need numerical attributes, Strathclyde University 

produced the file "german.data-numeric".  This file has been edited 

and several indicator variables added to make it suitable for 

algorithms which cannot cope with categorical variables.   Several

attributes that are ordered categorical (such as attribute 17) have

been coded as integer.    This was the form used by StatLog.





6\. Number of Attributes german: 20 (7 numerical, 13 categorical)

&#x20;  Number of Attributes german.numer: 24 (24 numerical)





7\.  Attribute description for german



Attribute 1:  (qualitative)

&#x09;       Status of existing checking account

&#x20;              A11 :      ... <    0 DM

&#x09;       A12 : 0 <= ... <  200 DM

&#x09;       A13 :      ... >= 200 DM /

&#x09;	     salary assignments for at least 1 year

&#x20;              A14 : no checking account



Attribute 2:  (numerical)

&#x09;      Duration in month



Attribute 3:  (qualitative)

&#x09;      Credit history

&#x09;      A30 : no credits taken/

&#x09;	    all credits paid back duly

&#x20;             A31 : all credits at this bank paid back duly

&#x09;      A32 : existing credits paid back duly till now

&#x20;             A33 : delay in paying off in the past

&#x09;      A34 : critical account/

&#x09;	    other credits existing (not at this bank)



Attribute 4:  (qualitative)

&#x09;      Purpose

&#x09;      A40 : car (new)

&#x09;      A41 : car (used)

&#x09;      A42 : furniture/equipment

&#x09;      A43 : radio/television

&#x09;      A44 : domestic appliances

&#x09;      A45 : repairs

&#x09;      A46 : education

&#x09;      A47 : (vacation - does not exist?)

&#x09;      A48 : retraining

&#x09;      A49 : business

&#x09;      A410 : others



Attribute 5:  (numerical)

&#x09;      Credit amount



Attibute 6:  (qualitative)

&#x09;      Savings account/bonds

&#x09;      A61 :          ... <  100 DM

&#x09;      A62 :   100 <= ... <  500 DM

&#x09;      A63 :   500 <= ... < 1000 DM

&#x09;      A64 :          .. >= 1000 DM

&#x20;             A65 :   unknown/ no savings account



Attribute 7:  (qualitative)

&#x09;      Present employment since

&#x09;      A71 : unemployed

&#x09;      A72 :       ... < 1 year

&#x09;      A73 : 1  <= ... < 4 years  

&#x09;      A74 : 4  <= ... < 7 years

&#x09;      A75 :       .. >= 7 years



Attribute 8:  (numerical)

&#x09;      Installment rate in percentage of disposable income



Attribute 9:  (qualitative)

&#x09;      Personal status and sex

&#x09;      A91 : male   : divorced/separated

&#x09;      A92 : female : divorced/separated/married

&#x20;             A93 : male   : single

&#x09;      A94 : male   : married/widowed

&#x09;      A95 : female : single



Attribute 10: (qualitative)

&#x09;      Other debtors / guarantors

&#x09;      A101 : none

&#x09;      A102 : co-applicant

&#x09;      A103 : guarantor



Attribute 11: (numerical)

&#x09;      Present residence since



Attribute 12: (qualitative)

&#x09;      Property

&#x09;      A121 : real estate

&#x09;      A122 : if not A121 : building society savings agreement/

&#x09;			   life insurance

&#x20;             A123 : if not A121/A122 : car or other, not in attribute 6

&#x09;      A124 : unknown / no property



Attribute 13: (numerical)

&#x09;      Age in years



Attribute 14: (qualitative)

&#x09;      Other installment plans 

&#x09;      A141 : bank

&#x09;      A142 : stores

&#x09;      A143 : none



Attribute 15: (qualitative)

&#x09;      Housing

&#x09;      A151 : rent

&#x09;      A152 : own

&#x09;      A153 : for free



Attribute 16: (numerical)

&#x20;             Number of existing credits at this bank



Attribute 17: (qualitative)

&#x09;      Job

&#x09;      A171 : unemployed/ unskilled  - non-resident

&#x09;      A172 : unskilled - resident

&#x09;      A173 : skilled employee / official

&#x09;      A174 : management/ self-employed/

&#x09;	     highly qualified employee/ officer



Attribute 18: (numerical)

&#x09;      Number of people being liable to provide maintenance for



Attribute 19: (qualitative)

&#x09;      Telephone

&#x09;      A191 : none

&#x09;      A192 : yes, registered under the customers name



Attribute 20: (qualitative)

&#x09;      foreign worker

&#x09;      A201 : yes

&#x09;      A202 : no







8\.  Cost Matrix



This dataset requires use of a cost matrix (see below)





&#x20;     1        2

\----------------------------

&#x20; 1   0        1

\-----------------------

&#x20; 2   5        0



(1 = Good,  2 = Bad)



the rows represent the actual classification and the columns

the predicted classification.



It is worse to class a customer as good when they are bad (5), 

than it is to class a customer as bad when they are good (1).







