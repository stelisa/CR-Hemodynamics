import omnicare_tools.bloodpressure as ob
df = ob.Blood_pressure('03_bp_df.csv')
df.showhead(15)
df.preprocess_lineplot('test22')