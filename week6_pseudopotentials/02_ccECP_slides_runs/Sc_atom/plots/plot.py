#!/usr/bin/env python3

from functions import *

totals = pd.read_csv("data.csv", delim_whitespace=True, engine='python', index_col=['timestep'])
totals = pd_s2f(totals)
#print(totals)

zero = []
slopes = {}
xdata = list(map(float, list(totals.index)))
#print(xdata)
for method in totals.columns:
	#print(method)
	ydata = unumpy.nominal_values(list(totals[method]))
	yerr = unumpy.std_devs(list(totals[method]))
	#print(ydata)
	#print(yerr)
	initial=[min(ydata), 0.0]
	try:
	        popt, pcov = curve_fit(size_linear, xdata, ydata, sigma=yerr, p0=initial)
	except:
	        popt = [np.nan]
	        pcov = [np.nan]
	#print("Fit params:", method, popt, np.sqrt(np.diag(pcov)))
	zero.append(ufloat(popt[0], np.sqrt(np.diag(pcov))[0]))
	slopes[method] = popt

totals.loc[0.0] = zero
print(pd_f2s(totals))


my_colors = {'no':'blue', 'v0':'red', 'v1':'green'}
my_labels = {'no':'LA', 'v0':'T-Moves (2006)', 'v1':'T-Moves (2010)'}

fig, ax = init()

for method in ['no', 'v0', 'v1']:
	xdata = np.array(list(map(float, list(totals.index))))
	ydata = unumpy.nominal_values(list(totals[method]))
	yerr = unumpy.std_devs(list(totals[method]))
	
	x = np.linspace(0.0,xdata[0],50)
	y = size_linear(x, *slopes[method])
	
	ax.errorbar(xdata, ydata, yerr=yerr, linestyle='None', color=my_colors[method], alpha=0.6, marker='o', markersize=6, markeredgecolor='#000000', markeredgewidth=0.5, capsize=3, label=my_labels[method])
	plt.plot(x, y, '--', lw=1, color=my_colors[method])
	ax.set_xlabel(r'Timestep [Ha$^{-1}$]')
	ax.set_ylabel(r'FN-DMC Energy [Ha]')
	xlabels = np.array(list(map("{:.4f}".format, list(totals.index))))
	plt.xticks(xdata, labels=xlabels, rotation = 50, fontsize=17)
	
legend = ax.legend(loc='upper right', shadow=False)
plt.savefig('timesteps_locality.pdf', format='pdf')
plt.show()
