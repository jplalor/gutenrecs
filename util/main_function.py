
#main script to pull everything together
import gutenbergtextPCA, gutenbergtextPCALSA, newsimilarity

gutenberg-text-PCA.runPCA()
gutenberg-text-PCALSA.runPCALSA()

#LSA only already completed.
newsimilarity.calcSim('pca_file.mtx')
newsimilarity.calcSim('pca_lsa_file.mtx')


