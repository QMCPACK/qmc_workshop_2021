#!/usr/bin/env python3                                                                                                                                                                         
# INLCUDE THE FOLLOWING IN YOUR SCRIPT:
#=====================================
#import sys
#sys.path.append('/path/to/python/file/')
#from functions import *

### ================= PACKGAES ======================

import sys
import os
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker

import uncertainties
from uncertainties import ufloat
from uncertainties import unumpy
from uncertainties import ufloat_fromstr

import string
from scipy.optimize import curve_fit

from itertools import repeat

### =================== FUNCTIONS ======================

class ShorthandFormatter(string.Formatter):
	def format_field(self, value, format_spec):
		if isinstance(value, uncertainties.UFloat):
			return value.format(format_spec+'S')  # Shorthand option added
		# Special formatting for other types can be added here (floats, etc.)
		else:
			# Usual formatting:
			return super(ShorthandFormatter, self).format_field(value, format_spec)
frmtr = ShorthandFormatter()

def f2s(x, digits = 1):   # float to string
	try:
		#y = frmtr.format("{0:.1u}", x)
		y = frmtr.format("{0:."+str(digits)+"u}", x)
	except:
		y = x
	return y

def s2f(x):   # string to float
	if isinstance(x, float) or isinstance(x, int):
		y = x
	else:
		try:
			try:
				y = float(x)
			except:
				y = ufloat_fromstr(x)
		except:
			y = x
	return y

def pd_s2f(df):   # df to df with uncertainties
	udf = df.copy()
	for column in df.columns:
		try:
			udf[column] = list(map(s2f,list(df[column])))
		except:
			udf[column] = "pd_s2f failed"
	return udf

def pd_f2s(udf, digits = 1):   # df to df with uncertainties
	df = udf.copy()
	for column in udf.columns:
		try:
			#df[column] = list(map(f2s,list(udf[column])))
			df[column] = list(map(f2s,list(udf[column]), repeat(digits)))
		except:
			df[column] = "pd_f2s failed"
	return df

def pd_mad(errors):	# Handle MAD with error bars
	errors = np.mean(np.absolute(np.array(errors)))
	return errors

def size_linear(x, a, b):
        y = a + b*x
        return y

def cons_linear(x, b, en_lim):
        y = en_lim + b*x
        return y

def init():
    font   = {'family' : 'serif', 'size': 18}
    lines  = {'linewidth': 2.0}
    axes   = {'linewidth': 2.0}    # border width
    tick   = {'major.size': 2, 'major.width':2}
    legend = {'frameon':True, 'fontsize':15.5, 'handlelength':2.20, 'labelspacing':0.40, 'handletextpad':0.4, 'loc':'best', 'facecolor':'white', 'framealpha':1.00, 'edgecolor':'#f2f2f2'}
    mpl.rc('font',**font)
    mpl.rc('lines',**lines)
    mpl.rc('axes',**axes)
    mpl.rc('xtick',**tick)
    mpl.rc('ytick',**tick)
    mpl.rc('legend',**legend)
    mpl.rcParams['text.usetex'] = True
    mpl.rcParams.update({'figure.autolayout':True})
    fig = plt.figure()
    fig.set_size_inches(7.0, 5.4)   # Default 6.4, 4.8
    ax1 = fig.add_subplot(111) # row, column, nth plot
    ax1.tick_params(direction='in', length=6, width=2, which='major', pad=6)
    ax1.tick_params(direction='in', length=4, width=1, which='minor', pad=6)
    ax1.grid(b=None, which='major', axis='both', alpha=0.15)
    y_formatter = ScalarFormatter(useOffset=False)
    ax1.yaxis.set_major_formatter(y_formatter)

    return fig, ax1

toev = 27.211386245988

