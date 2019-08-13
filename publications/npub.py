files = ['publist_1st.tex', 'publist_major.tex', 'publist_others.tex']
npub = []
for file in files:
    with open(file) as f:
        npub.append(sum([line.startswith('\\item') for line in f]))
    print('{0} publications in {1}'.format(npub[-1], file))
print('Total {0} publications'.format(sum(npub)))

