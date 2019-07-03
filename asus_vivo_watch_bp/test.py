import omnicare_tools.bloodpressure as ob
df = ob.Blood_pressure('03_bp_df.csv')
df.showhead(15)

# Test with arbitary file name
df.preprocess('test22')
df.lineplot(saveFile=True)
df.errorbar(saveFile=True)
