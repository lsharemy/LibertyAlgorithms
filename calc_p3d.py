import matplotlib.pyplot as plt
import numpy as np
# Constant
dividendFee_ = 10
tokenPriceInitial_ = 0.0000001
tokenPriceIncremental_ = 0.00000001
magnitude = 2**64
tokenSupply_ =  3881381.8343*1e18
profitPerShare_ = 0
ethereumBalance = 78977.5157*1e18
myToken = 37920.3576*1e18

def sub(a,b):
	return a-b

def div(a,b):
	return a/b

def add(a,b):
	return a+b

def sellPrice():
	if (tokenSupply_ == 0):
		return tokenPriceInitial_ - tokenPriceIncremental_
	else:
		_ethereum = tokensToEthereum_(1e18)
		_dividends = _ethereum/dividendFee_
		_taxedEthereum = _ethereum-_dividends
		return _taxedEthereum


def tokensToEthereum_(_tokens):
	tokens_ = _tokens + 1e18
	_tokenSupply = tokenSupply_ + 1e18
	_etherReceived = (sub(
                (
                    (
                        (
                            tokenPriceInitial_ +(tokenPriceIncremental_ * (_tokenSupply/1e18))
                        )-tokenPriceIncremental_
                    )*(tokens_ - 1e18)
                ),(tokenPriceIncremental_*((tokens_**2-tokens_)/1e18))/2
            )/1e18)
	return _etherReceived


def sell(_amountOfTokens):
	_tokens = _amountOfTokens
	_ethereum = tokensToEthereum_(_tokens)
	_dividends = div(_ethereum,dividendFee_)
	_taxedEthereum = sub(_ethereum,_dividends)
	# print("Taxed:",_dividends)
	# print("Sell:",_taxedEthereum,"eth")
	global tokenSupply_
	tokenSupply_ = sub(tokenSupply_,_tokens)
	global profitPerShare_
	#_updatedPayouts = (profitPerShare_ * _tokens + (_taxedEthereum * magnitude))
	profitPerShare_ = add(profitPerShare_, (_dividends * magnitude) / tokenSupply_);


def restValueAfterSell(sellAmount, show = False):
	global profitPerShare_
	global tokenSupply_
	profitPerShare_ = 0
	if show:
		print("Token value before:",tokensToEthereum_(myToken)*0.9)
	sell(sellAmount*1e18)
	tokenValue = tokensToEthereum_(myToken)*0.9
	profitValue = myToken*profitPerShare_/magnitude
	totalValue = profitValue + tokenValue
	if show:
		print("Profit from sell",myToken*profitPerShare_/magnitude)
		print("Token value",tokensToEthereum_(myToken)*0.9)
		print("Total value",totalValue)
	tokenSupply_+=sellAmount*1e18

	return totalValue,tokenValue,profitValue

if __name__ == "__main__":
	baseValue = tokensToEthereum_(myToken)*0.9
	y4 = [baseValue,]
	y4 = y4*3800000
	token = [tokensToEthereum_(myToken)*0.9,]
	profit = [0,]
	record = 0
	total = [tokensToEthereum_(myToken)*0.9,]
	for i in range(1,3800000):
		totalValue,tokenValue,profitValue = restValueAfterSell(i)
		token.append(tokenValue)
		profit.append(profitValue)
		total.append(totalValue)
		if int(totalValue) == int(baseValue):
			record = i
		if i % 100000 == 0:
			print(str(i),"/3800000")

	x = np.linspace(1,3800000,3800000)
	y1 = np.array(token)
	y2 = np.array(profit)
	y3 = np.array(total)

	plt.plot(x,y1,color = 'red',linestyle="--")
	plt.plot(x,y2,color = 'blue',linestyle="-.")
	plt.plot(x,y3,color = 'black')
	plt.plot(x,y4,color = 'red',linestyle="--",linewidth=4)
	if record != 0:
		plt.plot(record,int(baseValue))
	plt.xlabel("Sell Tokens")
	plt.ylabel("Rest Value")
	plt.show()