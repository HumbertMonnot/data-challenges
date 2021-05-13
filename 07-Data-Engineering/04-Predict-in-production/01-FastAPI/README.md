
Now that we have a performant model trained in the cloud, we will expose it to the world 🌍

We will create a **Prediction API** for our model, run it on our machine in order to make sure that everything works correctly. Then we will put it in the cloud so that everyone can play with our model!

In order to do so, we will:
- Challenge 1 : create a **Prediction API** using **FastAPI**
- Challenge 2 : create a **Docker image** containing the environment required in order to run the code of our API
- Challenge 3 : push this image to **Google Cloud Run** so that it is instantiated as a **Docker container** that will run our code and allow developers all over the world to use it

**Where to start?**

We will use the package we provided for you in the current directory, `TaxiFareModel`. In order to avoid creating a `git` repository within the `data-challenges`, let's move it outside!
`cp TaxiFareModel ~/code/<user.github_nickname>/`
`cd ~/code/<user.github_nickname>/TaxiFareModel `
`pip install -e .`
`git init`

Make sure to update the variables in `params.py` and in the `Makefile` which will enable you to connect to your project on Google Cloud.

## Before we start - let's go through some important points

### About the version of your trained model + code

⚠️ Do not forget that we cannot load a `model.joblib` file without the code that was used in order to train it! After all, we need to be using the exact same pipeline ⚠️

👉 You can run `make run_locally` to train the model and save it within your project. If it's not working for you, make a ticket.

### About the version of your trained model + packages

⚠️ We need to make sure that the versions of the packages (`numpy`, `pandas`, `scikit-learn` and so on) used in order to train the model are going to be the same as the ones used in order to load the `model.joblib` file ⚠️

👉 This is probably not going to be a concern if you trained your model just now (no new versions of the packages)

