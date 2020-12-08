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