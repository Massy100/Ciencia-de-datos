import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn 

from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

# clasificador -> (formato, nombre_clasificador)
CLASS_MAP = {
    'Logistid Regression': ('-', LogisticRegression()),
    'Naive Bayes': ('--', GaussianNB()),
    'Decision Tree': ('.-', DecisionTreeClassifier()),
    'Random Forest': (':', RandomForestClassifier())
}

df = sns.load_dataset('iris')
print(df)
sns.pairplot(df, hue='species')
plt.show()

X, Y  = df[df.columns[:3]], (df['species'] == 'virginica')
print(X)
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=77)
for nombre, (line_fmt, model) in CLASS_MAP.items():
    model.fit(X_train, Y_train)
    preds = model.predict_proba(X_test)
    predicciones = pd.Series(preds[:,1])
    fpr, tpr, umbral = roc_curve(Y_test, predicciones)
    auc_score = auc(fpr, tpr)
    etiqueta = '%s: auc=%f' % (nombre, auc_score)
    plt.plot(fpr, tpr, line_fmt, linewidth=5, label=etiqueta)
plt.legend(loc='lower right')
plt.title('Comparacion de clasificadores')
plt.plot([0, 1], [0, 1], 'k--', linewidth=5)
plt.xlim([0.0, 1.05])
plt.ylim([0.0, 1.05])
plt.xlabel('Indice de falsos positivos')
plt.ylabel('Indice de verdaderos positivos')
plt.show()
    