👉 You may encounter this issue in the future if you try to load a `model.joblib` file for your **Prediction API** a few months from now. The solution is to pin the versions of the packages in your `requirements.txt`. Remember the **AI Platform RUNTIME** ? The [version of the runtime](https://cloud.google.com/ai-platform/training/docs/runtime-version-list) that you used for the training allows you to know which versions of the packages to use.

## Let's create our first Prediction API exposing our model

Do you remember having consumed an API during the Python module using the `requests` package?

Today we are going to create your own API allowing other developers to ask our model for predictions.

### First step: let's create an API endpoint and test it

Your project should look like this (use the `tree` command):

```
.
├── api
│   ├── __init__.py
│   └── fast.py
├── notebooks
│   └── API usage.ipynb
├── TaxiFareModel
│   ├── __init__.py
│   ├── data.py
│   ├── encoders.py
│   ├── gcp.py
│   ├── params.py
│   ├── trainer.py
│   └── utils.py
├── Makefile
├── MANIFEST.in
├── model.joblib
├── predict.py
├── requirements.txt
└── setup.py
```

In `api/fast.py`, let's create a root endpoint that will welcome the developers using our API.

In order to do that, we will use **FastAPI**.

⚠️ Usually our API is going to be called from the python code inside of a notebook or a package or from any language ran in the **Back-End**. That means that the code is not located inside of a web page. In this case, no issues 👌

We want our API to be quite open and to allow developers to plug it in the code that is going to run inside of a browser: the **JavaScript** code running in the browser when a web page is displayed.

In order to allow that, we need to add some specific **CORS** boilerplate to our **FastAPI** code:

``` python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
```

👉 If we do not use the `add_middleware` method, then our API will only work when called from **Back-End** code (or similar), but not when called from the **JavaScript** code of a web page. Open this link in order to learn [more about CORS](https://fastapi.tiangolo.com/tutorial/cors/)...

**Let's create our root endpoint**

Add the below code right after *middleware*:

```python
@app.get("/")
def index():
    return {"greeting": "Hello world"}
```

The endpoint will simply return the following json content when a developer hits the root of our API : http://localhost:8000/

``` json
{
  "greeting": "Hello world"
}
```

*Hint*: you may create the `make run_api` **Makefile** directive in order to run the **uvicorn** web server that will serve the API:

```python
run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload
```

Once the server is started, you can play with the API either directly: http://localhost:8000/

... Or through the **Swagger** documentation: http://localhost:8000/docs (click on the endpoint you wish to play with, then hit **Try it out**)

### Receive the parameters for the prediction

We have a basic endpoint for our API but that is not very useful...

Let's create a `/predict` endpoint that will be used for the predictions.

We want developers to provide the following parameters to the endpoint:
- `pickup_datetime`
- `pickup_longitude`
- `pickup_latitude`
- `dropoff_longitude`
- `dropoff_latitude`
- `passenger_count`

As a response, let's first send back the provided values in order to make sure that everything is connected correctly:

For example, when called with the following parameters: `http://127.0.0.1:8000/predict?pickup_datetime=2013-07-06 17:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=1`

...the API will respond:

``` json
{
  "pickup_datetime": "2013-07-06 17:18:00",
  "pickup_longitude": "-73.950655",
  "pickup_latitude": "40.783282",
  "dropoff_longitude": "-73.984365",
  "dropoff_latitude": "40.769802",
  "passenger_count": "1"
}
```

If you don't remember how to retrieve parameters from an API call go back to the lecture slides.

### Predicting the fare amount

Now that the piping is done, let's make an actual prediction.

#### Build a dataframe for the prediction

First, we need to store the API parameters as an observation in an `X_pred` dataframe.

The columns should match the format of the `X_train` used in order to train the pipeline of our model. Otherwise the pipeline will output a python error...

Here are the data types of the columns of `X_train`:

```
key                     object
pickup_datetime         object
pickup_longitude        float64
pickup_latitude         float64
dropoff_longitude       float64
dropoff_latitude        float64
passenger_count         int64
```

🚨 Be careful with the order of the columns when you create the dataframe! **Pandas** does not care about the order of the columns but **Numpy** does and you might end up surprised by the results if you build a dataframe with an incorrect order of columns.

#### Handle the `key` column

*Hint*: the code provided for the TaxiFare model uses an additional **key** column. Its value (for example `key="2013-07-06 17:18:00.000000119"`) will not affect the model however if the column is missing the pipeline will not accept the dataframe as an input...

We cannot ask the developer calling our API to provide a value for the key column, as this data does not make sense for our API.

Yet the column needs to exist in the dataframe that is passed to the pipeline for the prediction.

👉 You need to fill the column with some hard coded value in order to allow the pipeline to train.

#### Localize the datetime provided by the developer

Since our API predicts the price of a fare in NYC, it seems straightforward to assume that the user (and therefore the developer) will input a datetime with the time in New York City when querying our API.

Our model was trained using UTC though (remember the content of the dataset where the `pickup_datetime` look like "2013-07-06 17:18:00 UTC").

We need to convert the time input by the user (and assume it is a time on the timezone of NYC).

<details>
<summary>
  💡 Hint: how to localize the user provided datetime to the NYC timezone ?
</summary>


``` python
from datetime import datetime
import pytz

# create a datetime object from the user provided datetime
pickup_datetime = "2021-05-30 10:12:00"
pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

# localize the user datetime with NYC timezone
eastern = pytz.timezone("US/Eastern")
localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
```

</details>


Once we have a localized user time, we want to convert it to UTC so that it can be fed to our pipeline.

<details>
<summary>
  💡 Hint: how to convert a localized datetime to UTC ?
</summary>


``` python
# localize the datetime to UTC
utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
```

</details>


Remember the specific format expected by the pipeline (an `object`, not a `datetime64`).

👉 Convert the data accordingly

<details>
<summary>
  💡 Hint: how to convert a datetime to the format expected by the pipeline ?
</summary>


``` python
formatted_pickup_datetime = utc_pickup_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
```

</details>


#### Make a prediction

Now that we have created a `X_pred` dataframe, let's make a prediction.

Let's load the model from the trained `model.joblib`.

Optionally, you may decide to use the best performing model trained during __Train at scale__. If so, load it from **Google Cloud Storage**.

We just need to store the resulting prediction in our **json** response:

``` json
{
  "prediction": 1.234
}
```

*Hint*: in order to play with your API, you may either fill the parameters manually in the URL, or use the notebook provided in `notebooks/API usage.ipynb`.

⚠️ The notebook is built to query an API responding to the following URL... Maybe you will want to adapt the way the notebook works if you choose a different format for your API ⚠️

`http://127.0.0.1:8000/predict?pickup_datetime=2013-07-06 17:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=1`

Congratulations, you just created your first API! 🎉

Let's see how we can put this API into production so that it gets exposed to the internet 🚀
