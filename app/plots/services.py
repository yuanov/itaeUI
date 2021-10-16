import numpy as np
import matplotlib.pyplot as plt
from numpy.core.function_base import linspace
from math import sqrt
from cmath import pi, exp
from scipy.integrate import dblquad
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from pathlib import Path

from app.plots.enums import Shapes


class RCS:
    @staticmethod
    def _field(x, y, z, shape: Shapes):
        lambd = 1
        k = 2 * pi / lambd
        z = lambd * z
        u = exp(-1j * k * z)

        def func_real(ksi, eta):
            r = sqrt((ksi - x) ** 2 + (eta - y) ** 2 + z ** 2)
            expr1 = exp(-1j * k * r) / r * (-1j * k * u)
            expr2 = u * (-(1j * k / r + 1 / r ** 2) * exp(-1j * k * r) * z / r)
            return 1 / (4 * pi) * (expr1 - expr2).real

        def func_imag(ksi, eta):
            r = sqrt((ksi - x) ** 2 + (eta - y) ** 2 + z ** 2)
            expr1 = exp(-1j * k * r) / r * (-1j * k * u)
            expr2 = u * (-(1j * k / r + 1 / r ** 2) * exp(-1j * k * r) * z / r)
            return 1 / (4 * pi) * (expr1 - expr2).imag

        if shape == shape.CIRCLE:
            r = 1.5
            return dblquad(func_real, -r, r,
                           lambda eta: -sqrt(r ** 2 - eta ** 2),
                           lambda eta: sqrt(r ** 2 - eta ** 2)), \
                   dblquad(func_imag, -r, r,
                           lambda eta: -sqrt(r ** 2 - eta ** 2),
                           lambda eta: sqrt(r ** 2 - eta ** 2))
        if shape == shape.SQUARE:
            return dblquad(func_real, -1.5, 1.5, lambda eta: -1.5, lambda eta: 1.5), \
                   dblquad(func_imag, -1.5, 1.5, lambda eta: -1.5, lambda eta: 1.5)

    @classmethod
    def get_plot(cls, z: float, shape: Shapes):
        num_x = 20
        num_y = 20
        xs = linspace(-20, 20, num_x)
        ys = linspace(-20, 20, num_y)
        zs = np.zeros((num_y, num_x))
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                res = cls._field(x=x, y=y, z=z, shape=shape)
                zs[j][i] = abs(res[0][0] + 1j * res[1][0])

        plt.figure(figsize=(9.6, 5))
        font = {'size': 14}
        plt.rc('font', **font)
        cc = plt.contourf(xs, ys, np.abs(zs), cmap="coolwarm", levels=100)
        plt.colorbar(cc)
        plt.title('E', color='black')
        plt.grid(True)
        plt.tight_layout()
        tf = NamedTemporaryFile(delete=False)
        tf.seek(0)
        plt.savefig(tf)

        return FileResponse(Path(tf.name), filename='rcs.png')


rcs = RCS()
