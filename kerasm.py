import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn import preprocessing

global_model = 0

# define base model
def baseline_model(glob_model):
	def baseline_model():
		# create model
		model = Sequential()
		model.add(Dense(3, input_dim=3, kernel_initializer='normal', activation='relu'))
		model.add(Dense(1, kernel_initializer='normal'))
		# Compile model
		model.compile(loss='mean_squared_error', optimizer='adam')
		glob_model = model
		return model

# define the model
def larger_model(glob_model):
	# create model
	model = Sequential()
	model.add(Dense(10, input_dim=3, kernel_initializer='normal', activation='tanh'))
	model.add(Dense(10, kernel_initializer='normal', activation='sigmoid'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	glob_model = model
	return model

# load dataset
dataframe = pandas.read_csv("data_soft.csv", delim_whitespace=True, header=None)
dataset = dataframe.values
# split into input (X) and output (Y) variables
X = dataset[:,0:3]
Y = dataset[:,3]
#X = preprocessing.normalize(X)

# fix random seed for reproducibility
seed = 7
# evaluate model with standardized dataset

#global_model = load_model('model.nn')

np.random.seed(seed)
estimator = KerasRegressor(build_fn=baseline_model(global_model), epochs=50, batch_size=5, verbose=0)
estimator.fit(X, Y)
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', estimator))
pipeline = Pipeline(estimators)
kfold = KFold(n_splits=2, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kfold)

global_model.save('model.nn')

print(results)
print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# Voir comment ce mec fait : https://stackoverflow.com/questions/44132652/keras-how-to-perform-a-prediction-using-kerasregressor

## PREDICTION
Xnew = np.array([[12.98, 15.48, 15.57]])
Ynew = np.array([[0.1]])
prediction = estimator.predict(Xnew)
print(prediction)
# make a prediction
Xnew = np.array([[11.65, 13.46, 14.03]])
Ynew = np.array([[0.6]])
prediction = estimator.predict(Xnew)
print(prediction)
# make a prediction
Xnew = np.array([[0.7, 8.48, 9.0]])
Ynew = np.array([1.4])
prediction = estimator.predict(Xnew)
print(prediction)
# make a prediction
# show the inputs and predicted outputs
#accuracy_score(Ynew, prediction)