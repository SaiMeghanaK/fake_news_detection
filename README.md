# fake_news_detection
A human in the loop fake news detection platform that combines XGBoost based NLP predictions with human verification to improve the reliability of news classification. Built with Django, DRF, PostgreSQL, and Bootstrap.
This project is a news publishing and verification platform that combines **Machine Learning with Human Review** to reduce the risk of publishing potentially fake news. The platform allows writers to submit news articles, automatically analyzes submitted content using a trained **TF-IDF + XGBoost fake news detection model**, and routes suspicious articles to an administrator for manual verification.

The key idea behind the project is:
**AI assists the verification process, while the final publishing decision can remain with a human administrator.**


<img width="517" height="601" alt="image" src="https://github.com/user-attachments/assets/b2ca5a75-2936-45df-ada1-106a7ab5fb0c" />


The project provides three types of users:
**Writer** — Creates and submits news articles.
**Reader** — Reads verified and published articles.
**Administrator** — Reviews articles flagged by the ML model and makes the final decision.

When an article is predicted as **real**, it can be published automatically. When an article is predicted as **fake**, it is **not immediately rejected**. Instead, it is flagged and sent to the administrator for human review.
The administrator can then:
->Approve the article and publish it.
->Reject the article and provide a reason.
The writer receives a notification about the final decision.

# Technology Stack
## Machine Learning
* Python
* Pandas
* NumPy
* NLTK
* BeautifulSoup
* Scikit-learn
* TF-IDF
* XGBoost
* Joblib
* Matplotlib
* Seaborn
* WordCloud

## Backend
* Python
* Django
* Django REST Framework

## Database
* PostgreSQL
  
## Frontend
* HTML
* Bootstrap 5
* JavaScript

## Development Tools
* Google Colab
* Visual Studio Code

# Machine Learning Pipeline
The fake news detection model was trained separately in Google Colab and then integrated into the Django application. The following process is used:


<img width="281" height="612" alt="image" src="https://github.com/user-attachments/assets/fb6789f0-e32a-467b-b6f4-306906e909d3" />

## Dataset
This project uses the **WELFake Dataset** for training and evaluating the fake news detection model.

* **Dataset:** WELFake Dataset
* **Author:** Saurabh Shahane
* **Source:** [Kaggle – Fake News Classification](https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification)
* **Original dataset:** The dataset combines multiple existing news datasets and contains news titles, article text, and labels.
* **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The dataset was used for academic/project purposes and was processed and transformed as part of this project, including text preprocessing, TF-IDF feature extraction, and model training using XGBoost.



