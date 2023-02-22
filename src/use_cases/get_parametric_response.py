from src.domain.domain_methods import get_parameters, get_features_message, infer


def get(oid, forecast_mjd, shifted_mjd):

    features_on_db, parameters = get_parameters(oid)
    message = get_features_message(features_on_db)

    forecasts = []
    for fid in parameters.fid.unique():
        fid_params = parameters[parameters.fid == fid]
        fid_params.set_index("name", inplace=True)
        fid_params = fid_params.value
        magpsf = infer(fid_params, shifted_mjd)
        forecasts.append(
            {
                "magpsf": magpsf,
                "mjd": forecast_mjd,
                "fid": fid,
            }
        )

    return {"oid": oid, "forecast": forecasts, "comment": message}
