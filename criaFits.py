import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as pf
from scipy.interpolate import interp1d
from scipy import interpolate


sourceNames=['/graduacao/theweckerle/Downloads/Stars/2m.csv',] # Lista com o nome dos arquivos a serem convertidos ['nome','nome2','nome3']

plot=True   # Salvar o plot (usar True ou False)

savetxt=True # Salvar txt, True ou False

NormalizationFactor=1E-3   # Fator de escala dos espectros

# Varrendo todos os arquivos

for sourceName in sourceNames:
    
    # Abrindo o arquivo
    f,l = np.loadtxt(sourceName, delimiter=',', unpack=True, dtype='float', skiprows=1)

    # Rebinando de modo a ter um passo constante, pequeno o suficiente para nao perder informacoes
    rebin=interpolate.interp1d(l,f)
    # calculando o tamanho do passo no inicio do espectro e pegando soh 10%
    binsize=0.1*(l[1]-l[0]) 
    # criando um array com os novos comprimentos de onda (rebinados)
    n_l=np.arange(l[0],l[-1],binsize)
    # Interpolando os antigos para poder calcular os novos valores 
    n_f=rebin(n_l)*NormalizationFactor
    # criando a lista de HDU (para fazer o fits)
    savefile=pf.HDUList()
    # criando a lista de header (para fazer o fits)
    hdr = pf.Header()
   # Adicionando keywords aos header
    hdr.append(('OBJECT',sourceName.split('.')[0]))
    hdr.append(('CTYPE1','LINEAR'))
    #  hdr.append(('CRPIX1',float(n_l[0])))
    hdr.append(('CRVAL1',float(n_l[0])))
    hdr.append(('CD1_1',float(binsize)))
    #hdr.append(('WAT1_001', 'wtype=linear axtype=wave' ))
    # Salvando os valores de fluxo no HDU
    savefile.append(pf.ImageHDU(data=n_f,header=hdr))
    # grando o HDU em fits
    savefile.writeto(sourceName.split('.')[0]+'.fits',overwrite=True)
    if savetxt:

       save=np.column_stack((n_l,n_f))
       np.savetxt(sourceName.split('.')[0]+'.txt',save,fmt='%.2f %.2e',header='lambda  flux')



    if plot:
        plt.plot(l,f)
        plt.plot(n_l,n_f)
        plt.savefig(sourceName.split('.')[0]+'.png')
#        plt.show()


