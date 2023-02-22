from numba import jit
import numpy as np


MODEL_PARAMS = [
    "SPM_t0",
    "SPM_chi",
    "SPM_gamma",
    "SPM_beta",
    "SPM_A",
    "SPM_tau_rise",
    "SPM_tau_fall",
]


class SNModel:
    def flux_to_mag(flux):
        return 16.4 - 2.5 * np.log10(flux)

    @jit(nopython=True)
    def model_inference(times, A, t0, gamma, f, t_rise, t_fall):
        # f in this function is SPM_beta
        beta = 1.0 / 3.0
        t1 = t0 + gamma

        sigmoid = 1.0 / (1.0 + np.exp(-beta * (times - t1)))
        den = 1 + np.exp(-(times - t0) / t_rise)
        flux = A * (1 - f) * np.exp(-(times - t1) / t_fall) / den * sigmoid + A * (
            1.0 - f * (times - t0) / gamma
        ) / den * (1 - sigmoid)
        return flux
