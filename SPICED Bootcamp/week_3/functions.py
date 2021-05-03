# extract date features
def extract_date_info(df):
    
    df['month'] = df.index.month
    df['day'] = df.index.day
    df['weekday'] = df.index.day_name()
    df['hour'] = df.index.hour



    # Outlier detection

# https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
def m_z_score(series):
    z_score = (0.6745*(series-series.median()))/series.mad()
    return z_score

def detect_outlier(series, threshold=3.5):
    outliers = series[m_z_score(series) > threshold]
    return outliers

    

def rsmle_scorer(y_true, y_pred):
    RSMLE = np.sqrt(np.mean((np.log1p(y_pred) - np.log1p(y_true))**2))
    return RSMLE

    
    #Lr in one line:

    # lr_base = LinearRegression().fit(X_train, np.log1p(y_train))


    #Bin and scale : pipeline_bin5_scale = Pipeline(steps=[('bin10', KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')), ('scale', MinMaxScaler())])


def print_evaluations(ytrue, ypred, model):
    '''
    Prints the confusion matrix and some evaluation metrics for 
    a specified model.
    
    Parameters:
    -----------
    ytrue : The true y-values
    ypred : The predicted y-values
    model : The model used to make the predictions: str
    '''
    
    print(f'How does model {model} score:')
    print(f'The accuracy of the model is: {round(accuracy_score(ytrue, ypred), 3)}')
    print(f'The precision of the model is: {round(precision_score(ytrue, ypred), 3)}')
    print(f'The recall of the model is: {round(recall_score(ytrue, ypred), 3)}')
    print(f'The f1-score of the model is: {round(f1_score(ytrue, ypred), 3)}')
    
    #print heatmap/confusion-matrix
    fig = plt.figure(figsize=(7, 6))
    cm = confusion_matrix(ytrue, ypred)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, fmt='.0f', ax=ax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['non-fraud', 'fraud'])
    ax.yaxis.set_ticklabels(['non-fraud', 'fraud'])