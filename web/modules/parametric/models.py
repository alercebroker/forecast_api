from flask_restx import Resource, fields, Model

forecast_model = Model(
    "forecast",
    {
        "magap": fields.Float(
            description="Forecast Apparent Magnitude"
        ),
        "mjd": fields.Float(
            description="MJD associated to forecast"
        ),
        "fid": fields.Integer(
            description="Filter ID (1=g; 2=r; 3=i)"
        )
    }
)

parametric_response = Model(
    "Parametric Model Response",
    {
        "oid": fields.String(description="Object identifier"),
        "forecasts": fields.List(fields.Nested(forecast_model)),
        "message": fields.String(description="Metadata from forecast")

    }

)
