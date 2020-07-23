#!/bin/bash
python main.py --url "https://www.indeed.com/cmp/Leidos/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f Leidos_reviews.csv
python main.py --url "https://www.indeed.com/cmp/Raytheon/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f Raytheon_reviews.csv
python main.py --url "https://www.indeed.com/cmp/CACI-International-Inc/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f CACI_reviews.csv
python main.py --url "https://www.indeed.com/cmp/Perspecta/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f Perspecta_reviews.csv
python main.py --url "https://www.indeed.com/cmp/Booz-Allen-Hamilton/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f BoozAllen_reviews.csv
python main.py --url "https://www.indeed.com/cmp/Jacobs/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f Jacobs_reviews.csv
python main.py --url "https://www.indeed.com/cmp/SAIC/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f SAIC_reviews.csv
python main.py --url "https://www.indeed.com/cmp/ManTech-International-Corporation/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f ManTech_reviews.csv
python main.py --url "https://www.indeed.com/cmp/Peraton/reviews?fcountry=US&floc=Washington%2C+DC" --limit 300 -f Peraton_reviews.csv

