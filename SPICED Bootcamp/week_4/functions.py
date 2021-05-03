def run_model(estimator, X_train, y_train):
    
    from sklearn.metrics import classification_report

    estimator.fit(X_train, y_train)
    
    y_pred = estimator.predict(X_train)
    
    print(classification_report(y_train, y_pred))
    
    return(estimator, y_pred)


def tune_model(estimator, X_train, y_train, param_grid, scoring, cv = 5):
    
    from sklearn.model_selection import GridSearchCV

    gridsearch = GridSearchCV(estimator = estimator, 
                              scoring = scoring,
                              param_grid = param_grid, 
                              cv = cv,
                              verbose = False)

    gridsearch.fit(X_train, y_train)
    
    print("CV results (mean test score):")
    print(gridsearch.cv_results_["mean_test_score"])

    print("Best score:")
    print(gridsearch.best_score_)
    
    print("Best parameters:")
    print(gridsearch.best_params_)
    
    return gridsearch