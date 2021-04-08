# Forecast API

ALeRCE Forecast API, build to have several types of forecast models for different astronomical object.


# Running the API

To run the API just install the requirements, there are some issues installing directly the resources from the file, we recommend installing them one by one.

For example in bash:
```bash
while read p; do pip install --use-deprecated=legacy-resolver $p; done < requirements.txt;
```

Then just run the app with
```bash
python -m web.app
```

This will deploy the webserver locally in http://localhost:5000

# Deploy the API

To deploy the API we recommend using a docker container with gunicorn.

Create the image
```bash
docker build -t forecast_api .
```

Run the container
```bash
docker run -p 8080:8080 forecast_api
```
This will deploy the API on port 8080.
