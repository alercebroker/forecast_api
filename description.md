# Models

## Parametric Model

### Supernova parametric model.

Forecast based on modified **Villar et al. 2019. analytic model** (see [https://arxiv.org/abs/1905.07422] and [https://arxiv.org/abs/2008.03311]).

The model uses the pre-computed parameters from the alert stream when there are enough detections, when there are not enough we calculate the parameteres on-demand.

# Using the documentation.

Each model has their specific namespace. In each model we can see the different routes available.

For example the Parametric SN model is in
```
GET /parametric/sn
```
Selecting the route shows the different fields available. By default it uses the ZTF Object ID and uses the current mjd. The mjd field is an optional field for every model and is the date we want the forecast magnitude.

The interface can be used to test the request and generate a **curl** request example to use it with bash.
```
curl -X GET "http://api.alerce.online/forecast/v1/parametric/sn?oid=ZTF20aaelulu" -H "accept: application/json"
```
