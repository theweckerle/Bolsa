from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



hdul = fits.open('/graduacao/theweckerle/Downloads/Stars/ADP.2017-10-26T16_00_38.264.fits') 
hdul.info()

#hdulist = fits.open('ADP.2017-10-26T16_00_38.264.fits')

hdu_number = 0
fits.getheader('/graduacao/theweckerle/Downloads/Stars/ADP.2017-10-26T16_00_38.264.fits', hdu_number)
data = hdul[1].data
lambda1 = data.field(0)
flux=data.field(3)

x = np.array(lambda1, dtype=np.float)
y = np.array(flux, dtype=np.float)

d = {'lambda1': x[0][:], 'flux': y[0][:]}
a2 = pd.DataFrame(d)
a2.to_csv('2m.csv', index=False, sep=',')


#plt.plot(lambda1,flux)
#plt.show()  

print(type(data))


