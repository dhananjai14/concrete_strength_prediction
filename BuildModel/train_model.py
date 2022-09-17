import pandas as pd
import traceback
import sklearn.metrics as metrics
from Logger import logger
from Model_save import ModelSave

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor


class modelFinder:
    """
                This class is used to find the model with best accuracy and AUC score.
    """

    def __init__(self):
        try:
            self.log = logger.logs()
            self.log.write_log('train_model', 'inside the class Model_finder')
            self.model = ModelSave.model_load()

        except:
            self.log.write_log('train_model', traceback.format_exc(), 'error')

    def train_test_split(self, path):
        try:
            data = pd.read_csv(path)
            self.log.write_log('train_model', 'inside the "train_test_split" method')
            train = data.sample(frac=.8, random_state=2)
            self.log.write_log('train_model', 'train dataset created')
            test = data.drop(train.index)
            self.log.write_log('train_model', 'test dataset created')
            self.log.write_log('train_model', 'return train and test dataset')
            return train, test
        except:
            self.log.write_log('train_model', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def x_y_split(self, data):
        try:
            self.log.write_log('train_model', 'inside the method "x_y_split"')
            y = data['Strength']
            x = data.drop(columns='Strength')
            self.log.write_log('train_model', 'x and y dataset are returned')
            return x, y
        except:
            self.log.write_log('train_model', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def get_best_params_for_random_forest(self, train_x, train_y):
        """
            Method Name: get_best_params_for_random_forest
            Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                         Use Hyper Parameter Tuning.
            Output: The model with the best parameters
            On Failure: Raise Exception

        """
        try:
            # initializing with different combination of parameters
            self.log.write_log('train_model', 'inside the "get_best_params_for_random_forest"')
            param_grid = {"n_estimators": [10, 50, 100, 130], "criterion": ['poisson'],
                          "ccp_alpha": [.1, .2, .3], "max_features": ['sqrt', 'log2']}
            # param_grid = {"n_estimators": [10],
            #               "criterion": ['poisson'],
            #               "ccp_alpha": [.1], "max_features": ['sqrt']}
            self.log.write_log('train_model', 'parameter grid created')
            # Creating an object of the Grid Search class
            regressor = RandomForestRegressor()

            grid = GridSearchCV(estimator=regressor, param_grid=param_grid, cv=5, verbose=3)
            self.log.write_log('train_model', 'GridSearchCV created')
            # finding the best parameters
            grid.fit(train_x, train_y)
            self.log.write_log('train_model', 'Training model to find best parameter on dataset')
            # extracting the best parameters
            criterion = grid.best_params_['criterion']
            ccp_alpha = grid.best_params_['ccp_alpha']
            max_features = grid.best_params_['max_features']
            n_estimators = grid.best_params_['n_estimators']
            self.log.write_log('train_model', 'best parameter criterion: {},ccp_alpha: {}, max_features: {} ,'
                                              'n_estimators: {}'.format(criterion, ccp_alpha, max_features,
                                                                        n_estimators))

            # creating a new model with the best parameters
            regressor = RandomForestRegressor(n_estimators=n_estimators, criterion=criterion, ccp_alpha=ccp_alpha,
                                              max_features=max_features)
            # training the mew model
            regressor.fit(train_x, train_y)
            self.log.write_log('train_model', 'model created')
            self.log.write_log('train_model', 'model returned')
            return regressor

        except:
            self.log.write_log('train_model', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def get_best_params_for_xgboost(self, train_x, train_y):

        """
                                        Method Name: get_best_params_for_xgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        On Failure: Raise Exception

        """

        try:
            # initializing with different combination of parameters
            self.log.write_log('train_model', 'inside the "get_best_params_for_xgboost"')
            param_grid_xgboost = {
                'learning_rate': [0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10],
                'n_estimators': [10, 50, 100],
                'gamma': [.1, 0]
            }
            # Creating an object of the Grid Search class
            model = XGBRegressor(objective='reg:squarederror')
            grid = GridSearchCV(model, param_grid_xgboost, verbose=3, cv=5)
            # finding the best parameters
            grid.fit(train_x, train_y)
            self.log.write_log('train_model', 'Find the best parameter')
            # extracting the best parameters
            learning_rate = grid.best_params_['learning_rate']
            max_depth = grid.best_params_['max_depth']
            n_estimators = grid.best_params_['n_estimators']
            gamma = grid.best_params_['gamma']
            self.log.write_log('train_model', 'best parameter learning_rate: {}, max_depth: {}, n_estimator: {}, '
                                              'gamma: {}'.format(learning_rate, max_depth, n_estimators, gamma))

            # creating a new model with the best parameters
            xgb = XGBRegressor(learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators, gamma=gamma)
            self.log.write_log('train_model', 'Creating model with best parameter')

            # training the mew model
            xgb.fit(train_x, train_y)
            self.log.write_log('train_model', 'XGBoost regressor model fit')
            self.log.write_log('train_model', 'XGBoost model returned')
            return xgb
        except:
            self.log.write_log('train_model', traceback.format_exc(), 'error')
            return traceback.format_exc()

    def get_best_model(self, train_x, train_y, test_x, test_y):
        """
                                                Method Name: get_best_model
                                                Description: Find out the Model which has the best r2 score.
                                                Output: The best model object
                                                On Failure: Raise Exception

        """

        try:
            xgboost = self.get_best_params_for_xgboost(train_x, train_y)
            prediction_xgboost = xgboost.predict(test_x)
            xgboost_score = metrics.r2_score(test_y, prediction_xgboost)
            self.log.write_log('train_model', 'XGBoost model score is {}'.format(xgboost_score))

            # create best model for Random Forest
            random_forest = self.get_best_params_for_random_forest(train_x, train_y)
            prediction_random_forest = random_forest.predict(test_x)  # prediction using the Random Forest Algorithm
            random_forest_score = metrics.r2_score(test_y, prediction_random_forest)
            self.log.write_log('train_model', 'Random forest score is {}'.format(random_forest_score))

            # comparing the two models
            if random_forest_score < xgboost_score:
                self.log.write_log('train_model', 'Model returned XGBoost')
                self.model.to_save(xgboost, 'train_model')
                return xgboost
            else:
                self.log.write_log('train_model', 'Model returned Random Forest')
                self.model.to_save(random_forest, 'train_model')
                return random_forest

        except:

            self.log.write_log('train_model', traceback.format_exc(), 'error')
            return traceback.format_exc()


# a = modelFinder()
# train, test = a.train_test_split(
#     r'C:\Users\preet\Desktop\DS\Project\Concrete Project\Clustered Data\training\clustered_cement.csv')
# train_x, train_y = a.x_y_split(train)
# test_x, test_y = a.x_y_split(test)
# model = a.get_best_model(train_x, train_y, test_x, test_y)
