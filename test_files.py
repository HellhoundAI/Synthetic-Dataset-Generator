filenames = ['test1.txt', 'test2.txt', 'test3.txt', 'test4.txt', 'test5.txt']
with open('test_join2.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line_n, line in enumerate(infile):
                # nasledujici radka zajisti, ze prvni radek souboru (nazvy sloupcu) se nebere v potaz
                if line_n == 0:
                    continue

                # je NUTNE aby soubory koncily s 1 prazdnou radkou
                outfile.write(line)