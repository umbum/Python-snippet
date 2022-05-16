import sys


if sys.argv[1] == 'apy':
    apy = int(sys.argv[2].replace(",", ""))
    daily_apr = (1 + (apy/100)) ** (1/365) - 1
    print('apy to daily apr: {}%'.format(daily_apr * 100))
    print('apy to yearly apr: {}%'.format(daily_apr * 365 * 100))
elif sys.argv[1] == 'apr':
    apr = int(sys.argv[2].replace(",", ""))
    print('apr to apy: {}'.format((1 + (apr/100)) ** 365))
    
