from DataAnalysis import analysis as a


x = a.Analysis("matura_data.csv")
print(x.compare_pass_ratio("Kujawsko-pomorskie", "Pomorskie"))
